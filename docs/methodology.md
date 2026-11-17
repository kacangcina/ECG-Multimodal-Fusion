# Methodology

Dokumen ini menjelaskan metodologi penelitian secara sistematis untuk klasifikasi detak jantung ECG 5-kelas pada repository **ECG-Multimodal-Fusion**.

---

## Alur Pipeline Utama

```text
Raw ECG (187 points)
  → preprocessing
  → GAF/GASF transformation
  → resize 224×224
  → ResNet18 / CBAM-ResNet18
  → classifier
  → 5-class prediction
  → evaluation
```

---

## 1. Dataset

Penelitian ini menggunakan **MIT-BIH Heartbeat Dataset** yang diperoleh dari Kaggle (`shayanfazeli/heartbeat`). Setiap sampel merepresentasikan segmen satu siklus detak jantung (*heartbeat*) yang terdiri dari **187 titik** (*data points*) dan dikategorikan ke dalam **5 kelas** (`N`, `S`, `V`, `F`, `Q`).

- **Total Sampel Training**: `87,554` sampel
- **Total Sampel Test**: `21,892` sampel

---

## 2. ECG Preprocessing

Setiap sinyal detak jantung mentah berdurasi 187 titik diproses pada tingkat segmen *heartbeat* individual agar siap ditransformasikan ke dalam domain citra 2D berbasis korelasi sudut (*Gramian Angular Field*), diikuti dengan penyesuaian dimensi spasial (*resizing*) ke ukuran `224×224` piksel agar sesuai dengan arsitektur jaringan konvolusional 2D berbasis ResNet.

---

## 3. Data Split

Pembagian dataset mengikuti partisi *training* dan *test* tetap dengan distribusi kelas yang sangat tidak seimbang (*imbalanced*), di mana kelas normal (`N`) mendominasi dataset:

| Kelas | Training Set (Asli) | Test Set (Tetap) |
| :---: | :---: | :---: |
| **N** | `72,471` | `18,118` |
| **S** | `2,223` | `556` |
| **V** | `5,788` | `1,448` |
| **F** | `641` | `162` |
| **Q** | `6,431` | `1,608` |
| **Total** | **`87,554`** | **`21,892`** |

---

## 4. SMOTE

Untuk mengatasi ketimpangan distribusi antar-kelas pada data latih tanpa mengubah distribusi evaluasi, diterapkan teknik *Synthetic Minority Over-sampling Technique* (**SMOTE**) secara eksklusif pada **training set**:

| Kelas | Sebelum SMOTE (Train) | Sesudah SMOTE (Train) |
| :---: | :---: | :---: |
| **N** | `72,471` | `72,471` |
| **S** | `2,223` | `30,000` |
| **V** | `5,788` | `20,000` |
| **F** | `641` | `20,000` |
| **Q** | `6,431` | `10,000` |

*Test set* (`21,892` sampel) dipertahankan pada distribusi aslinya untuk menjaga validitas pengujian.

---

## 5. GAF Representation

Pada model baseline, sinyal ECG 1D sepanjang `187` titik dikonversi menjadi representasi citra 2D menggunakan **Gramian Angular Field (GAF)**. Sinyal 1D dinormalisasi dan dipetakan ke koordinat polar sehingga hubungan temporal antar-titik sinyal direpresentasikan dalam bentuk matriks korelasi sudut 2D, yang kemudian di-*resize* menjadi **`224×224`**.

---

## 6. GASF Representation

Pada eksperimen alternatif, digunakan **Gramian Angular Summation Field (GASF)** yang memetakan sinyal ECG `187` titik ke koordinat polar dan menghitung penjumlahan kosinus sudut berpasangan:

$$\text{GASF}_{i,j} = \cos(\phi_i + \phi_j)$$

Matriks hasil transformasi GASF kemudian di-*resize* menjadi **`224×224`** sebelum diproses oleh jaringan konvolusional berbasis atensi.

---

## 7. ResNet18 Baseline

Model baseline dibangun menggunakan backbone **ResNet18** (*pretrained* ImageNet) dengan total **`11,341,125`** parameter:

- **Fine-Tuning**: Blok konvolusi `layer3` dan `layer4` dibuka untuk pelatihan (*trainable*).
- **Classifier Head**: *Fully connected layers* dengan struktur dimensi `512 → 256 → 128 → 5` untuk menghasilkan prediksi probabilitas 5 kelas detak jantung.

---

## 8. CBAM-ResNet18

Untuk meningkatkan sensitivitas model terhadap pola diskriminatif pada kelas minoritas, modul atensi **Convolutional Block Attention Module (CBAM)** diintegrasikan ke dalam layer **ResNet18** (*pretrained* ImageNet) dengan input citra **GASF** berukuran `224×224`. Mekanisme atensi kanal dan spasial pada CBAM mengarahkan fokus representasi fitur pada area sinyal yang paling informatif dalam membedakan morfologi aritmia.

---

## 9. Training Configuration

Konfigurasi pelatihan yang digunakan pada eksperimen utama dirangkum sebagai berikut:

| Komponen Pelatihan | Konfigurasi |
| :--- | :--- |
| **Optimizer** | `Adam` |
| **LR Scheduler** | `ExponentialLR` (`gamma = 0.95`) |
| **Class Weights** | `[1, 2, 1, 2, 1]` |
| **Batch Size** | `64` |
| **Epoch Baseline (`ResNet18 + GAF`)** | `25 epochs` |
| **Checkpoint Evaluasi (`CBAM-ResNet18 + GASF`)** | `Epoch 5` |

