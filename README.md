# ECG Multimodal Fusion — Replikasi dan Metode Pembanding

Proyek ini merupakan tugas Digital Signal Processing (PSD) untuk mereplikasi metode klasifikasi detak jantung ECG dari sebuah paper, kemudian menguji metode pembanding dan memilih metode yang memberikan peningkatan pada minimal satu metrik evaluasi.

## Ringkasan Proyek

Alur penelitian:

1. Replikasi metode referensi sebagai baseline.
2. Eksperimen beberapa metode pembanding.
3. Membandingkan hasil eksperimen.
4. Memilih metode pembanding yang memberikan peningkatan minimal pada satu parameter.
5. Menyusun analisis dan artikel ilmiah berbasis hasil eksperimen.

### Baseline

Model baseline yang digunakan:

**ResNet18 + Gramian Angular Field (GAF)**

| Metrik | Hasil |
|---|---:|
| Accuracy | 98.86% |
| Macro Precision | 95.23% |
| Macro Recall | 91.97% |
| Macro F1 | 93.53% |

### Metode Pembanding Terpilih

**CBAM-ResNet18 + Gramian Angular Summation Field (GASF)**

Hasil evaluasi test:

| Metrik | ResNet18 + GAF | CBAM-ResNet18 + GASF | Selisih |
|---|---:|---:|---:|
| Accuracy | 98.86% | 98.4652% | -0.3948 pp |
| Macro Precision | 95.23% | 89.6226% | -5.6074 pp |
| **Macro Recall** | **91.97%** | **92.1795%** | **+0.2095 pp** |
| Macro F1 | 93.53% | 90.5251% | -3.0049 pp |

Dengan demikian, CBAM-ResNet18 + GASF memberikan peningkatan pada **Macro Recall sebesar 0.2095 percentage point** dibandingkan baseline.

> Catatan metodologis: hasil CBAM-ResNet18 + GASF merupakan metode pembanding yang terinspirasi dari literatur, bukan reproduksi exact paper kedua. Eksperimen menggunakan dataset heartbeat-level 187 titik yang digunakan pada proyek. Checkpoint yang dievaluasi berasal dari epoch 5.

---

## Dataset

Dataset utama yang digunakan adalah **ECG Heartbeat Categorization Dataset** berbasis MIT-BIH.

### Sumber

Kaggle:  
https://www.kaggle.com/datasets/shayanfazeli/heartbeat

Paper baseline:  
**ECG Heartbeat Classification Using Multimodal Fusion**

IEEE:  
https://ieeexplore.ieee.org/document/9486862

DOI:  
`10.1109/ACCESS.2021.3097614`

Repository referensi:  
https://github.com/zaamad/ECG-Heartbeat-Classification-Using-Multimodal-Fusion

### Format Dataset

Setiap sampel memiliki:

- 187 titik sinyal ECG
- 1 label kelas
- 5 kelas arrhythmia:

| Label | Kelas |
|---:|---|
| 0 | N |
| 1 | S |
| 2 | V |
| 3 | F |
| 4 | Q |

Ukuran data:

```text
Train: 87,554 × 187
Test : 21,892 × 187
```

Distribusi train:

```text
N = 72,471
S =  2,223
V =  5,788
F =    641
Q =  6,431
```

Distribusi test:

```text
N = 18,118
S =    556
V =  1,448
F =    162
Q =  1,608
```

Dataset asli tidak disimpan di repository GitHub karena ukuran file besar. Dataset dapat diunduh langsung dari sumber Kaggle di atas.

---

## Metode

### 1. Baseline — ResNet18 + GAF

Pipeline baseline:

```text
ECG 187 titik
      ↓
Gramian Angular Field (GAF)
      ↓
Resize 224 × 224
      ↓
ResNet18
      ↓
5 kelas
```

Konfigurasi utama baseline:

- ResNet18 pretrained ImageNet
- Input 224 × 224
- Layer3 dan Layer4 di-unfreeze
- Fully connected: `512 → 256 → 128 → 5`
- Class weights: `[1, 2, 1, 2, 1]`
- Optimizer: Adam
- Betas: `(0.5, 0.999)`
- ExponentialLR: `gamma=0.95`
- Batch size: 64

### 2. Metode Pembanding — CBAM-ResNet18 + GASF

Pipeline:

```text
ECG 187 titik
      ↓
GASF (summation)
      ↓
Resize 224 × 224
      ↓
CBAM-ResNet18
      ↓
5 kelas
```

CBAM terdiri dari:

- Channel Attention
- Spatial Attention

Eksperimen pembanding menggunakan konfigurasi training yang sedekat mungkin dengan baseline.

Catatan penting:

- CWGAN-GP dari paper referensi CBAM tidak digunakan.
- Dataset tetap menggunakan heartbeat-level 187 titik milik proyek.
- Checkpoint kandidat dipilih berdasarkan validation Macro Recall.
- Test set digunakan pada tahap evaluasi akhir.

---

## Eksperimen Pembanding Lain

Beberapa metode lain diuji atau disaring selama penelitian.

### MobileNetV3-Small + GAF

Hasil Week 2:

- Accuracy: 98.63%
- Macro F1: 92.11%

Tidak mengungguli baseline.

### 1D CNN + Raw ECG

Hasil Week 2:

- Accuracy: 97.61%
- Macro F1: 88.64%

Tidak mengungguli baseline.

### ECGTransForm

Metode ini diuji secara terpisah, tetapi tidak mengungguli baseline pada eksperimen proyek.

### KAN

Pilot KAN 10 epoch menghasilkan validation Macro F1 sekitar 84.90%, sehingga tidak dilanjutkan ke full training.

