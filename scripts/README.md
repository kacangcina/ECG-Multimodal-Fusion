# Scripts (`scripts/`)

Folder `scripts/` menyediakan antarmuka baris perintah (*command-line entry points*) dan *documentation runner* untuk eksperimen klasifikasi detak jantung ECG pada repository **ECG-Multimodal-Fusion**.

## Tujuan Folder `scripts/`

1. **Entry Point & Documentation Runner**: Memberikan cara standar untuk memeriksa lokasi notebook eksperimen, ringkasan konfigurasi arsitektur, serta metrik evaluasi final langsung dari terminal tanpa harus membuka notebook terlebih dahulu.
2. **Validasi Struktur Proyek**: Memverifikasi keberadaan file notebook eksperimen yang bersesuaian pada direktori `notebooks/` menggunakan *relative path*.
3. **Panduan Reproduksibilitas**: Menyediakan instruksi eksekusi yang jelas mengenai lingkungan komputasi yang digunakan dalam penelitian.

> **Catatan Penting:** Kedua script di dalam folder ini **bukan implementasi training ulang**. Script tidak menjalankan proses pelatihan model secara otomatis.

## Daftar File

- **`run_baseline.py`**
  *Entry point* dan *documentation runner* untuk eksperimen **Baseline** (`notebooks/01_replikasi.ipynb`). Menampilkan konfigurasi model (ResNet18 pretrained ImageNet, input ECG 187 titik, Gramian Angular Field 224×224, pelatihan `layer3`, `layer4`, dan `classifier`, SMOTE, *class weights* `[1, 2, 1, 2, 1]`, Adam, ExponentialLR, 25 epoch), hasil evaluasi final, lokasi notebook, serta instruksi eksekusi di Google Colab.
- **`run_cbam_gasf.py`**
  *Entry point* dan *documentation runner* untuk eksperimen alternatif **CBAM-GASF** (`notebooks/09_cbam_gasf_pilot_recall_selection (2).ipynb`). Menampilkan konfigurasi model (ResNet18 pretrained ImageNet + CBAM pada layer ResNet, GASF 224×224, *class weights* `[1, 2, 1, 2, 1]`, Adam, ExponentialLR), hasil evaluasi pada **checkpoint Epoch 5**, perbandingan selisih metrik terhadap baseline (dengan keunggulan Macro Recall `+0.2095 percentage point`), lokasi notebook, serta instruksi eksekusi di Google Colab.
- **`README.md`**
  Dokumentasi panduan penggunaan folder `scripts/`.

## Mengapa Eksperimen Utama Berada di Jupyter Notebook?

Seluruh pipeline pelatihan (*training*), ekstraksi citra GAF/GASF, serta evaluasi penuh tetap dipertahankan di dalam file Jupyter Notebook pada folder `notebooks/` karena:

- Eksperimen dijalankan menggunakan **Google Colab** untuk kebutuhan akselerasi GPU.
- Pipeline terintegrasi dengan **Google Drive** untuk membaca dataset ECG, menyimpan *checkpoint* model tiap epoch, serta mengelola artefak eksperimen berukuran besar.

## Cara Menjalankan

Jalankan kedua script dari **root repository** (`ECG-Multimodal-Fusion/`):

```bash
python scripts/run_baseline.py
python scripts/run_cbam_gasf.py
```

Jika file notebook yang dirujuk tidak ditemukan pada path relatif yang diharapkan, script akan menampilkan pesan error yang jelas dan keluar dengan *exit code* non-zero (`1`).

## Struktur Folder yang Relevan

```text
ECG-Multimodal-Fusion/
├── notebooks/
│   ├── 01_replikasi.ipynb
│   └── 09_cbam_gasf_pilot_recall_selection (2).ipynb
├── configs/
│   ├── baseline.yaml
│   └── cbam_gasf.yaml
├── scripts/
│   ├── README.md
│   ├── run_baseline.py
│   └── run_cbam_gasf.py
└── outputs/
    ├── figures/
    └── results/
```
