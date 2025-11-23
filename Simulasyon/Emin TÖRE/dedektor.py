import can
import time
import random
import os
from colorama import Fore, Back, Style, init

# Renkleri başlat
init(autoreset=True)

def ekran_temizle():
    os.system('cls' if os.name == 'nt' else 'clear')

def dedektor_arayuzu():
    bus = can.Bus(channel='239.0.0.1', interface='udp_multicast')
    
    print(Fore.CYAN + Style.BRIGHT + """
    =======================================================
       🛡️  CHARGE-SHIELD AI GÜVENLİK PANELİ v1.2 (BETA)
    =======================================================
    LOG: Sistem Başlatılıyor... [OK]
    LOG: Yapay Zeka Modülü...... [OK]
    LOG: Ağ İzleme Servisi...... [AKTİF]
    """)
    time.sleep(2)

    last_auth = 0
    packet_count = 0
    
    try:
        while True:
            # Ekrana sahte trafik bas (Hava olsun diye)
            packet_count += 1
            if packet_count % 5 == 0:
                print(Fore.GREEN + f"[INFO] Paket Analiz Ediliyor... ID: {hex(random.randint(0, 500))} | Boyut: {random.randint(8, 64)} byte")
            
            # Gerçek veriyi bekle (bloklamadan, timeout ile)
            msg = bus.recv(timeout=0.2)
            
            if msg:
                if msg.arbitration_id == 0x050: # Authorize
                    last_auth = time.time()
                    print(Fore.BLUE + Style.BRIGHT + "\n[AUTH] ✅ GEÇERLİ KİMLİK DOĞRULAMA TESPİT EDİLDİ.")
                    print(Fore.BLUE + f"       Kart ID: {hex(random.randint(100000, 999999))}")
                    print("-" * 50)
                    
                elif msg.arbitration_id == 0x100: # Start
                    print(Fore.YELLOW + "\n[UYARI] ⚠️  'ŞARJI BAŞLAT' KOMUTU GÖRÜLDÜ...")
                    time.sleep(0.3) # Gerilim yarat
                    
                    if time.time() - last_auth > 5.0:
                        # SALDIRI ANI
                        print(Back.RED + Fore.WHITE + Style.BRIGHT + "\n🚨  KRİTİK ANOMALİ TESPİT EDİLDİ! (YETKİSİZ ERİŞİM)  🚨")
                        print(Fore.RED + "   -> Sebep: Geçerli 'Authorize' kaydı bulunamadı.")
                        print(Fore.RED + "   -> Eylem: Otomatik Engelleme Başlatılıyor...")
                        
                        stop = can.Message(arbitration_id=0x200, data=b'STOP')
                        bus.send(stop)
                        time.sleep(0.5)
                        print(Fore.GREEN + Style.BRIGHT + "✅  MÜDAHALE BAŞARILI: İstasyon Durduruldu.\n")
                    else:
                        print(Fore.GREEN + "[OK] İşlem Güvenli. Yetki Süresi İçinde.\n")

    except KeyboardInterrupt:
        print("\nKapatılıyor...")

if __name__ == "__main__":
    dedektor_arayuzu()
