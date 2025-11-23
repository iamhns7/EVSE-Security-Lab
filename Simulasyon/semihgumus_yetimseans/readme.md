# EVSE Security Lab – Yetim Seans Anomali Simülasyonu

Bu proje, **EV şarj istasyonlarının güvenliği** kapsamında OCPP 1.6 kullanan
basit bir **CSMS (merkez sistem) + Charge Point (şarj istasyonu)** simülasyonudur.

Amaç:  
**Fiş çekildiği hâlde seansın düzgün kapanmaması** gibi hataları (Yetim Seans / Orphan Session)
simüle etmek ve bunları bir **Anomali Dedektörü** ile tespit etmektir.

---

## 1. Proje Yapısı

Klasördeki önemli dosyalar:

- `csms.py`  
  - OCPP 1.6 WebSocket sunucusu (CSMS).
  - Şu mesajları karşılar:
    - `BootNotification`
    - `StatusNotification`
    - `StartTransaction`
    - `MeterValues`
    - `StopTransaction`
  - Her mesaj geldiğinde **session state**’i günceller ve
    `AnomalyDetector` üzerinden kuralları kontrol eder.
  - Konsolda küçük bir **“Yetim Seans İzleme Paneli”** gösterir.

- `charge_point.py`  
  - Tek bir istasyonu temsil eden **OCPP client**.
  - CSMS’e bağlanır ve sırayla şu senaryoları çalıştırır:
    1. **Normal akış**  
       - BootNotification → StartTransaction → MeterValues → StopTransaction  
       - Durum geçişleri: `Available → Charging → Finishing → Available`
    2. **S1 – StopTransaction gecikmesi (Yetim Seans)**  
       - StartTransaction ve Charging sonrası fiş çekiliyor gibi  
         `StatusNotification(Finishing/Available)` gönderiliyor.  
       - **StopTransaction özellikle gönderilmiyor.**  
       - CSMS tarafında belirlenen `timeout` (örn. 30 sn) geçince **Kural-1 alarmı** beklenir.
    3. **S2 – Durum kilitlenmesi (Status Lock)**  
       - Seans normal bir şekilde StopTransaction ile bitiyor.  
       - Buna rağmen istasyon hâlâ `Charging` status gönderiyor.  
       - CSMS tarafında **Kural-2 alarmı** beklenir.

- `anomaly_detector.py`  
  - Her `connector_id` için şu bilgileri tutar (örnek):
    - `status` (OCPP durumu: Available, Charging, Finishing, vs.)
    - `plug_state` (fiş takılı mı, çekili mi? – mantıksal model)
    - `session_active` (şarj oturumu açık mı?)
    - `meter_total_kwh` (son sayaç değeri)
    - `plug_false_time` (fiş çekildiğinin görüldüğü zaman)
  - `update_state(...)` ile CSMS’ten gelen her olayda durum güncellenir.
  - `check_for_anomaly(connector_id)` kuralları uygular ve gerekirse
    **alarm metni döndürür**.

---

## 2. Uygulanan Güvenlik Kuralları (Anomali Tespiti)

Örnek kurallar:

1. **Kural-1: Yetim Seans (StopTx yok)**  
   - Fiş çekilmiş durumda kabul edilir (`plug_state = False`),  
     fakat belirli süre (örn. 30 sn) içinde **StopTransaction mesajı gelmezse**  
     → **“Yetim Seans”** alarmı üret.

2. **Kural-2: Durum Kilitlenmesi (Charging Status Lock)**  
   - `plug_state = False` (fiş çekilmiş)  
   - ama `status = Charging` gelmeye devam ediyor  
   → fiziksel durum ile OCPP durumu çelişkili → **alarm**.

3. **Kural-3: Sayaç Artışı Fiş Çekiliyken**  
   - `plug_state = False` iken `meter_total_kwh` artmaya devam ediyorsa  
   → fiş yok ama enerji akışı varmış gibi gözüküyor → **alarm**.

CSMS tarafında bu alarm metinleri, loglarda:

```text
🚨🚨 Kural-1: ... 🚨🚨
🚨🚨 Kural-2: ... 🚨🚨

gibi görünür.

3. Kurulum

Not: Bu projede venv klasörü versiyon kontrolüne eklenmez.
Her kullanıcı kendi sanal ortamını oluşturur.

Proje klasörüne gir:

cd SEMIHGUMUS_YETIMSEANS


Sanal ortam oluştur ve aktive et (Windows):

python -m venv venv
.\venv\Scripts\activate


Gerekli Python paketlerini yükle:

pip install ocpp websockets


İstersen bunları requirements.txt içine de yazabilirsin:

ocpp
websockets


ve sonra:

pip install -r requirements.txt

4. Çalıştırma
4.1. CSMS Sunucusunu Başlat
python csms.py


Konsolda şuna benzer bir çıktı görmelisin:

INFO:root:CSMS Başlatıldı: ws://0.0.0.0:9000


Bu terminal açık kalacak. CSMS, OCPP 1.6 bağlantılarını bekliyor.

4.2. Şarj İstasyonu (Charge Point) Simülatörünü Çalıştır

Yeni bir terminal aç, yine sanal ortamı aktive et ve:

python charge_point.py


Bu script sırasıyla:

BootNotification gönderir ve CSMS’ten Accepted cevabı alır.

Normal şarj senaryosunu çalıştırır.

S1 senaryosu için StopTransaction göndermeden fiş çekilmiş gibi davranır.

S2 senaryosu için seans bittikten sonra tekrar Charging status gönderir.

5. Beklenen Çıktılar

charge_point.py tarafında:

Gönderilen OCPP istekleri ve alınan cevaplar,

Senaryo adımlarını açıklayan INFO/WARNING logları.

csms.py tarafında:

Her mesaj sonrası küçük bir metin paneli:

==================================================
  ⚡ Yetim Seans İzleme Paneli (CSMS) 🛡️
==================================================
| Connector ID: 1
|   - Durum: ChargePointStatus.charging | Oturum: 🟢 AKTİF
|   - Fiş: 🔌 TAKILI
|   - Sayaç: 0.15 kWh
--------------------------------------------------


S1 / S2 sırasında anomali kuralları tetiklendiğinde:

🚨🚨 Kural-1: ... 🚨🚨
🚨🚨 Kural-2: ... 🚨🚨


gibi uyarılar görünür.

6. Notlar

Bu simülasyon, gerçek şarj istasyonuna bağlanmadan OCPP mesaj akışını ve
güvenlik senaryolarını test etmek için tasarlanmıştır.

Testler izole bir ağda / lab ortamında koşturulmalıdır.

Proje, Bilgi Sistemleri Güvenliği dersi kapsamındaki
EVSE Security Lab – Yetim Seans Anomali Tespiti çalışması için hazırlanmıştır.


