# TGSS 2024 — Grafik Paneli

Türkiye Genel Sosyal Saha Araştırması 2024 (n = 2.615) verisinden otomatik grafik üreten Python projesi. Streamlit arayüzü üzerinden grafikleri oluşturup görüntüleyebilirsiniz.

## Gereksinimler

| Gereksinim | Minimum sürüm |
|------------|---------------|
| Python | 3.10 veya üzeri (3.11 önerilir) |
| pip | Güncel sürüm |
| Git | Repoyu klonlamak için |

İnternet bağlantısı ilk kurulumda paket indirmek için gerekir.

## Proje yapısı

```
Simple-Chart-Plotter/
├── app.py                  # Streamlit web arayüzü
├── main.py                 # Grafik üretim mantığı
├── SimpleChartPlotter.py   # Grafik sınıfı (matplotlib)
├── data/
│   └── TGSS2024.csv        # Anket verisi (repo ile gelir)
├── outputs/                # Oluşturulan PNG'ler (otomatik oluşur)
├── requirements.txt
└── README.md
```

## Kurulum (sıfırdan)

### 1. Repoyu klonlayın

```bash
git clone https://github.com/KaanCan1/Simple-Chart-Plotter.git
cd Simple-Chart-Plotter
```

### 2. Sanal ortam oluşturun

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Sanal ortam aktifken terminalde `(.venv)` öneki görünür.

### 3. Bağımlılıkları yükleyin

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Yüklenen ana paketler: `streamlit`, `matplotlib`, `seaborn`, `pandas`, `numpy`, `scipy`, `pillow`.

### 4. Veri dosyasını kontrol edin

`data/TGSS2024.csv` dosyasının mevcut olduğundan emin olun. Bu dosya olmadan grafik üretilemez.

## Çalıştırma

### Web arayüzü (önerilen)

Proje klasöründeyken, sanal ortam **aktif** iken:

```bash
streamlit run app.py
```

Tarayıcıda otomatik açılır (genelde `http://localhost:8501`). Açılmazsa bu adresi elle girin.

Arayüzde **⟳ Grafikleri Oluştur** butonuna basın. 6 grafik `outputs/` klasörüne kaydedilir ve sayfada gösterilir.

- İlk çalıştırmada matplotlib font önbelleği kurulabilir; bu normaldir ve bir kez olur.
- Sonraki üretimler genelde birkaç saniye sürer.

### Sadece terminalden grafik üretmek

Streamlit olmadan doğrudan PNG oluşturmak için:

```bash
python main.py
```

Çıktılar: `outputs/line.png`, `bar.png`, `scatter.png`, `pie.png`, `histogram.png`, `dashboard.png`.

## Üretilen grafikler

| Dosya | Açıklama |
|-------|----------|
| `line.png` | Yaş grubuna göre mutluluk, memnuniyet, sağlık |
| `bar.png` | Toplumsal tehdit algısı ortalamaları |
| `scatter.png` | Sosyal güven × yaşam memnuniyeti (cinsiyet) |
| `pie.png` | Medeni durum dağılımı |
| `histogram.png` | Katılımcı yaş dağılımı |
| `dashboard.png` | Üç panelli genel bakış |

## Sık karşılaşılan sorunlar

### `ModuleNotFoundError` (streamlit, pandas, scipy vb.)

Sanal ortamı aktive etmeden komut çalıştırıyorsunuzdur. Her oturumda:

```bash
source .venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
```

### Grafikler çok yavaş oluşuyor

- Komutları **sanal ortam içinde** çalıştırın; sistem `python3` ile karıştırmayın.
- `streamlit run app.py` kullanın; her seferinde yeni process açan eski yöntemlerden kaçının.
- İlk çalıştırmadan sonra `.mpl_cache/` oluşur; ikinci üretimler hızlanır.

### `FileNotFoundError: data/TGSS2024.csv`

Komutu proje kök klasöründen çalıştırın:

```bash
cd Simple-Chart-Plotter
streamlit run app.py
```

### Port zaten kullanımda

Farklı port ile başlatın:

```bash
streamlit run app.py --server.port 8502
```

## Geliştirme notları

- Grafik motoru: `matplotlib` (`Agg` backend, dosyaya kayıt).
- Arayüz: `Streamlit`.
- `outputs/` ve `.mpl_cache/` git’e dahil değildir; çalışma sırasında oluşur.

## Lisans

Bu proje eğitim / demo amaçlıdır. TGSS verisinin kullanım koşulları veri sahibine aittir.
