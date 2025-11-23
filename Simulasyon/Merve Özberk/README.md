# Şarj İstasyonlarında Hayalet Akım (Phantom Current) Saldırı Simülasyonu

Bu proje, Elektrikli Araç Şarj İstasyonlarında (EVSE) meydana gelebilecek "Hayalet Akım Çekme" (Phantom Current Draw) anomalisini simüle etmek ve tespit etmek amacıyla geliştirilmiştir.

## 🎯 Proje Amacı
Merkezi yönetim sisteminde (CSMS) şarj işlemi sonlanmış olmasına rağmen, istasyonun enerji tüketmeye devam ettiği (veya ediyor gibi sahte veri gönderdiği) senaryoyu canlandırmak ve bu durumu yazılımsal olarak yakalamaktır.

## 🛠 Kullanılan Teknolojiler
* **Dil:** Python 3
* **Protokol:** OCPP 1.6 (Open Charge Point Protocol)
* **Kütüphaneler:** `ocpp`, `websockets`, `asyncio`

## 📂 Dosyalar
* **`csms_server.py`:** Merkezi Yönetim Sistemi (Sunucu). Anomali tespit algoritmasını içerir.
* **`cp_attacker.py`:** Saldırgan Şarj İstasyonu. Normal şarj sonrası sahte veri enjekte eder.

## 🚀 Kurulum ve Çalıştırma

1. Kütüphaneleri yükleyin:
   ```bash
   pip install ocpp websockets
   Önce Sunucuyu (CSMS) başlatın:
   python csms_server.py
   eni bir terminalde Saldırganı (Attacker) başlatın:
   python cp_attacker.py
   📊 Senaryo Akışı
İstasyon normal şarj başlatır (StartTransaction).

Şarj yasal olarak durdurulur (StopTransaction).

Saldırgan modundaki istasyon, oturum kapalıyken sahte sayaç verileri (MeterValues) göndermeye başlar.

Sunucu bu durumu tespit eder ve "ANOMALİ TESPİT EDİLDİ" uyarısı verir.
