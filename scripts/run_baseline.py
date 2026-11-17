"""Entry point and documentation runner for the ECG baseline experiment."""

from pathlib import Path
import sys


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    notebook_rel_path = Path("notebooks") / "01_replikasi.ipynb"
    notebook_path = repo_root / notebook_rel_path

    if not notebook_path.is_file():
        print(
            f"[ERROR] Notebook baseline tidak ditemukan pada path relatif: "
            f"{notebook_rel_path.as_posix()}",
            file=sys.stderr,
        )
        print(
            "Pastikan Anda menjalankan script ini dari root repository "
            "(contoh: python scripts/run_baseline.py) dan file notebook tersedia.",
            file=sys.stderr,
        )
        return 1

    separator = "=" * 68
    print(separator)
    print("ECG HEARTBEAT CLASSIFICATION - BASELINE EXPERIMENT RUNNER")
    print(separator)
    print(f"Lokasi Notebook : {notebook_rel_path.as_posix()}")
    print("Status File     : Ditemukan")
    print()

    print("[Konfigurasi Eksperimen Baseline]")
    print("- Arsitektur     : ResNet18 (pretrained ImageNet)")
    print("- Input Sinyal   : ECG 187 titik")
    print("- Representasi   : Gramian Angular Field (GAF)")
    print("- Ukuran Input   : 224 x 224")
    print("- Layer Dilatih  : layer3, layer4, dan classifier")
    print("- Penyeimbang    : SMOTE pada data training")
    print("- Class Weights  : [1, 2, 1, 2, 1]")
    print("- Optimizer      : Adam")
    print("- LR Scheduler   : ExponentialLR")
    print("- Jumlah Epoch   : 25 epoch")
    print()

    print("[Hasil Evaluasi Baseline Final]")
    print("- Accuracy       : 98.86%")
    print("- Macro Precision: 95.23%")
    print("- Macro Recall   : 91.97%")
    print("- Macro F1       : 93.53%")
    print("- Parameters     : 11,341,125")
    print()

    print("[Instruksi Eksekusi]")
    print(
        "Script ini berfungsi sebagai entry point dokumentasi dan tidak "
        "menjalankan proses training secara otomatis."
    )
    print(
        "Eksperimen utama harus dijalankan melalui Google Colab dengan membuka "
        f"'{notebook_rel_path.as_posix()}', karena proses training dan evaluasi "
        "menggunakan Google Drive untuk penyimpanan dataset, checkpoint model, "
        "serta artefak eksperimen berukuran besar."
    )
    print(separator)
    return 0


if __name__ == "__main__":
    sys.exit(main())