### CAT-Net dan kandidat lainnya

Beberapa kandidat berbasis literatur disaring berdasarkan kompatibilitas dataset dan hasil eksperimen. Kandidat yang tidak memenuhi tujuan proyek tidak dilanjutkan.

---

## Struktur Repository

Struktur yang direkomendasikan:

```text
ECG-Multimodal-Fusion/
├── README.md
├── requirements.txt
├── .gitignore
│
├── notebooks/
│   ├── 01_replikasi.ipynb
│   ├── 02_pembanding.ipynb
│   ├── 03_hasil_analisis.ipynb
│   ├── 04_audit_ecgtransform.ipynb
│   ├── 05_train_ecgtransform.ipynb
│   ├── 08_kan_pilot.ipynb
│   └── 09_cbam_gasf_pilot_recall_selection.ipynb
│
├── outputs/
│   ├── figures/
│   └── results/
│
├── scripts/
│   └── ...
│
├── configs/
│   └── ...
│
└── docs/
    └── experiment_log.md
```

File besar seperti dataset, HDF5, dan checkpoint tidak disimpan di GitHub.

---

## Artefak Besar

Karena ukuran dataset dan beberapa artefak eksperimen besar, file-file berikut disimpan di storage terpisah:

- dataset asli
- file `.npy` berukuran besar
- HDF5 GAF/RP/MTF
- checkpoint model
- artefak preprocessing besar

Google Drive artefak:

**[ISI LINK GOOGLE DRIVE DI SINI]**

Repository GitHub:

**[ISI LINK REPOSITORY GITHUB DI SINI]**

---

## Reproduksi Eksperimen

### 1. Siapkan environment

Gunakan Python dan dependency yang tercantum di:

```text
requirements.txt
```

### 2. Siapkan dataset

Unduh dataset dari Kaggle:

https://www.kaggle.com/datasets/shayanfazeli/heartbeat

Letakkan file yang diperlukan sesuai struktur project.

Contoh:

```text
data/
└── mitbih_train.csv

features/
├── X_test.npy
└── y_test.npy
```

### 3. Jalankan notebook

Baseline:

```text
notebooks/01_replikasi.ipynb
```

Eksperimen pembanding:

```text
notebooks/02_pembanding.ipynb
```

Analisis:

```text
notebooks/03_hasil_analisis.ipynb
```

CBAM-ResNet18 + GASF:

```text
notebooks/09_cbam_gasf_pilot_recall_selection.ipynb
```

### 4. Evaluasi

Metrik utama:

- Accuracy
- Macro Precision
- Macro Recall
- Macro F1

Evaluasi tambahan:

- Confusion matrix
- Classification report
- Per-class recall
- Learning curve
- Parameter count
- Inference time

---

## Reproducibility dan Catatan Metodologis

Beberapa hasil eksperimen memiliki keterbatasan metodologis:

1. Baseline Week 1 memilih checkpoint berdasarkan performa test, sehingga hasil baseline bersifat optimistik dibandingkan protokol yang memilih checkpoint berdasarkan validation.
2. Baseline menggunakan SMOTE, sedangkan eksperimen CBAM-ResNet18 + GASF menggunakan train/validation split dari data raw dan class-weighted loss.
3. Oleh karena itu, perbandingan kedua model tidak sepenuhnya merupakan controlled comparison.
4. CBAM-ResNet18 + GASF dipilih sebagai metode pembanding karena menghasilkan Macro Recall test yang lebih tinggi daripada baseline.
5. Peningkatan Macro Recall tidak berarti CBAM-ResNet18 + GASF lebih baik pada seluruh metrik.

---

## Hasil Utama

Temuan utama proyek:

```text
Baseline:
ResNet18 + GAF
Macro Recall = 91.97%

Pembanding:
CBAM-ResNet18 + GASF
Macro Recall = 92.1795%

Improvement = +0.2095 percentage point
```

Metode pembanding memiliki Accuracy, Macro Precision, dan Macro F1 yang lebih rendah daripada baseline. Karena itu, kesimpulan penelitian dibatasi pada peningkatan Macro Recall, bukan peningkatan performa secara keseluruhan.

---

## Artikel

Draft artikel Week 4 menggunakan format IMRaD dan membahas:

- Pendahuluan
- Metode
- Hasil dan Diskusi
- Kesimpulan
- Keterbatasan dan pekerjaan lanjutan
- Reproducibility dan artefak eksperimen

Simpan artikel pada folder:

```text
docs/
```

---

## Lisensi dan Referensi

Proyek ini dibuat untuk keperluan akademik.

Referensi utama:

1. *ECG Heartbeat Classification Using Multimodal Fusion*. IEEE Access. DOI: `10.1109/ACCESS.2021.3097614`
2. Ma, K., Zhan, C. A., & Yang, F. (2022). *Multi-classification of arrhythmias using ResNet with CBAM on CWGAN-GP augmented ECG Gramian Angular Summation Field*. Biomedical Signal Processing and Control, 77, 103684. DOI: `10.1016/j.bspc.2022.103684`
3. Cui, H., et al. (2025). *ECG Signal Classification Using Interpretable KAN: Towards Predictive Diagnosis of Arrhythmias*. Algorithms, 18(2), 90. DOI: `10.3390/a18020090`

---

## Disclaimer

Hasil yang terdapat di repository ini adalah hasil eksperimen proyek dan tidak dimaksudkan sebagai klaim bahwa metode pembanding secara umum lebih unggul daripada baseline.

Peningkatan yang diperoleh pada eksperimen ini hanya terlihat pada **Macro Recall**, pada konfigurasi dan dataset yang digunakan.
