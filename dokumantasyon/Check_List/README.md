# 🛡️ OCPP & EV Şarj İstasyonu Güvenlik Kontrol Listesi (50 Madde)

Bu kontrol listesi, elektrikli araç şarj istasyonlarının (EVCS) merkezi yönetim sistemi (CSMS) ve şarj ünitesi (CP) arasındaki iletişim ve donanım katmanlarında karşılaşılabilecek olası güvenlik zafiyetleri ve anomali türlerini kapsamaktadır. [cite_start]Özellikle, projemizin odak noktası olan **Zaman Kaydırma** ve **Enerji Hırsızlığı** gibi siber-fiziksel anomalilerin tespiti hedeflenmiştir[cite: 5, 81, 165].

## 🎯 Projenin Amacı ve Kapsamı

[cite_start]Kontrol listesi, **Yapay Zeka Destekli Anomali Tespit Sisteminin** (SMART Hedef 1) geliştirilmesi için bir **veri etiketleme ve kural tabanlı tespit altyapısı** oluşturmayı amaçlar[cite: 163, 175].

Liste, sekiz ana kategoride toplanmış olup, her bir madde bir güvenlik açığı, hatalı konfigürasyon veya anomaliye işaret eder. 

---

## 📋 Güvenlik Kontrol Listesi Kategorileri

Kontrol listesi, istasyon güvenliğini uçtan uca değerlendirmek üzere tasarlanmıştır:

### 1. Kimlik Doğrulama & Erişim Kontrolü (A)
* [cite_start]CP ve CSMS arasındaki bağlantının **Mutual TLS (mTLS)** ile kurulup kurulmadığı[cite: 52, 117].
* Cihazlarda **varsayılan (default) kimlik bilgilerinin** kullanılıp kullanılmadığı.

### 2. Giriş Doğrulama (V)
* [cite_start]Gelen **OCPP JSON yüklerinin şema ve format doğrulamasından** geçip geçmediği[cite: 8, 157].
* [cite_start]CAN-Bus'a iletilen komut ID'lerinin **izin verilen listeler (whitelisting)** ile filtrelediği[cite: 50, 126].

### 3. Kriptografi (C)
* [cite_start]Kritik bileşenlerin sadece imzalı yazılım çalıştırmasını sağlayan **Güvenli Önyükleme (Secure Boot)** mekanizmasının varlığı[cite: 51].
* [cite_start]OTA (Over-the-Air) firmware güncellemelerinde **imza doğrulaması**nın zorunlu tutulması[cite: 9, 51].

### 4. Bütünlük (Integrity) (I)
* [cite_start]MeterValues gibi faturalandırma verilerinin **dijital olarak imzalanması** (OCPP 2.0.1'de `SignedMeterValues` özelliği)[cite: 105, 116].
* [cite_start]Ağ trafiğindeki mesajların **sıra takibinin** yapılması (Replay saldırılarına karşı)[cite: 107].

### 5. Zaman ve Enerji (T) **(Proje Odak Noktası)**
* [cite_start]CP ile CSMS arasındaki zaman damgası farkının (**Timestamp Delta**) belirli bir eşiğin (`< 5 saniye`) altında olup olmadığının sürekli izlenmesi[cite: 108].
* [cite_start]NTP sunucusunun durumunun takip edilmesi (NTP Spoofing/Zehrine karşı)[cite: 92, 104, 119].
* Raporlanan şarj değerlerinin, geçen **zamana göre fiziksel limitleri** aşıp aşmadığı.

### 6. Ağ Güvenliği (N)
* CP üzerinde harici erişime açık **gereksiz portların** olup olmadığı.
* [cite_start]CSMS'ye gelen bağlantı oranlarında **anormal bir yükselişin** (Brute Force/DoS riski) olup olmadığı[cite: 207].

### 7. Davranışsal Anomali (B)
* [cite_start]Şarj işlemleri sırasında `RemoteStart` ve `RemoteStop` komutlarının **anormal hızda tekrarı**[cite: 7].
* Kullanıcı şarj sürelerinin veya tüketim profillerinin **genel ortalamadan** ciddi şekilde sapması.

### 8. Fiziksel ve Olay Yanıtlama (P & D)
* [cite_start]Kritik anahtarların **TPM/HSM** gibi güvenli bir elementte saklanıp saklanmadığı[cite: 15].
* [cite_start]Bir anomali tespit edildiğinde, sistemin **otomatik müdahale** (şarjı durdurma, erişimi kısıtlama) yeteneğinin olup olmadığı (SMART Hedef 4)[cite: 166].

---

## 📝 Uygulama ve Kullanım

Bu kontrol listesi, projenizin iki ana bileşenini destekler:

1.  [cite_start]**Kural Tabanlı IDS:** Özellikle T1, T2 ve V3 gibi maddeler, temel seviyede anomali tespiti için (`IF [Şart] THEN ALARM`) basit **Güvenlik Geçidi (Gateway)** filtreleri oluşturmak için kullanılır.
2.  **Yapay Zeka Veri Etiketlemesi:** Kontrol listesindeki maddeler, toplanan gerçek veya sentetik saldırı verilerini (örneğin MeterValues veya CAN trafiği) etiketlemek için kullanılır. [cite_start]Etiketli bu veri setleri, **Zaman Serisi Kümeleme** veya **Autoencoder** gibi yapay zeka modellerini eğitmek için temel oluşturur.

---
