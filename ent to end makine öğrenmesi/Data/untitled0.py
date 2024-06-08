import pandas as pd

# CSV dosyasını oku
df = pd.read_csv("robot-fill-training.csv")

# Marka ismini çıkarmak için bir fonksiyon
def markayi_cikar(url):
    # URL'yi "/" karakterine göre ayır
    parcalar = url.split('/')
    
    # Markanın bulunduğu indeksin belirlenmesi (5. slash sonrası)
    marka_index = 4
    
    # Marka indeksinden sonraki parçayı al
    marka = parcalar[marka_index]
    
    return marka

# "Marka" sütununu oluştur
df['Marka'] = df['url'].apply(markayi_cikar)

# Güncellenmiş veriyi yeni bir CSV dosyasına kaydet
df.to_csv('robot-fill-training2.csv', index=False)
