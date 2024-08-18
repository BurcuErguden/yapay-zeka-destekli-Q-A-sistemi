import pandas as pd
import re
import matplotlib.pyplot as plt

dosya_yolu = r"C:\Users\burcu\Desktop\yz.log"

veri = []
with open(dosya_yolu, 'r') as file:
    for line in file:
        # Regex deseni
        pattern = r'(?P<ip>[\d\.]+) - - \[(?P<zamandamgasi>[^\]]+)\] "(?P<metod>[A-Z]+) (?P<url>[^ ]+) HTTP/[^"]+" (?P<durum_kodu>\d+) (?P<boyut>\d+) "(?P<sayfa>[^"]+)" "(?P<tarayici>[^"]+)"'
        match = re.match(pattern, line)
        if match:
            veri.append(match.groupdict())
df = pd.DataFrame(veri)

# Durum kodları ve yanıt boyutlarını sayısal verilere dönüştürüyoruz
df['durum_kodu'] = pd.to_numeric(df['durum_kodu'], errors='coerce')
df['boyut'] = pd.to_numeric(df['boyut'], errors='coerce')

# Tarih ve saat sütununu tarih formatına dönüştürüyoruz
df['zamandamgasi'] = pd.to_datetime(df['zamandamgasi'], format='%d/%b/%Y:%H:%M:%S')

# Zaman damgalarını indeks olarak ayarlıyoruz
df.set_index('zamandamgasi', inplace=True)

# saate göre ayarlama
unique_hours = df.index.floor('h').unique()
hourly_requests = df.groupby(df.index.floor('h')).size()
print("Saat bazında istekler:")
print(hourly_requests)

# Her IP'nin en çok erişilen URL'sini hesaplayalım
en_cok_erisilen_url = df.groupby('ip')['url'].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown')

# IP bazında en sık erişilen URL'yi DataFrame'e ekle
df['en_cok_erişilen_url'] = df['ip'].map(en_cok_erisilen_url)

# IP bazında özet istatistikler
ozellikler = df.groupby('ip').agg({
    'url': 'count',  # İstek sayısı
    'durum_kodu': lambda x: x.value_counts().index[0] if not x.value_counts().empty else 'Unknown',  # En sık görülen durum kodu
    'metod': lambda x: x.value_counts().index[0] if not x.value_counts().empty else 'Unknown',  # En sık kullanılan metod
    'boyut': 'mean', 
    'en_cok_erişilen_url': lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown'  # En sık erişilen URL
}).rename(columns={
    'url': 'istek_sayisi',
    'boyut': 'ortalama_boyut'
})

print("Özellikler:")
print(ozellikler)

# HTTP durum kodları dağılımını görselleştirme
df['durum_kodu'].value_counts().plot(kind='bar')
plt.xlabel('HTTP Durum Kodu')
plt.ylabel('Frekans')
plt.title('HTTP Durum Kodları Dağılımı')
plt.show()

# URL'leri sayalım
url_sayilari = df['url'].value_counts()

# URL'leri görselleştirelim
plt.figure(figsize=(10, 6))
url_sayilari.plot(kind='bar', color='yellow')
plt.title('URL Dağılımı')
plt.xlabel('URL')
plt.ylabel('Frekans')
plt.xticks(rotation=45, ha='right')
plt.show()


# Her IP için vektör özellikleri çıkarma (örnek: istek sayısı, en çok erişilen sayfa, en çok erişilen zaman dilimi)
df['saat'] = df.index.hour
ip_vektör = df.groupby('ip').agg({
    'url': 'count', 
    'boyut': 'mean', 
    'saat': lambda x: x.mode().iloc[0]  # En sık erişilen saat
})


vektör = []
for ip, row in ip_vektör.iterrows():
    vektör.append({
        'id': ip, 
        'values': row.tolist()
    })

print(vektör)
