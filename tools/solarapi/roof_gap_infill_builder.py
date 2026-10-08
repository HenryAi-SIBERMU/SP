#!/usr/bin/env python3
"""
roof_gap_infill_builder.py
==========================
Tool Analisis Suplemen & Rekayasa Potensi Celah Atap Fisik (Roof Gap Infill Builder).

PRINSIP METODOLOGI & ARSITEKTUR MUTLAK:
1. IMMUTABLE GOOGLE BASELINE: Data mentah Google Solar API (building_insights & dataLayers)
   bersifat READ-ONLY dan TIDAK BOLEH dimodifikasi, ditimpa, atau dicemari.
2. SEPARATE SUPPLEMENTAL DATASET: Skrip ini menghasilkan entitas dataset baru terpisah
   (pow_solar_gap_infill_extension.csv / .parquet) untuk menyajikan skenario rekayasa optimis.
3. ZERO HARDCODED DATA: Seluruh spesifikasi modul surya, fraksi ruang bebas pemadam kebakaran,
   dan aturan struktural dibaca secara dinamis dari file konfigurasi:
   - configs/roof_gap_infill_rules.json
   - configs/roof_gap_infill_overrides.csv
4. REPRODUCIBLE & AUDITABLE: Setiap baris output mencatat lineage formula, asumsi fraksi celah,
   dan referensi standar regulasi (SNI 8395:2017 & NFPA 1).
"""

