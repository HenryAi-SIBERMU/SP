"""
generate_kumulatif_segments.py
==============================
Mengekstrak seluruh data segmentasi bidang atap (roofSegmentStats dan solarPanels)
dari file mentah Google Solar API Building Insights JSON untuk seluruh 2.100 aset.
Menghasilkan output terstandarisasi:
  - data/processed/calculations/pow_solar_kumulatif_segments.parquet
  - data/processed/calculations/pow_solar_kumulatif_segments.csv
"""

import json
import time
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CALC_DIR = PROJECT_ROOT / "data" / "processed" / "calculations"
RAW_BI_DIR = PROJECT_ROOT / "data" / "raw" / "solar" / "building_insights"

SOLAR_INSIGHTS = [
    "Menghadap Utara (Iradiasi optimal saat matahari di utara)",
    "Menghadap Timur Laut (Iradiasi optimal pagi menjelang siang)",
    "Menghadap Timur (Iradiasi optimal pagi hari 07.00–11.00)",
    "Menghadap Tenggara (Iradiasi optimal pagi hari)",
    "Menghadap Selatan (Iradiasi optimal saat matahari di selatan)",
    "Menghadap Barat Daya (Iradiasi optimal siang–sore)",
    "Menghadap Barat (Iradiasi optimal siang–sore 12.00–16.00)",
    "Menghadap Barat Laut (Iradiasi optimal sore hari)"
]
DIRS = ["Utara", "Timur Laut", "Timur", "Tenggara", "Selatan", "Barat Daya", "Barat", "Barat Laut"]


def main():
    print("=" * 80)
    print("  KUMULATIF ROOF SEGMENTS ETL PROCESSOR (2.100 TITIK)")
    print("=" * 80)
    t0 = time.time()

    summary_path = CALC_DIR / "pow_solar_kumulatif_summary.csv"
    if not summary_path.exists():
        raise FileNotFoundError(f"File summary kumulatif tidak ditemukan: {summary_path}")

    df_summary = pd.read_csv(summary_path)
    print(f"[*] Total aset dalam summary: {len(df_summary)} titik")

    records = []
    missing_bi = 0

    for idx, row in df_summary.iterrows():
        aid = str(row["asset_id"]).strip()
        aid_lower = aid.lower()
        cat = str(row["category"]).strip().lower()
        cat_disp = str(row["category_display"]).strip()
        asset_name = str(row["asset_name"]).strip()

        folder_candidates = [cat, cat.replace("_", "")]
        if "mrt" in aid_lower:
            folder_candidates.extend(["mrt", "mrt_lrt"])
        if "lrt" in aid_lower:
            folder_candidates.extend(["lrt", "mrt_lrt"])

        bi_candidates = [RAW_BI_DIR / c / f"{aid_lower}_insights.json" for c in folder_candidates]
        bi_path = next((p for p in bi_candidates if p.exists()), None)

        if not bi_path:
            missing_bi += 1
            continue

        try:
            with open(bi_path, "r", encoding="utf-8") as f:
                bi_data = json.load(f)
        except Exception as e:
            print(f"[!] Gagal membaca {bi_path}: {e}")
            continue

        sp = bi_data.get("solarPotential", {})
        panels = sp.get("solarPanels", [])
        segs = sp.get("roofSegmentStats", [])

        for s_idx, s in enumerate(segs):
            p_cnt = sum(1 for pan in panels if pan.get("segmentIndex") == s_idx)
            p_kwh = sum(pan.get("yearlyEnergyDcKwh", 0) for pan in panels if pan.get("segmentIndex") == s_idx)

            pitch = round(float(s.get("pitchDegrees", 0.0)), 2)
            az = float(s.get("azimuthDegrees", 0.0))
            d_idx = int((az + 22.5) // 45) % 8

            if pitch < 3.0:
                insight = "Atap Datar (Puncak tengah hari 11.00–13.00, self-cleaning alami rendah)"
            else:
                insight = SOLAR_INSIGHTS[d_idx]

            records.append({
                "asset_id": aid,
                "asset_name": asset_name,
                "category": cat,
                "category_display": cat_disp,
                "segment_index": s_idx,
                "pitch_degrees": pitch,
                "azimuth_degrees": round(az, 2),
                "azimuth_direction": DIRS[d_idx],
                "spatial_status": "Tampil di Citra" if p_cnt > 0 else "Dieliminasi Google (0 Panel)",
                "solar_insight": insight,
                "plane_height_m": round(float(s.get("planeHeightAtCenterMeters", 0.0)), 2),
                "area_m2": round(float(s.get("stats", {}).get("areaMeters2", 0.0)), 2),
                "ground_area_m2": round(float(s.get("stats", {}).get("groundAreaMeters2", 0.0)), 2),
                "panels_count": p_cnt,
                "capacity_kwp": round(p_cnt * 0.4, 2),
                "annual_generation_mwh": round(p_kwh / 1000.0, 2)
            })

    df_segs = pd.DataFrame(records)
    print(f"[*] Berhasil mengekstrak {len(df_segs):,} segmen dari {len(df_summary) - missing_bi:,} titik.")
    if missing_bi > 0:
        print(f"[!] Peringatan: {missing_bi} titik tidak memiliki file Building Insights.")

    # Export to Parquet and CSV
    out_parquet = CALC_DIR / "pow_solar_kumulatif_segments.parquet"
    out_csv = CALC_DIR / "pow_solar_kumulatif_segments.csv"

    df_segs.to_parquet(out_parquet, index=False)
    print(f"[+] Tersimpan Parquet : {out_parquet.relative_to(PROJECT_ROOT)} ({out_parquet.stat().st_size / 1024:.1f} KB)")

    df_segs.to_csv(out_csv, index=False, encoding="utf-8")
    print(f"[+] Tersimpan CSV     : {out_csv.relative_to(PROJECT_ROOT)} ({out_csv.stat().st_size / (1024*1024):.2f} MB)")

    print(f"[*] Waktu eksekusi total: {time.time() - t0:.2f} detik")
    print("=" * 80)


if __name__ == "__main__":
    main()
