# Çalıştırma rehberi

## Dosyalar hazır; yeniden çalıştırmak için

`results/` klasöründeki grafikler ve tablolar kod gerçekten çalıştırılarak üretildi. GitHub'a yüklemek için önce kendi bilgisayarına Python kurman gerekmiyor. Projeyi öğrenmek ve parametreleri denemek için aşağıdaki yollardan birini kullan.

## Seçenek 1: Google Colab

1. Projenin ZIP'ini indir. İçinden `RUN_IN_COLAB.ipynb` dosyasını çıkar.
2. https://colab.research.google.com/ adresini aç; Google hesabınla giriş yap.
3. Notebook açma penceresindeki Upload bölümüne veya File > Upload notebook seçeneğine gir ve bu `.ipynb` dosyasını seç.
4. Notebook hücrelerini yukarıdan aşağıdaki oynat düğmelerinden çalıştır.
5. ZIP yüklemeni isteyen hücrede **bu projenin ZIP dosyasını** seç. Diğer projeyi veya tüm dosyaları birleştiren paketi seçme.
6. Kurulum hücresi kütüphaneleri yükler; test hücresi kontrolleri çalıştırır; sonraki hücre programı çalıştırıp grafikleri gösterir.
7. Parametre hücresindeki sayıları değiştirebilirsin. Sonuçlar Colab oturumunda üretilir; GitHub'da kendiliğinden güncellenmez.
8. Son hücre sonuç ZIP'ini indirir. İstersen GitHub'daki sonuç dosyalarını elle güncelle.

Notebook'un Colab'a özel yükleme/indirme hücreleri bu ortamda doğrudan denenmedi; Python kodu, paket kurulumları, testler ve hesaplar yerel temiz ortamda doğrulandı. Colab menü adları dil ve arayüz sürümüne göre değişebilir.

## Seçenek 2: Bilgisayarında

64 bit Python 3.11 veya 3.12 kullan. ZIP'i çıkar; terminali `communication-node-placement-optimizer` klasörünün **içinde** aç. `main.py` dosyasını görebildiğin klasör doğru yer.

### Windows PowerShell

Python kurulu değilse https://www.python.org/downloads/ adresinden kur; kurulumda Python'u PATH'e ekleme seçeneğini işaretle.

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m unittest -v
.venv\Scripts\python.exe main.py
```

Python 3.11 kurduysan ilk komutta `-3.11` kullan. `py` bulunamıyorsa aynı ilk komutu `python -m venv .venv` olarak deneyebilirsin. Sanal ortamı aktive etmeden kendi Python'unu çağırıyoruz.

### macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest -v
.venv/bin/python main.py
```

Kurulum sırasında internet gerekiyor. Sonrasında hesaplar API anahtarı veya ücretli yapay zekâ servisi olmadan çalışır. Grafikler pencere açmak yerine `results/` klasörüne PNG olarak yazılır.

## Temel komutlar

Doğru Python ortamını seçtikten sonra:

```bash
python main.py
python -m unittest -v
python benchmark.py
```

Örnek parametre değiştirme komutları README'de. `--output-dir results/custom` kullanırsan kayıtlı varsayılan örneği korursun.

## Hata görürsem

`ModuleNotFoundError`: Kütüphaneleri, programı çalıştıran Python ile kur. Yukarıda kurulum ve çalıştırma aynı sanal ortamı kullanıyor.

`can't open file main.py`: Terminal yanlış klasörde. `main.py` bulunan proje klasörüne geç.

`Invalid` / `error`: Girdi aralığı veya fizik/model koşulu ihlal edilmiş olabilir; hata mesajındaki koşulu uygula.

Görsel pencere çıkmaması normal: `results/` içindeki PNG'yi aç. JSON deney koşullarını; CSV hesaplanan sayıları içeriyor.
