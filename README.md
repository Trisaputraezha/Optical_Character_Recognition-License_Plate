# Indonesian License Plate OCR with LLaVA Vision Language Model

Nama : Ezha Tri Saputra
NIM  : 4222201026

Proyek ini mengimplementasikan sistem Optical Character Recognition (OCR) untuk plat nomor kendaraan Indonesia menggunakan model LLaVA (Large Language and Vision Assistant) melalui LMStudio.

## 📁 Struktur Proyek

```
Optical_Character_Recognition-License_Plate/
├── .ipynb_checkpoints/
├── Indonesian_LPR_Dataset/           # Dataset hasil ekstraksi
│   ├── images/
│   │   ├── train/
│   │   ├── test/
│   │   └── val/
│   ├── labels/
│   │   ├── train/
│   │   ├── test/
│   │   └── val/
│   └── merged/                       # Hasil penggabungan
│       ├── train/                    # .jpg + .txt files
│       ├── test/                     # .jpg + .txt files
│       └── val/                      # .jpg + .txt files
├── File-path.ipynb                   # Script ekstraksi dan merge dataset
├── Generate_Ground_Truth_csv.py      # Generator ground truth dari .txt files
├── ground_truth_new.csv             # Ground truth dalam format CSV
├── ocr-illava-main.py               # Script utama OCR menggunakan LLaVA
├── results.csv                      # Hasil OCR dengan evaluasi CER
├── README.md                        # Dokumentasi proyek
└── Indonesian License Plate Recognition Dataset.zip  # Dataset asli
```

## 🚀 Workflow Penggunaan

### 1. Persiapan Dataset
Download dataset asli pada : Link	download	dataset:	https://www.kaggle.com/datasets/juanthomaswijaya/indonesian
license-plate-dataset		

#### Step 1: Ekstraksi Dataset
```bash
# Jalankan File-path.ipynb untuk:
# 1. Ekstraksi zip file ke folder Indonesian_LPR_Dataset
# 2. Merge images dan labels ke folder merged/
```

Dataset akan diekstrak dengan struktur:
- `merged/train/` - File training (.jpg + .txt)
- `merged/test/` - File testing (.jpg + .txt) 
- `merged/val/` - File validasi (.jpg + .txt)

#### Step 2: Generate Ground Truth CSV
```bash
python Generate_Ground_Truth_csv.py
```
Script ini akan:
- Membaca semua file `.txt` dari folder `merged/test/`
- Mengekstrak ground truth label plat nomor
- Menyimpan ke `ground_truth_new.csv`

### 2. Setup LMStudio

#### Download & Install LMStudio
1. Download LMStudio dari: https://lmstudio.ai/
2. Install sesuai OS Anda

#### Download Model LLaVA
1. Buka LMStudio → Tab "Discover"
2. Search "llava" 
3. Download salah satu model:
   - `llava-v1.6-vicuna-7b-gguf` (Recommended)
   - `llava-v1.5-7b-gguf`
   - `bakllava-1-gguf`

#### Start LMStudio Server
1. Go to "Chat" tab → Load model LLaVA
2. Go to "Local Server" tab 
3. Click "Start Server"
4. Pastikan running di `localhost:1234`

### 3. Menjalankan OCR

```bash
python ocr-illava-main.py
```

Script akan:
- Memproses semua gambar di `merged/test/`
- Mengirim ke LLaVA model via LMStudio API
- Menggunakan prompt: *"What is the license plate number shown in this image? Respond only with the plate number."*
- Menghitung Character Error Rate (CER)
- Menyimpan hasil ke `results.csv`

## 📊 Format Output

### results.csv
```csv
image,ground_truth,prediction,CER_score
test001_1.jpg,B1234XYZ,B1234XYZ,0.0000
test002_1.jpg,D5678ABC,D5678AB,0.1250
...
```

### Kolom Penjelasan:
- **image**: Nama file gambar
- **ground_truth**: Label sebenarnya dari file .txt
- **prediction**: Hasil prediksi dari model LLaVA
- **CER_score**: Character Error Rate (0.0 = perfect, 1.0 = completely wrong)

## 🧮 Metrik Evaluasi

### Character Error Rate (CER)

