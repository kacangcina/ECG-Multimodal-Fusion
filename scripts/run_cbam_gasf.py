"""Entry point and documentation runner for the CBAM-GASF ECG experiment."""

from pathlib import Path
import sys


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    notebook_rel_path = (
        Path("notebooks") / "09_cbam_gasf_pilot_recall_selection (2).ipynb"
    )
    notebook_path = repo_root / notebook_rel_path

    if not notebook_path.is_file():
        print(
            f"[ERROR] Notebook CBAM-GASF tidak ditemukan pada path relatif: "
            f"{notebook_rel_path.as_posix()}",
            file=sys.stderr,
        )
        print(
            "Pastikan Anda menjalankan script ini dari root repository "
            "(contoh: python scripts/run_cbam_gasf.py) dan file notebook tersedia.",
            file=sys.stderr,
        )
        return 1

    separator = "=" * 68
    print(separator)
    print("ECG HEARTBEAT CLASSIFICATION - CBAM-GASF EXPERIMENT RUNNER")
    print(separator)
    print(f"Lokasi Notebook : {notebook_rel_path.as_posix()}")
    print("Status File     : Ditemukan")
    print(f"Checkpoint Eval : Epoch 5")
    print()

    print("[Konfigurasi Eksperimen CBAM-GASF]")
    print("- Arsitektur     : ResNet18 (pretrained ImageNet) + CBAM pada layer ResNet")
    print("- Input Sinyal   : ECG 187 titik")
    print("- Representasi   : GASF (Gramian Angular Summation Field)")
    print("- Ukuran Input   : Resize menjadi 224 x 224")
    print("- Class Weights  : [1, 2, 1, 2, 1]")
    print("- Optimizer      : Adam")
    print("- LR Scheduler   : ExponentialLR")
    print("- Evaluasi       : Menggunakan checkpoint Epoch 5")
    print()

    print("[Hasil Evaluasi CBAM-GASF (Checkpoint Epoch 5)]")
    print("- Accuracy       : 98.4652%")
    print("- Macro Precision: 89.6226%")
    print("- Macro Recall   : 92.1795%")
    print("- Macro F1       : 90.5251%")
    print("- Inference Time : 1.906 ms/sample")
    print("- Checkpoint     : Epoch 5")
    print()

    print("[Perbandingan Terhadap Baseline]")
    print("- Accuracy        : -0.3948 percentage point")
    print("- Macro Precision : -5.6074 percentage point")
    print("- Macro Recall    : +0.2095 percentage point")
    print("- Macro F1        : -3.0049 percentage point")
    print(
        "Catatan Pemilihan : CBAM-GASF dipilih karena memiliki Macro Recall "
        "sedikit lebih tinggi daripada baseline (+0.2095 percentage point)."
    )
    print()

    print("[Instruksi Eksekusi]")
    print(
        "Script ini berfungsi sebagai entry point dokumentasi dan tidak "
        "menjalankan proses training secara otomatis."
    )
    print(
        "Untuk menjalankan eksperimen atau mereproduksi hasil, buka dan jalankan "
        f"'{notebook_rel_path.as_posix()}' melalui Google Colab, karena notebook "
        "bergantung pada Google Drive untuk akses dataset, checkpoint, dan "
        "artefak berukuran besar."
    )
    print(separator)
    return 0


if __name__ == "__main__":
    sys.exit(main())