---

## 10. Evaluation Metrics

Evaluasi kinerja model dilakukan menggunakan metrik klasifikasi multi-kelas dan efisiensi komputasi:

1. **Accuracy**: Proporsi keseluruhan prediksi yang benar terhadap total sampel uji.
2. **Macro Precision**: Rata-rata tidak tertimbang dari *precision* pada seluruh 5 kelas.
3. **Macro Recall**: Rata-rata tidak tertimbang dari *recall* (sensitivitas) pada seluruh 5 kelas, menjadi metrik prioritas untuk mendeteksi kelas minoritas secara merata.
4. **Macro F1-Score**: Rata-rata harmonik dari *precision* dan *recall* yang dirata-ratakan secara makro di seluruh kelas.
5. **Efisiensi Komputasi**: Jumlah parameter model (*parameters*) dan waktu inferensi per sampel (`ms/sample`).

---

## 11. Week 2 Comparison

Pada Week 2 dilakukan perbandingan antara arsitektur berbasis citra 2D dan sinyal 1D langsung untuk mengevaluasi efisiensi komputasi:

- **`ResNet18 + GAF` (Baseline)**: Accuracy `98.86%`, Macro F1 `93.53%`, Parameters `11,341,125`, Inference `0.797 ms/sample`.
- **`MobileNetV3-Small + GAF`**: Accuracy `98.63%`, Macro F1 `92.11%`, Parameters `1,522,981`, Inference `0.215 ms/sample`.
- **`1D CNN + Raw ECG`**: Accuracy `97.61%`, Macro F1 `88.64%`, Parameters `36,357`, Inference `0.012 ms/sample`.

Selain itu, dilakukan eksplorasi kandidat arsitektur lain (`ECGTransForm`, `CAT-Net`, `KAN`, dan `Multi-branch CNN + Transformer`). Dari seluruh eksplorasi, **`CBAM-ResNet18 + GASF`** (checkpoint Epoch 5) dipilih sebagai model alternatif karena mencapai **Macro Recall `92.1795%`** (`+0.2095 percentage point` di atas baseline `91.97%`), meskipun lebih rendah pada Accuracy (`98.4652%`, `-0.3948 percentage point`), Macro Precision (`89.6226%`, `-5.6074 percentage point`), dan Macro F1 (`90.5251%`, `-3.0049 percentage point`), serta memiliki latensi inferensi lebih tinggi (`1.906 ms/sample`). Dengan demikian, model ini dipilih berdasarkan kriteria keunggulan Macro Recall, bukan sebagai model terbaik secara keseluruhan.

---

## 12. Week 3 Analysis

Pada Week 3 dilakukan analisis perbandingan antara **`ResNet18 + GAF`** dan **`MobileNetV3-Small + GAF`** menggunakan pembagian **5 subset terstratifikasi pada fixed test set**:

- **Macro F1 `ResNet18 + GAF`**: `0.9221`, `0.9424`, `0.9514`, `0.9369`, `0.9236`
- **Macro F1 `MobileNetV3-Small + GAF`**: `0.8956`, `0.9360`, `0.9475`, `0.9253`, `0.9035`
- **Exploratory Paired t-Test**:
  - Macro F1: `p = 0.0318`
  - Accuracy: `p = 0.0471`
  - Macro Recall: `p = 0.0123`
  - Macro Precision: `p = 0.1597`

Analisis ini **bukan** merupakan *true 5-fold cross-validation* karena model tidak dilatih ulang pada setiap partisi dan pengujian dilakukan pada subset dari *fixed test set* yang sama. Uji *paired t-test* hanya digunakan sebagai analisis eksploratif.

---

## 13. Limitations

Beberapa keterbatasan metodologis dalam penelitian ini perlu diperhatikan dalam interpretasi hasil:

1. **Potensi Optimistic Bias pada Baseline**: Pemilihan checkpoint model baseline mempertimbangkan performa pada *test set*, yang berpotensi menimbulkan *optimistic bias*.
2. **Evaluasi Week 3 Bukan True Cross-Validation**: Partisi pada Week 3 merupakan subset terstratifikasi dari *fixed test set* yang sama dan bukan replikasi pelatihan independen (*independent training replicates*), sehingga tidak mengukur varians proses pelatihan.
3. **Sifat Eksploratif Uji Statistik**: Hasil *paired t-test* bersifat eksploratif dan tidak dapat dijadikan bukti konklusif bahwa suatu arsitektur (termasuk CBAM) secara mutlak lebih unggul.
4. **Trade-off Kinerja Model Alternatif**: `CBAM-ResNet18 + GASF` memberikan peningkatan tipis pada Macro Recall (`+0.2095 percentage point`), namun mengalami penurunan pada Accuracy, Macro Precision, dan Macro F1 serta membutuhkan waktu inferensi lebih lama (`1.906 ms/sample`).
5. **Keterbatasan Granularitas Data**: Data yang tersedia berbentuk segmen *heartbeat* individual 187 titik sehingga tidak mendukung arsitektur yang membutuhkan informasi urutan interval RR antar-detak secara kontinu (seperti kandidat `Multi-branch CNN + Transformer`).