**Rumus:**
```
CER = (S + D + I) / N
```

**Dimana:**
- **S** = Substitutions (karakter salah)
- **D** = Deletions (karakter dihapus)  
- **I** = Insertions (karakter disisipkan)
- **N** = Jumlah karakter ground truth

**Implementasi:**
```
CER = Edit Distance / Ground Truth Length
```

**Contoh Perhitungan:**

1. **Perfect Match:**
   ```
   Ground Truth: "B1234XYZ"
   Prediction:   "B1234XYZ"
   CER = 0/8 = 0.0000 ✅
   ```

2. **Single Error:**
   ```
   Ground Truth: "B1234XYZ" 
   Prediction:   "B1234XY"   (Z missing)
   CER = 1/8 = 0.1250
   ```

3. **Multiple Errors:**
   ```
   Ground Truth: "D5678ABC"
   Prediction:   "D567ABC"   (8 missing)
   CER = 1/8 = 0.1250
   ```

## 🛠️ Persyaratan Sistem

### Software
- Python 3.8+
- LMStudio dengan model LLaVA
- Jupyter Notebook (untuk File-path.ipynb)

### Python Dependencies
```bash
pip install requests pandas pillow python-Levenshtein pathlib
```

## 📝 Cara Menggunakan

### Langkah Lengkap:

1. **Extract Dataset:**
   ```bash
   jupyter notebook File-path.ipynb
   # Jalankan semua cell untuk ekstraksi dan merge
   ```

2. **Generate Ground Truth:**
   ```bash
   python Generate_Ground_Truth_csv.py
   ```

3. **Start LMStudio:**
   - Load model LLaVA
   - Start server di localhost:1234

4. **Run OCR:**
   ```bash
   python ocr-illava-main.py
   ```

5. **Check Results:**
   - Lihat `results.csv` untuk hasil lengkap
   - Analisis performa menggunakan CER scores

## 🎯 Expected Results

Sistem ini dirancang untuk:
- **Akurasi tinggi** pada plat nomor Indonesia yang jelas
- **Robust handling** untuk berbagai kondisi pencahayaan
- **Detailed evaluation** dengan metrik CER
- **Comprehensive logging** untuk debugging

## 📈 Format Dataset
### [results.csv](results.csv)
| Image ID | OCR Output | Ground Truth | CER Score |

### File .txt (Label Format):
```
B1234XYZ
```

### Indonesian License Plate Patterns:
- Standard: `B1234XYZ` (1 huruf + 1-4 digit + 1-3 huruf)
- Jakarta: `B1234ABC`
- Regional variations: `AA1234XYZ`

## 🔧 Troubleshooting

### Common Issues:

1. **LMStudio Connection Error:**
   ```
   Error: Connection refused to localhost:1234
   ```
   **Solution:** Pastikan LMStudio server running dan model loaded

2. **Dataset Path Error:**
   ```
   FileNotFoundError: merged/test/ not found
   ```
   **Solution:** Jalankan File-path.ipynb terlebih dahulu

3. **Ground Truth Missing:**
   ```
   Error: ground_truth_new.csv not found
   ```
   **Solution:** Jalankan Generate_Ground_Truth_csv.py

4. **Model Response Error:**
   ```
   Error: Model returned empty response
   ```
   **Solution:** Cek model LLaVA sudah loaded dengan benar

## 📊 Performance Analysis

Setelah menjalankan OCR, analisis performa meliputi:
- **Overall Accuracy** (% perfect matches)
- **Mean CER Score** 
- **CER Distribution** by quality categories
- **Error Patterns** analysis
- **Performance by plate format**

## 👨‍💻 Author

Dibuat untuk memenuhi tugas mata kuliah Computer Vision (RE604) - Teknik Robotika

---

## 📝 Notes

- Dataset menggunakan Indonesian License Plate Recognition Dataset dari Kaggle
- Model LLaVA memberikan hasil terbaik untuk plat nomor yang jelas dan kontras tinggi
- Preprocessing gambar dapat meningkatkan akurasi untuk gambar berkualitas rendah
- CER threshold 0.2 umumnya menunjukkan hasil yang dapat diterima untuk aplikasi praktis