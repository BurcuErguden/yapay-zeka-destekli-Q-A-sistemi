import random
import datetime

ip_adresleri = ['192.168.1.1', '192.168.1.2', '192.168.1.3']
http_kodlari = [200, 404, 500]

def log_verisi_olusturma():
    ip = random.choice(ip_adresleri)
    zaman_gostergesi = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S %z')
    metod = random.choice(['GET', 'POST'])
    url = random.choice(['/index.html', '/about.html'])
    durum = random.choice(http_kodlari)
    cevap_boyutu = random.randint(100, 2000)
    referer = 'http://example.com'
    tarayici_bilgisi = 'Chrome/90.0'
    
    return f'{ip} - - [{zaman_gostergesi}] "{metod} {url} HTTP/1.1" {durum} {cevap_boyutu} "{referer}" "{tarayici_bilgisi}"'

dosya_yolu = r"C:\Users\burcu\Desktop\yz.log"
with open(dosya_yolu, 'a') as log_dosyasi:
    for _ in range(99):
        log_girdisi = log_verisi_olusturma()
        log_dosyasi.write(log_girdisi + '\n')

print(f'Log Dosyası {dosya_yolu} oluşturuldu.')
