# Week 1 — Replication Notes

Catatan ini mendokumentasikan proses replikasi baseline pada **Week 1** sebagai fondasi eksperimen klasifikasi detak jantung ECG pada repository **ECG-Multimodal-Fusion**.

---

## 1. Referensi Paper & Sumber Data

| Komponen | Keterangan |
| :--- | :--- |
| **Judul Paper** | *ECG Heartbeat Classification Using Multimodal Fusion* |
| **DOI** | `10.1109/ACCESS.2021.3097614` |
| **IEEE Xplore** | https://ieeexplore.ieee.org/document/9486862 |
| **Repository Referensi** | https://github.com/zaamad/ECG-Heartbeat-Classification-Using-Multimodal-Fusion |
| **Dataset** | https://www.kaggle.com/datasets/shayanfazeli/heartbeat |

---

## 2. Konfigurasi Implementasi Baseline

Implementasi baseline direplikasi menggunakan representasi citra 2D dari sinyal ECG 1D dengan konfigurasi sebagai berikut:

- **Backbone**: `ResNet18` (*pretrained* ImageNet)
- **Input Sinyal**: ECG `187` titik
- **Transformasi Citra**: Gramian Angular Field (`GAF`)
- **Ukuran Citra Input**: `224×224`
- **Fine-Tuning Layer**: `layer3` dan `layer4` dilatih (bersama *classifier*)
- **Arsitektur Classifier**: `512 → 256 → 128 → 5`
- **Penanganan Imbalance**: `SMOTE` pada data *training*
- **Class Weights**: `[1, 2, 1, 2, 1]`
- **Optimizer**: `Adam`
- **Learning Rate Scheduler**: `ExponentialLR` (`gamma = 0.95`)
- **Batch Size**: `64`
- **Jumlah Epoch**: `25 epochs`

---

## 3. Hasil Evaluasi Baseline

Hasil performa baseline yang diperoleh pada set pengujian:

| Metrik Evaluasi | Nilai |
| :--- | :---: |
| **Accuracy** | `98.86%` |
| **Macro Precision** | `95.23%` |
| **Macro Recall** | `91.97%` |
| **Macro F1** | `93.53%` |

---

## 4. Perbedaan Implementasi Terhadap Paper Asli

Selama proses replikasi dan audit kode terhadap naskah publikasi, ditemukan enam perbedaan utama antara paper asli dengan implementasi:

1. **Arsitektur Backbone**: Paper membahas penggunaan **AlexNet**, sedangkan repository dan implementasi baseline menggunakan **ResNet18**.
2. **Resolusi Input Citra**: Paper menggunakan ukuran input sekitar **`227×227`**, sedangkan implementasi menggunakan **`224×224`**.
3. **Formulasi MTF**: Implementasi *Markov Transition Field* (**MTF**) berbeda dari formulasi matematis yang dijelaskan pada paper.
4. **Implementasi RP**: Terdapat perbedaan pada implementasi *Recurrence Plot* (**RP**) dibandingkan deskripsi pada paper.
5. **Rekonstruksi Komponen Multimodal**: Beberapa komponen multimodal pada paper direkonstruksi berdasarkan struktur kode yang tersedia di repository referensi.
6. **Potensi Optimistic Bias pada Pemilihan Checkpoint**: Checkpoint baseline dipilih berdasarkan *test-set performance*, sehingga terdapat potensi *optimistic bias* dalam pelaporan metrik evaluasi.