import os
import sys
import json
import argparse
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def load_rules(rules_path: Path) -> dict:
    """Memuat parameter rekayasa dari file konfigurasi JSON."""
    if not rules_path.exists():
        raise FileNotFoundError(f"File aturan rekayasa tidak ditemukan: {rules_path}")
    with open(rules_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_overrides(overrides_path: Path) -> pd.DataFrame:
    """Memuat data override spesifik per fasilitas jika tersedia."""
    if not overrides_path.exists():
        return pd.DataFrame()
    return pd.read_csv(overrides_path)


def run_infill_calculation(
    input_csv: Path,
    rules_json: Path,
    overrides_csv: Path,
    target_gap_cat: str,
    output_csv: Path,
    output_parquet: Path
):
    print("=" * 80)
    print("  TOOL SUPLEN REKAYASA POTENSI CELAH ATAP (ROOF GAP INFILL BUILDER)")
    print("=" * 80)
    print(f"[*] Input Google Baseline  : {input_csv} (READ-ONLY)")
    print(f"[*] Rules Config           : {rules_json}")
    print(f"[*] Overrides Config       : {overrides_csv}")
    print(f"[*] Filter Kategori Celah  : {target_gap_cat}")
    print(f"[*] Output Suplemen CSV    : {output_csv}")
    print(f"[*] Output Suplemen Parquet: {output_parquet}")
    print("-" * 80)

    # 1. Validasi Input Read-Only
    if not input_csv.exists():
        raise FileNotFoundError(f"File baseline input tidak ditemukan: {input_csv}")
    df_raw = pd.read_csv(input_csv)
    print(f"[i] Total fasilitas terdaftar di Google Baseline: {len(df_raw)} titik")

    # 2. Muat Aturan & Override
    rules = load_rules(rules_json)
    df_overrides = load_overrides(overrides_csv)
    if not df_overrides.empty:
        print(f"[i] Berhasil memuat {len(df_overrides)} baris override fasilitas dari {overrides_csv.name}")

    pv_specs = rules.get("pv_module_specifications", {})
    default_params = rules.get("default_infill_parameters", {})
    cat_rules = rules.get("category_specific_rules", {})

    rated_power_wp = float(pv_specs.get("rated_power_wp", 400.0))
    eff_area_panel = float(pv_specs.get("effective_area_per_panel_m2", 2.1027))
    min_cluster = int(default_params.get("minimum_panel_cluster", 6))
    derate_eff = float(pv_specs.get("system_derate_efficiency", 0.82))

    # 3. Filter Target
    if target_gap_cat.lower() == "all":
        df_target = df_raw.copy()
    else:
        df_target = df_raw[df_raw["gap_category"].astype(str).str.strip().str.lower() == target_gap_cat.lower()].copy()

    print(f"[i] Jumlah fasilitas yang dievaluasi untuk infill ({target_gap_cat}): {len(df_target)} titik")
    if df_target.empty:
        print("[!] Tidak ada data yang cocok dengan kriteria filter. Proses berhenti.")
        return

    # Buat lookup dict override berdasarkan asset_name
    override_dict = {}
    if not df_overrides.empty and "asset_name" in df_overrides.columns:
        for _, ov_row in df_overrides.iterrows():
            a_name = str(ov_row["asset_name"]).strip()
            override_dict[a_name] = ov_row.to_dict()

    # 4. Kalkulasi Komparatif Suplemen
    results = []

    for _, row in df_target.iterrows():
        asset_name = str(row["asset_name"]).strip()
        cat = str(row.get("category", "")).strip().lower()
        
        # Google Certified Baseline Metrics (READ ONLY)
        baseline_panels = int(row.get("max_panels_count", 0))
        baseline_kwp = float(row.get("installed_capacity_kwp", 0.0))
        baseline_mwh = float(row.get("annual_generation_mwh", 0.0))
        baseline_co2 = float(row.get("ghg_reduction_tons_co2", 0.0))
        co2_factor = float(row.get("carbon_offset_factor", 790.0))
        sunshine_hours = float(row.get("sunshine_hours_annual", 1400.0))

        # Celah Terukur
        gap_unseg_m2 = float(row.get("gap_unsegmented_m2", 0.0))
        gap_unpanel_m2 = float(row.get("gap_unpanelled_m2", 0.0))
        total_gap_m2 = float(row.get("total_gap_m2", 0.0))

        # Tentukan fraksi usable & area dasar
        ov_data = override_dict.get(asset_name, {})
        has_custom_area = pd.notna(ov_data.get("custom_infill_area_m2")) and float(ov_data.get("custom_infill_area_m2", 0)) > 0
        has_fraction_ov = pd.notna(ov_data.get("usable_gap_fraction_override")) and float(ov_data.get("usable_gap_fraction_override", 0)) > 0

        if has_fraction_ov:
            usable_fraction = float(ov_data["usable_gap_fraction_override"])
            fraction_source = "Facility Override"
        elif cat in cat_rules and "usable_gap_fraction" in cat_rules[cat]:
            usable_fraction = float(cat_rules[cat]["usable_gap_fraction"])
            fraction_source = f"Category Rule ({cat})"
        else:
            usable_fraction = float(default_params.get("usable_gap_fraction", 0.60))
            fraction_source = "Default Global Parameter"

        if has_custom_area:
            base_area_m2 = float(ov_data["custom_infill_area_m2"])
            area_source = "Survey / As-Built Drawing Override"
        else:
            # Gunakan unsegmented gap sebagai basis fisik terukur utama
            base_area_m2 = gap_unseg_m2
            area_source = "Unsegmented Footprint Gap (Google API Measured)"

        # Hitung Luas Bersih Layak Panel (dikurangi setback keselamatan)
        net_infill_area_m2 = max(0.0, base_area_m2 * usable_fraction)

        # Hitung Tambahan Panel
        if net_infill_area_m2 > 0 and eff_area_panel > 0:
            raw_additional_panels = int(np.floor(net_infill_area_m2 / eff_area_panel))
        else:
            raw_additional_panels = 0

        # Terapkan ambang batas klaster minimum
        if raw_additional_panels >= min_cluster:
            infill_panels = raw_additional_panels
        else:
            infill_panels = 0

        # Hitung Tambahan Kapasitas (kWp)
        infill_kwp = round(infill_panels * (rated_power_wp / 1000.0), 2)

        # Hitung Tambahan Energi Listrik Tahunan (MWh)
        # Menghitung produktivitas per panel lokal dari titik yang sama
        if baseline_panels > 0 and baseline_mwh > 0:
            kwh_per_panel = (baseline_mwh * 1000.0) / baseline_panels
        else:
            kwh_per_panel = sunshine_hours * (rated_power_wp / 1000.0) * derate_eff

        infill_annual_gen_mwh = round((infill_panels * kwh_per_panel) / 1000.0, 2)
        infill_co2_savings_ton = round(infill_annual_gen_mwh * (co2_factor / 1000.0), 2)

        # Metrik Gabungan (Skenario Optimis Suplemen)
        combined_panels = baseline_panels + infill_panels
        combined_kwp = round(baseline_kwp + infill_kwp, 2)
        combined_mwh = round(baseline_mwh + infill_annual_gen_mwh, 2)
        combined_co2 = round(baseline_co2 + infill_co2_savings_ton, 2)

        capacity_growth_pct = round((infill_kwp / baseline_kwp * 100.0), 1) if baseline_kwp > 0 else 0.0

        # Catatan Struktural & Bukti
        structural_note = ov_data.get("notes_justification") or cat_rules.get(cat, {}).get("structural_retrofit_note", "Pemeriksaan beban mati struktural standar")
        readiness_status = ov_data.get("structural_readiness_status") or "Perlu Verifikasi Struktur Lanjutan"

        res_row = {
            "asset_id": row.get("asset_id", ""),
            "asset_name": asset_name,
            "category": cat,
            "category_display": row.get("category_display", ""),
            "city_regency": row.get("city_regency", ""),
            "gap_category": row.get("gap_category", ""),
            # Google Baseline (READ-ONLY PROVENANCE)
            "google_building_id": row.get("google_building_id", ""),
            "google_baseline_panels": baseline_panels,
            "google_baseline_kwp": baseline_kwp,
            "google_baseline_generation_mwh": baseline_mwh,
            "google_baseline_co2_savings_ton": baseline_co2,
            # Celah Fisik Terukur
            "measured_unsegmented_gap_m2": round(gap_unseg_m2, 2),
            "measured_unpanelled_gap_m2": round(gap_unpanel_m2, 2),
            "measured_total_gap_m2": round(total_gap_m2, 2),
            # Parameter Infill Rekayasa
            "infill_base_area_source": area_source,
            "infill_applied_fraction": usable_fraction,
            "infill_fraction_source": fraction_source,
            "infill_net_usable_area_m2": round(net_infill_area_m2, 2),
            # Hasil Tambahan Suplemen (New Scenario)
            "infill_additional_panels": infill_panels,
            "infill_additional_kwp": infill_kwp,
            "infill_additional_generation_mwh": infill_annual_gen_mwh,
            "infill_additional_co2_savings_ton": infill_co2_savings_ton,
            # Gabungan (Baseline + Infill)
            "combined_scenario_total_panels": combined_panels,
            "combined_scenario_total_kwp": combined_kwp,
            "combined_scenario_generation_mwh": combined_mwh,
            "combined_scenario_co2_savings_ton": combined_co2,
            "capacity_growth_potential_pct": capacity_growth_pct,
            # Audit Trail & Lineage
            "structural_readiness": readiness_status,
            "engineering_justification": structural_note,
            "methodology_standard": "SNI 8395:2017 & NFPA 1 Ch.11.12 Setback Model",
            "data_layer_type": "SUPPLEMENTAL_ROOF_GAP_EXTENSION"
        }
        results.append(res_row)

    df_result = pd.DataFrame(results)

    # 5. Simpan Hasil ke File Baru Terpisah
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df_result.to_csv(output_csv, index=False, encoding="utf-8")
    df_result.to_parquet(output_parquet, index=False)

    print("[+] SUKSES: Data suplemen rekayasa celah atap berhasil disimpan!")
    print(f"    - CSV    : {output_csv}")
    print(f"    - Parquet: {output_parquet}")
    print("-" * 80)

    # 6. Ringkasan Eksekutif
    tot_base_kwp = df_result["google_baseline_kwp"].sum()
    tot_infill_kwp = df_result["infill_additional_kwp"].sum()
    tot_comb_kwp = df_result["combined_scenario_total_kwp"].sum()
    tot_growth = (tot_infill_kwp / tot_base_kwp * 100.0) if tot_base_kwp > 0 else 0.0

    print("RINGKASAN EKSEKUTIF SKENARIO GAP INFILL:")
    print(f"  * Total Fasilitas Dianalisis       : {len(df_result)} titik ({target_gap_cat})")
    print(f"  * Baseline Google Solar API        : {tot_base_kwp:,.2f} kWp ({df_result['google_baseline_panels'].sum():,} panel)")
    print(f"  * Potensi Tambahan Celah Infill    : +{tot_infill_kwp:,.2f} kWp (+{df_result['infill_additional_panels'].sum():,} panel)")
    print(f"  * Total Gabungan (Skenario Optimis): {tot_comb_kwp:,.2f} kWp (+{tot_growth:.1f}% kenaikan kapasitas)")
    print(f"  * Tambahan Energi Bersih Tahunan   : +{df_result['infill_additional_generation_mwh'].sum():,.2f} MWh/thn")
    print(f"  * Tambahan Reduksi Emisi CO2       : +{df_result['infill_additional_co2_savings_ton'].sum():,.2f} Ton/thn")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Tool Analisis Suplemen & Rekayasa Potensi Celah Atap Fisik (Roof Gap Infill Builder)"
    )
    parser.add_argument(
        "--input",
        type=str,
        default=str(PROJECT_ROOT / "data" / "processed" / "calculations" / "pow_solar_100_titik_summary.csv"),
        help="Path ke file CSV baseline Google Solar API (READ ONLY)"
    )
    parser.add_argument(
        "--rules",
        type=str,
        default=str(PROJECT_ROOT / "configs" / "roof_gap_infill_rules.json"),
        help="Path ke file aturan parameter rekayasa celah JSON"
    )
    parser.add_argument(
        "--overrides",
        type=str,
        default=str(PROJECT_ROOT / "configs" / "roof_gap_infill_overrides.csv"),
        help="Path ke file CSV override spesifik fasilitas"
    )
    parser.add_argument(
        "--target-gap-category",
        type=str,
        default="Gap Besar",
        help="Target kategori celah atap yang dianalisis: 'Gap Besar', 'Gap Sedang', 'Gap Sedikit', atau 'all'"
    )
    parser.add_argument(
        "--output-csv",
        type=str,
        default=str(PROJECT_ROOT / "data" / "processed" / "calculations" / "pow_solar_gap_infill_extension.csv"),
        help="Path output CSV untuk dataset suplemen baru"
    )
    parser.add_argument(
        "--output-parquet",
        type=str,
        default=str(PROJECT_ROOT / "data" / "processed" / "calculations" / "pow_solar_gap_infill_extension.parquet"),
        help="Path output Parquet untuk dataset suplemen baru"
    )

    args = parser.parse_args()

    run_infill_calculation(
        input_csv=Path(args.input),
        rules_json=Path(args.rules),
        overrides_csv=Path(args.overrides),
        target_gap_cat=args.target_gap_category,
        output_csv=Path(args.output_csv),
        output_parquet=Path(args.output_parquet)
    )


if __name__ == "__main__":
    main()
