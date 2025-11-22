# 🔌 EV Şarj İstasyonlarında Siber Güvenlik Mimarisi ve Anomali Tespiti

Bu proje, elektrikli araç şarj altyapılarında (EVCS) ortaya çıkan siber güvenlik tehditlerini incelemekte ve özellikle **OCPP protokolü** üzerinden gerçekleştirilen **Zaman Senkronizasyonu Manipülasyonu** saldırılarına karşı proaktif bir savunma mekanizması geliştirmeyi hedeflemektedir. Çalışma, yapay zekâ destekli anomali tespiti ve blokzincir tabanlı veri bütünlüğü çözümlerini merkezine almaktadır.

---

## 1. 🕒 Anomali Senaryosu: Zaman Kaydırma ile Enerji Maskelenmesi

Bu çalışmanın temelini oluşturan anomali, şarj istasyonlarının faturalandırma ve yük yönetimi süreçlerini hedef almaktadır.

### Saldırı Özeti

Saldırgan, şarj istasyonu (CP) ile merkezi yönetim sistemi (CSMS) arasındaki OCPP trafiğine **Man-in-the-Middle (MitM)** yöntemiyle müdahale eder. [cite_start]Saldırının amacı, yüksek tarifeli saatlerde tüketilen enerjiyi, düşük tarifeli saatlere aitmiş gibi göstermektir[cite: 289, 293].

| Parametre | Fiziksel Gerçeklik | Saldırganın Kaydı | Sonuç |
| :--- | :--- | :--- | :--- |
| **Gerçek Zaman** | [cite_start]Yüksek Tarife (Örn: 14:00) [cite: 278] | [cite_start]Düşük Tarife (Örn: 02:00) [cite: 278] | **Yanlış Faturalandırma** |
| **Gerçek Tüketim** | [cite_start]50 kWh [cite: 278] | [cite_start]35 kWh [cite: 278] | **Gelir Kaybı (Revenue Loss)** |

### [cite_start]Saldırının Vektörleri [cite: 290, 291, 304, 305]

* **Zaman Damgası Manipülasyonu:** `MeterValues` veya `TransactionEvent` mesajlarının zaman damgası değiştirilir.
* **NTP Zehirlenmesi:** Şarj istasyonunun NTP sunucusuna müdahale edilerek sistem saati kaydırılır.
* **Zayıf Şifreleme:** MitM saldırısını mümkün kılan zayıf TLS/WS veya zayıf kimlik doğrulama kullanılır.

### [cite_start]Etkileri [cite: 309, 310, 312]

* **Finansal Etki:** Faturalandırma hatası ve operatör için gelir kaybı.
* **Operasyonel Etki:** Şebeke yönetim sistemlerinde hatalı enerji verisi nedeniyle yük dengeleme algoritmalarının yanlış çalışması.
* **Yasal Etki:** MID ve ISO 15118 standartlarına göre kayıt bütünlüğünün bozulması.

---

## 2.  SWOT Analizi ve Tehdit Modelimiz

Projenin tehdit modelini derinlemesine anlamak ve stratejik savunma hedeflerini belirlemek amacıyla bir **SWOT Analizi** yapılmıştır. [cite_start]Analiz, EV şarj altyapılarındaki temel güvenlik zafiyetlerine odaklanmaktadır[cite: 86, 96].

### [cite_start]A. Temel Problemler ve Zafiyetler [cite: 87, 88, 89, 90]

Proje, dört ana güvenlik problemine karşı çözüm üretmeyi hedefler:

1.  **Zayıf Şifreleme:** `ws://` kullanımı veya zayıf sertifikasyon (self-signed/test) MitM saldırılarına kapı açar.
2.  **Yetkisiz Erişim:** Zayıf kimlik doğrulama mekanizmaları nedeniyle CP/CSMS'e izinsiz girişler.
3.  **Man-in-the-Middle (MitM) Saldırıları:** İletişim trafiğinin yakalanıp değiştirilmesi (Zaman Kaydırma senaryosunun ana vektörü).
4.  **Firmware ve Yazılım Açıkları:** CAN seviyesinde davranış değiştirebilecek zararlı firmware enjeksiyonları.

### [cite_start]B. SMART Hedefler (Proje Odak Noktaları) [cite: 102, 104, 105, 106]

Geliştirilecek sistemin başarısını ölçmek için hedefler belirlenmiştir:

| Hedef ID | Tanım | Metrik (Minimum Başarı Oranı) |
| :--- | :--- | :--- |
| **Hedef 1** | Anomali Tespit Sisteminin Geliştirilmesi | Anormal davranışların $\ge 95\%$ doğrulukla tespiti. |
| **Hedef 3** | Enerji Hırsızlığı ve Sahte Veri Algoritması | Enerji hırsızlığının gerçek zamanlı olarak $\ge 90\%$ hassasiyetle tespiti. |
| **Hedef 4** | Gerçek Zamanlı İzleme ve Müdahale Modülü | Şüpheli aktivite tespit edildiğinde ortalama 30 saniye içinde otomatik müdahale (şarjı durdurma). |
| **Hedef 5** | Standartlara Uygunluk | Geliştirilen sistemin OCPP 2.0, ISO 27001 ve ISO 15118 gibi standartlara $100\%$ uyumlu olması. |

### C. Analiz Bileşenleri

| Kategori | Açıklama |
| :--- | :--- |
| **Güçlü Yönler (Strengths)** | [cite_start]Yapay zekâ (Zaman Serisi Kümeleme, Autoencoder) [cite: 113] [cite_start]ve blokzincir teknolojisi kullanılarak veri bütünlüğünün ve izlenebilirliğin sağlanması[cite: 161, 167]. |
| **Zayıf Yönler (Weaknesses)** | [cite_start]Blokzincir katmanının mimariye eklenmesiyle oluşabilecek **Mesaj İşleme Süresi** ve **CPU/Bellek** kullanımı artışı[cite: 222, 226]. |
| **Fırsatlar (Opportunities)** | [cite_start]Geliştirilen sistemin uluslararası standartlara (OCPP, ISO 15118) uyumluluğu ile pilot uygulama ve yaygınlaştırma potansiyeli[cite: 106, 107]. |
| **Tehditler (Threats)** | [cite_start]MitM, Sahte Mesaj Enjeksiyonu ve Tekrar Saldırıları gibi aktif siber tehditlerin varlığı; standartlarda belirtilen minimum güvenlik gereksinimlerinin aşılamaması[cite: 89, 178, 185]. |

---

## 💡 Savunma ve Yenilikçi Yaklaşım

Projemiz, CAN-Bus güvenliğini de kapsayan üç katmanlı bir savunma mimarisi üzerine inşa edilecektir:

1.  [cite_start]**Güvenlik Protokolü Katmanı:** OCPP iletişim kanalının **Mutual TLS** ile korunması ve `SignedMeterValues` gibi özelliklerin kullanılması[cite: 315, 316].
2.  [cite_start]**Anomali Tespit Katmanı (AI/ML):** Enerji tüketim desenlerini, ID frekanslarını ve zaman serisi verilerini analiz ederek anormal davranışları (`Time Desync`) $\ge 95\%$ doğrulukla tespit etme[cite: 102, 113].
3.  [cite_start]**Blokzincir Tabanlı Bütünlük Katmanı:** Kritik CAN mesajlarının veya OCPP verilerinin hashlenerek blokzincire kaydedilmesi, böylece mesaj kaynağı, zaman damgası ve bütünlüğünün değiştirilemez biçimde doğrulanması[cite: 161, 166].
