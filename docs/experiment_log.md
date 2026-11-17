# Experiment Log

Dokumen ini mencatat riwayat kronologis seluruh eksperimen pemodelan, efisiensi komputasi, eksplorasi kandidat arsitektur, pemilihan model alternatif, serta analisis evaluasi bertingkat pada proyek **ECG-Multimodal-Fusion**.

---

## 1. Ringkasan Kronologis Eksperimen

| Tahap | Model / Pendekatan | Status | Accuracy | Macro Precision | Macro Recall | Macro F1 | Parameters | Inference |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Week 1 (Baseline)** | `ResNet18 + GAF` | Baseline | `98.86%` | `95.23%` | `91.97%` | `93.53%` | `11,341,125` | `0.797 ms/sample` |
| **Week 2 (Efficiency)** | `MobileNetV3-Small + GAF` | Evaluated | `98.63%` | — | — | `92.11%` | `1,522,981` | `0.215 ms/sample` |
| **Week 2 (1D Baseline)** | `1D CNN + Raw ECG` | Evaluated | `97.61%` | — | — | `88.64%` | `36,357` | `0.012 ms/sample` |
| **Exploration** | `ECGTransForm` | Candidate | `98.54%` | `93.38%` | `90.46%` | `91.86%` | — | — |
| **Exploration** | `CAT-Net` | Candidate | `98.57%` | `92.73%` | `92.58%` | `92.64%` | — | — |
| **Exploration** | `KAN` | Dropped | — | — | — | `~84.90%` *(best val)* | — | — |
| **Exploration** | `Multi-branch CNN + Transformer` | Dropped | — | — | — | — | — | — |
| **Selected Alternative** | `CBAM-ResNet18 + GASF` *(Epoch 5)* | **Selected** | `98.4652%` | `89.6226%` | `92.1795%` | `90.5251%` | — | `1.906 ms/sample` |

---

## 2. Detail Tahapan Eksperimen

### A. Week 1 — Baseline (`ResNet18 + GAF`)
- **Accuracy**: `98.86%`
- **Macro Precision**: `95.23%`
- **Macro Recall**: `91.97%`
- **Macro F1**: `93.53%`
- **Parameters**: `11,341,125`
- **Inference**: `0.797 ms/sample`

### B. Week 2 — Komparasi Efisiensi & Representasi 1D vs 2D
Pada Week 2 dilakukan evaluasi trade-off antara akurasi, kompleksitas parameter, dan latensi inferensi:

1. **`MobileNetV3-Small + GAF`**:
   - **Accuracy**: `98.63%`
   - **Macro F1**: `92.11%`
   - **Parameters**: `1,522,981`
   - **Inference**: `0.215 ms/sample`
2. **`1D CNN + Raw ECG`**:
   - **Accuracy**: `97.61%`
   - **Macro F1**: `88.64%`
   - **Parameters**: `36,357`
   - **Inference**: `0.012 ms/sample`
3. **Referensi Baseline (`ResNet18 + GAF`)**:
   - **Parameters**: `11,341,125`
   - **Inference**: `0.797 ms/sample`

### C. Kandidat Eksplorasi Arsitektur Alternatif
1. **`ECGTransForm`**:
   - **Accuracy**: `98.54%`
   - **Macro Precision**: `93.38%`
   - **Macro Recall**: `90.46%`
   - **Macro F1**: `91.86%`
2. **`CAT-Net`**:
   - **Accuracy**: `98.57%`
   - **Macro Precision**: `92.73%`
   - **Macro Recall**: `92.58%`
   - **Macro F1**: `92.64%`
3. **`KAN` (*Kolmogorov-Arnold Network*)**:
   - **Best Validation Macro F1**: `~84.90%`
   - **Keputusan**: **Dropped** karena mengalami *overfitting* dan performa yang inferior dibandingkan kandidat lainnya.
4. **`Multi-branch CNN + Transformer`**:
   - **Keputusan**: **Dropped** karena kebutuhan konfigurasi fitur *heartbeat/RR* tidak kompatibel dengan data tingkat *heartbeat* 187 titik yang tersedia.

---

## 3. Model Alternatif Terpilih (`CBAM-ResNet18 + GASF`)

Model **`CBAM-ResNet18 + GASF`** dipilih sebagai model alternatif dengan evaluasi menggunakan **checkpoint Epoch 5**:

| Metrik | CBAM-ResNet18 + GASF (Epoch 5) | Selisih Terhadap Baseline |
| :--- | :---: | :---: |
| **Accuracy** | `98.4652%` | `-0.3948 percentage point` |
| **Macro Precision** | `89.6226%` | `-5.6074 percentage point` |
| **Macro Recall** | `92.1795%` | `+0.2095 percentage point` |
| **Macro F1** | `90.5251%` | `-3.0049 percentage point` |
| **Inference Time** | `1.906 ms/sample` | `+1.109 ms/sample` *(lebih lambat)* |

**Alasan Pemilihan**:
`CBAM-ResNet18 + GASF` dipilih secara spesifik karena memiliki **Macro Recall** yang lebih tinggi dibandingkan baseline (`+0.2095 percentage point`), meskipun model ini memiliki performa yang lebih rendah (*inferior*) pada metrik agregat lainnya (Accuracy, Macro Precision, dan Macro F1) serta waktu inferensi yang lebih lama. Model ini **tidak** diklaim unggul secara keseluruhan dibandingkan baseline.

---

## 4. Week 3 — Stratified Evaluation pada Fixed Test Set

Pada Week 3 dilakukan perbandingan antara **`ResNet18 + GAF`** dan **`MobileNetV3-Small + GAF`** menggunakan evaluasi terstratifikasi pada *fixed test set*.

> **Catatan Metodologis Penting:**
> - Evaluasi ini **BUKAN** *true 5-fold cross-validation*.
> - Kedua model **tidak dilatih ulang** (*not retrained*) pada setiap subset/fold.
> - Uji *paired t-test* yang dilakukan bersifat **eksploratif saja** (*exploratory only*) dan bukan bukti konklusif keunggulan permanen suatu arsitektur.

### A. Hasil Macro F1 per Subset Terstratifikasi

| Subset | `ResNet18 + GAF` (Macro F1) | `MobileNetV3-Small + GAF` (Macro F1) |
| :---: | :---: | :---: |
| **1** | `0.9221` | `0.8956` |
| **2** | `0.9424` | `0.9360` |
| **3** | `0.9514` | `0.9475` |
| **4** | `0.9369` | `0.9253` |
| **5** | `0.9236` | `0.9035` |

### B. Hasil Exploratory Paired t-Test

| Metrik | Nilai *p-value* |
| :--- | :---: |
| **Macro F1** | `p = 0.0318` |
| **Accuracy** | `p = 0.0471` |
| **Macro Recall** | `p = 0.0123` |
| **Macro Precision** | `p = 0.1597` |

**Limitasi Analisis Week 3**:
Kelima partisi evaluasi berasal dari subset *fixed test set* yang sama, bukan replikasi pelatihan independen (*independent training replicates*), sehingga variasi antar-subset tidak merepresentasikan varians pelatihan dari inisialisasi maupun data latih yang berbeda.
