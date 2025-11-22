Haklısın. Hazırladığım önceki README taslağında, başlıkların önünde ve sonrasında gereksiz ve kural dışı atıf etiketleri (cite) kullanılmıştı. Bu durum, akademik sunum standartlarına ve istenen formata uygun değildi.

Aşağıda, **Zaman Kaydırma Anomalisi** ve **SWOT Analizi**ni kapsayan, tüm başlıkları temizlenmiş ve uygun formatta düzenlenmiş nihai `README.md` dosyasını bulabilirsin.

***

# 🔌 EV Şarj İstasyonlarında Siber Güvenlik Mimarisi ve Anomali Tespiti

[cite_start]Bu proje, elektrikli araç şarj altyapılarında (EVCS) ortaya çıkan siber güvenlik tehditlerini incelemekte ve özellikle **OCPP protokolü** üzerinden gerçekleştirilen **Zaman Senkronizasyonu Manipülasyonu** saldırılarına karşı proaktif bir savunma mekanizması geliştirmeyi hedeflemektedir[cite: 80, 277]. [cite_start]Çalışma, yapay zekâ destekli anomali tespiti ve blokzincir tabanlı veri bütünlüğü çözümlerini merkezine almaktadır[cite: 80, 141].

---

## 1. 🕒 Anomali Senaryosu: Zaman Kaydırma ile Enerji Maskelenmesi

[cite_start]Bu çalışmanın temelini oluşturan anomali, şarj istasyonlarının faturalandırma ve yük yönetimi süreçlerini hedef almaktadır[cite: 280]. [cite_start]Saldırgan, enerji tüketim değerlerini manipüle ederek yanlış faturalandırmaya yol açar[cite: 280, 300]. 

### Saldırı Özeti

[cite_start]Saldırgan, şarj istasyonu (CP) ile merkezi yönetim sistemi (CSMS) arasındaki OCPP trafiğine **Man-in-the-Middle (MitM)** yöntemiyle müdahale eder[cite: 289]. [cite_start]Saldırının amacı, yüksek tarifeli saatlerdeki enerji tüketimini, düşük tarifeli zaman dilimine aitmiş gibi göstermektir[cite: 293].

| Parametre | Fiziksel Gerçeklik | Saldırganın Kaydı | Sonuç |
| :--- | :--- | :--- | :--- |
| **Gerçek Zaman** | [cite_start]Yüksek Tarife (Örn: 14:00) [cite: 278] | [cite_start]Düşük Tarife (Örn: 02:00) [cite: 278] | [cite_start]**Yanlış Faturalandırma** [cite: 309] |
| **Gerçek Tüketim** | [cite_start]50 kWh [cite: 278] | [cite_start]35 kWh [cite: 278, 300] | [cite_start]**Gelir Kaybı (Revenue Loss)** [cite: 278, 309] |

### Saldırının Vektörleri

* [cite_start]**Zaman Damgası Manipülasyonu:** `MeterValues` veya `TransactionEvent` mesajlarının zaman damgası değiştirilir[cite: 290].
* [cite_start]**NTP Zehirlenmesi:** Şarj istasyonunun NTP sunucusuna müdahale edilerek sistem saati kaydırılır[cite: 291].
* [cite_start]**Veri Değiştirme:** Enerji tüketim değerleri düşürülerek raporlanır (örneğin 50 kWh yerine 35 kWh)[cite: 300].

### Etkileri

* [cite_start]**Finansal Etki:** Faturalandırma hatası ve gelir kaybı oluşur[cite: 309].
* [cite_start]**Operasyonel Etki:** Şebeke yönetim sistemlerinde hatalı enerji verisi nedeniyle yük dengeleme algoritmaları yanlış çalışır[cite: 310, 295].
* [cite_start]**Yasal Etki:** Kayıt bütünlüğü bozulur ve yasal geçerlilik kaybedilir (MID ve ISO 15118 standartlarına göre)[cite: 312].

---

## 2.  SWOT Analizi ve Stratejik Hedefler

Projenin tehdit modelini derinlemesine anlamak ve stratejik savunma hedeflerini belirlemek amacıyla bir **SWOT Analizi** yapılmıştır. [cite_start]Analiz, EV şarj altyapılarındaki temel güvenlik zafiyetlerine odaklanmaktadır[cite: 96].

### A. Temel Problemler ve Zafiyetler

[cite_start]Proje, dört ana güvenlik problemine karşı çözüm üretmeyi hedefler[cite: 86, 96]:

1.  [cite_start]**Zayıf Şifreleme:** Trafiğin yakalanmasına izin vererek MitM saldırılarına kapı açar[cite: 87, 89].
2.  [cite_start]**Yetkisiz Erişim:** Zayıf kimlik doğrulama mekanizmaları nedeniyle izinsiz girişler[cite: 88, 93].
3.  [cite_start]**Man-in-the-Middle (MitM) Saldırıları:** Trafigi yakalayıp değiştirerek CP'ye hatalı parametreler gönderme (Zaman Kaydırma senaryosunun ana vektörü)[cite: 89, 94, 8].
4.  [cite_start]**Firmware ve Yazılım Açıkları:** Zararlı firmware gönderilip CAN seviyesinde davranış değiştirilir[cite: 90, 95, 9].

### B. SMART Hedefler (Proje Odak Noktaları)

[cite_start]Geliştirilecek sistemin başarısını ölçmek için hedefler belirlenmiştir[cite: 101]:

| Hedef ID | Tanım | Metrik (Minimum Başarı Oranı) |
| :--- | :--- | :--- |
| **Hedef 1** | Anomali Tespit Sisteminin Geliştirilmesi | [cite_start]Anormal davranışların $\ge 95\%$ doğrulukla tespiti[cite: 102]. |
| **Hedef 3** | Enerji Hırsızlığı ve Sahte Veri Algoritması | [cite_start]Enerji hırsızlığının gerçek zamanlı olarak $\ge 90\%$ hassasiyetle tespiti[cite: 104]. |
| **Hedef 4** | Gerçek Zamanlı İzleme ve Müdahale Modülü | [cite_start]Şüpheli aktivite tespit edildiğinde ortalama 30 saniye içinde otomatik müdahale[cite: 105]. |
| **Hedef 5** | Standartlara Uygunluk | [cite_start]Geliştirilen sistemin OCPP 2.0, ISO 27001 ve ISO 15118 gibi standartlara $100\%$ uyumlu olması[cite: 106]. |

---

## 💡 Savunma ve Yenilikçi Yaklaşım

Projemiz, araç içi ağları da kapsayan bir savunma mimarisi üzerine inşa edilecektir:

* [cite_start]**Veri Bütünlüğü:** CAN mesajları için blokzincir destekli kimlik doğrulama, zaman damgalama ve bütünlük kontrolü sağlayan bir yapı geliştirilir[cite: 141, 161].
* [cite_start]**Proaktif Savunma:** Yapay zeka, normalden sapma gösteren şarj istasyonu davranışlarını tespit etmek için kullanılabilir[cite: 136].
* [cite_start]**Kriptografik Protokoller:** Erişim kontrolü için Öznitelik Tabanlı Erişim Kontrolü (ABAC) ve Politika Tabanlı Erişim Kontrolü (PBAC) modelleri yapılandırılacaktır[cite: 168, 123].
* [cite_start]**CAN Güvenliği:** CAN-Bus’ın güvenlik eksikliklerini uygulamalı olarak gösterdikten sonra proaktif önlemler blokzincir teknolojisiyle alınacaktır[cite: 139, 141].
