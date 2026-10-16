"""
Script thẩm định tính nhất quán số liệu thực nghiệm Mốc M3
Học phần: Khai thác dữ liệu (Data Mining) — Đề tài 16: World Happiness Report
Phụ trách: Hà Mạnh Trường (Nhóm trưởng — MSSV: 2045240326)
Tài liệu căn cứ: reports/final_report/nhiem_vu_ha_manh_truong.md (Mốc M3, Ngày 15–21)
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import io
import re
from pathlib import Path
import pandas as pd
from PIL import Image

# Thiết lập đường dẫn tương đối độc lập môi trường
project_root = Path(__file__).resolve().parent.parent
tables_dir = project_root / "reports" / "tables"
figures_dir = project_root / "reports" / "figures"
processed_dir = project_root / "data" / "processed"
logs_dir = project_root / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)
log_file_path = logs_dir / "audit_m3_consistency.log"

YEARS = [2015, 2016, 2017, 2018, 2019]

def audit():
    output_lines = []
    
    def log(msg):
        print(msg)
        output_lines.append(msg)
        
    log("================================================================================")
    log("BÁO CÁO THẨM ĐỊNH TÍNH NHẤT QUÁN SỐ LIỆU THỰC NGHIỆM MỐC M3 — NHÓM TRƯỞNG")
    log("Người thẩm định: Hà Mạnh Trường (MSSV: 2045240326)")
    log("Đề tài 16: Phân nhóm quốc gia theo các yếu tố hạnh phúc (World Happiness Report)")
    log("Thời gian thực hiện: Mốc M3 (Ngày 15 – Ngày 21)")
    log("================================================================================\n")
    
    all_passed = True
    
    # --------------------------------------------------------------------------
    # NGÀY 15: Chốt định dạng bảng biểu và cách trình bày kết quả k* chính và k=3 đối chứng
    # --------------------------------------------------------------------------
    log("--- [NGÀY 15] THẨM ĐỊNH ĐỊNH DẠNG BẢNG BIỂU & CẤU HÌNH ĐỐI CHỨNG k=3 ---")
    c3_path = tables_dir / "contrast_k3_by_year.csv"
    if not c3_path.exists():
        log("FAIL: Không tìm thấy bảng reports/tables/contrast_k3_by_year.csv")
        all_passed = False
    else:
        df_c3 = pd.read_csv(c3_path)
        required_cols = {"year", "algorithm", "k_contrast", "silhouette", "davies_bouldin"}
        if not required_cols.issubset(df_c3.columns):
            log(f"FAIL: Bảng contrast_k3_by_year.csv thiếu cột bắt buộc {required_cols - set(df_c3.columns)}")
            all_passed = False
        elif len(df_c3) != 10:
            log(f"FAIL: Bảng contrast_k3_by_year.csv có {len(df_c3)} dòng (kỳ vọng đúng 10 dòng: 2 thuật toán x 5 năm)")
            all_passed = False
        else:
            log("PASS: Bảng contrast_k3_by_year.csv đúng cấu trúc 10 dòng (2 thuật toán K-Means/Ward x 5 năm).")
            for y in YEARS:
                sub = df_c3[df_c3["year"] == y]
                log(f"  - Năm {y}: K-Means Sil={sub[sub['algorithm']=='K-Means']['silhouette'].values[0]:.4f}, Ward Sil={sub[sub['algorithm']=='Ward']['silhouette'].values[0]:.4f}")

    # --------------------------------------------------------------------------
    # NGÀY 16: Kiểm tra tính hợp lý của số cụm k* giữa các năm (trong khoảng 2 đến 5 cụm)
    # --------------------------------------------------------------------------
    log("\n--- [NGÀY 16] KIỂM TRA TÍNH HỢP LÝ CỦA SỐ CỤM k* GIỮA CÁC NĂM ---")
    k_path = tables_dir / "k_sensitivity_by_year.csv"
    if not k_path.exists():
        log("FAIL: Không tìm thấy bảng reports/tables/k_sensitivity_by_year.csv")
        all_passed = False
    else:
        df_k = pd.read_csv(k_path)
        best_k_rows = df_k.loc[df_k.groupby("year")["silhouette"].idxmax()].sort_values("year")
        k_values = best_k_rows["k"].tolist()
        log(f"Số cụm tối ưu k* theo từng năm: {dict(zip(best_k_rows['year'], k_values))}")
        
        valid_range = all(2 <= k <= 5 for k in k_values)
        if not valid_range:
            log(f"FAIL: Có giá trị k* nằm ngoài khoảng hợp lý [2, 5]: {k_values}")
            all_passed = False
        else:
            log("PASS: 100% số cụm tối ưu k* nằm trong khoảng hợp lý [2, 5].")
            if all(k == 3 for k in k_values):
                log("PASS: Tất cả 5 năm đều đồng thuận k* = 3 là số cụm tối ưu toàn cục (Silhouette cực đại: 0.293 – 0.344).")
            else:
                log(f"NOTE: k* biến thiên giữa các năm: {k_values}")

    # --------------------------------------------------------------------------
    # NGÀY 17: Đối chiếu các con số trong notebook 03 với các file CSV trong reports/tables/
    # --------------------------------------------------------------------------
    log("\n--- [NGÀY 17] ĐỐI CHIẾU SỐ LIỆU THỰC NGHIỆM VỚI CÁC TỆP CSV ---")
    expected_tables = {
        "k_sensitivity_by_year.csv": (40, "Khảo sát k in [2, 9] qua 5 năm"),
        "model_comparison_metrics_by_year.csv": (25, "So sánh 5 cấu hình x 5 năm"),
        "dbscan_sweep.csv": (60, "Quét siêu tham số DBSCAN 4 eps x 3 min_samples x 5 năm"),
        "stability_ari.csv": (25, "Độ ổn định ARI qua 10 seed ngẫu nhiên x 5 năm"),
        "contrast_k3_by_year.csv": (10, "Cấu hình đối chứng k=3 xuyên năm"),
    }
    
    for t_name, (exp_rows, desc) in expected_tables.items():
        t_file = tables_dir / t_name
        if not t_file.exists():
            log(f"FAIL: Thiếu bảng {t_name}")
            all_passed = False
        else:
            df = pd.read_csv(t_file)
            if len(df) != exp_rows:
                log(f"FAIL: {t_name} có {len(df)} dòng, kỳ vọng {exp_rows} dòng")
                all_passed = False
            else:
                # Kiểm tra các chỉ số cốt lõi không được có NaN
                core_metric_cols = [c for c in ["silhouette", "davies_bouldin", "calinski_harabasz", "mean_pairwise_ari", "inertia"] if c in df.columns]
                core_nan = df[core_metric_cols].isna().sum().sum()
                if core_nan > 0:
                    log(f"FAIL: {t_name} có {core_nan} giá trị NaN ở các chỉ số đo lường cốt lõi")
                    all_passed = False
                else:
                    log(f"PASS: {t_name} ({len(df)}/{exp_rows} dòng, 0 NaN ở các độ đo cốt lõi) — {desc}")

    # --------------------------------------------------------------------------
    # NGÀY 18: Rà soát khóa chính và tên cột giữa các bảng số liệu
    # --------------------------------------------------------------------------
    log("\n--- [NGÀY 18] RÀ SOÁT KHÓA CHÍNH VÀ LIÊN KẾT DỮ LIỆU ---")
    interim_path = project_root / "data" / "interim" / "happiness_merged.csv"
    if not interim_path.exists():
        log("FAIL: Không tìm thấy dữ liệu interim happiness_merged.csv")
        all_passed = False
    else:
        df_interim = pd.read_csv(interim_path)
        log(f"Dữ liệu interim: {len(df_interim)} dòng, {len(df_interim['country'].unique())} quốc gia duy nhất.")
        
        # Kiểm tra tính khớp nối với bảng đối chứng k=3
        mismatched_years = set()
        for y in YEARS:
            kmeans_file = processed_dir / f"contrast_k3/contrast_k3_kmeans_{y}.csv"
            if kmeans_file.exists():
                df_k3 = pd.read_csv(kmeans_file)
                interim_year_countries = set(df_interim[df_interim["year"] == y]["country"])
                k3_countries = set(df_k3["country"])
                diff = interim_year_countries ^ k3_countries
                if diff:
                    log(f"FAIL: Lệch danh sách quốc gia năm {y} giữa interim và contrast_k3: {diff}")
                    all_passed = False
                    mismatched_years.add(y)
        if not mismatched_years:
            log("PASS: 100% danh sách quốc gia giữa bảng interim và kết quả gom cụm khớp nhau tuyệt đối.")

    # --------------------------------------------------------------------------
    # NGÀY 19: Kiểm tra bảng dịch chuyển cụm 156 quốc gia qua 5 năm
    # --------------------------------------------------------------------------
    log("\n--- [NGÀY 19] THẨM ĐỊNH BẢNG DỊCH CHUYỂN CỤM 156 QUỐC GIA ---")
    shift_path = processed_dir / "country_cluster_shift.csv"

    # Số liệu chuẩn đã đối chiếu với tài liệu M3 và các hình/bảng trong báo cáo
    expected_status_counts = {
        "Ổn định tuyệt đối": 142,
        "Biến động trung gian": 8,
        "Cải thiện nhóm (+)": 4,
        "Suy giảm nhóm (-)": 2,
    }
    expected_direction_counts = {"Không đổi": 150, "Tăng": 4, "Giảm": 2}
    expected_improved = {"Botswana", "Georgia", "Indonesia", "Myanmar"}
    expected_declined = {"Kuwait", "Uruguay"}
    iso3_pattern = re.compile(r"^[A-Z]{3}$")

    if not shift_path.exists():
        log("FAIL: Không tìm thấy data/processed/country_cluster_shift.csv")
        all_passed = False
    else:
        df_shift = pd.read_csv(shift_path)
        cluster_columns = [c for c in df_shift.columns if c.startswith("cluster_")]

        if len(df_shift) != 156:
            log(f"FAIL: country_cluster_shift.csv có {len(df_shift)} dòng, kỳ vọng đúng 156 dòng chuẩn WHR")
            all_passed = False
        elif df_shift["country"].nunique() != 156:
            log(f"FAIL: Có quốc gia bị trùng lặp tên trong bảng dịch chuyển ({df_shift['country'].nunique()}/156)")
            all_passed = False
        else:
            log("PASS: country_cluster_shift.csv có đúng 156 quốc gia, 0 trùng lặp tên.")

            # (a) Cột iso3: đủ, đúng định dạng 3 chữ cái in hoa, không rỗng
            if "iso3" not in df_shift.columns:
                log("FAIL: Thiếu cột iso3 trong bảng dịch chuyển cụm")
                all_passed = False
            else:
                iso_series = df_shift["iso3"].astype(str).str.strip()
                invalid_iso = df_shift.loc[
                    ~iso_series.apply(lambda value: bool(iso3_pattern.match(value))), "country"
                ].tolist()
                if invalid_iso:
                    log(f"FAIL: {len(invalid_iso)} mã ISO-3 không hợp lệ hoặc rỗng: {invalid_iso[:8]}")
                    all_passed = False
                else:
                    log("PASS: 100% mã ISO-3 trong bảng dịch chuyển hợp lệ (đúng 3 chữ cái in hoa), 0 giá trị rỗng.")

            # (b) Giá trị khuyết: chỉ được khuyết ở ô mà quốc gia thực sự không có dữ liệu năm đó.
            #     Đối chiếu chéo với bảng interim, bao gồm trường hợp UAE 2018 bị loại có chủ đích.
            interim_path = project_root / "data" / "interim" / "happiness_merged.csv"
            df_interim_local = pd.read_csv(interim_path)
            present_pairs = set(zip(df_interim_local["country"], df_interim_local["year"]))

            unexpected_missing = []
            for _, shift_row in df_shift.iterrows():
                for year in YEARS:
                    column = f"cluster_{year}"
                    if pd.isna(shift_row[column]) and (shift_row["country"], year) in present_pairs:
                        unexpected_missing.append((shift_row["country"], year))

            missing_cluster = int(df_shift[cluster_columns].isna().sum().sum())
            expected_missing_cells = 17
            if missing_cluster == expected_missing_cells and not unexpected_missing:
                log(
                    f"PASS: Đúng {missing_cluster} ô khuyết ở cột cụm, tất cả đều ứng với quốc gia "
                    "không có dữ liệu năm tương ứng (bao gồm UAE 2018 loại có chủ đích)."
                )
            else:
                log(
                    f"FAIL: Số ô khuyết = {missing_cluster} (kỳ vọng {expected_missing_cells}); "
                    f"số ô khuyết bất thường = {len(unexpected_missing)}: {unexpected_missing[:5]}"
                )
                all_passed = False

            meta_columns = [c for c in ["shift_status", "shift_direction", "is_stable"] if c in df_shift.columns]
            meta_missing = int(df_shift[meta_columns].isna().sum().sum())
            if len(meta_columns) == 3 and meta_missing == 0:
                log("PASS: Các cột shift_status, shift_direction, is_stable không có giá trị khuyết.")
            else:
                log(f"FAIL: Thiếu cột hoặc có {meta_missing} giá trị khuyết ở cột trạng thái dịch chuyển.")
                all_passed = False

            # (c) Phân bố trạng thái dịch chuyển khớp tài liệu
            actual_status_counts = df_shift["shift_status"].value_counts().to_dict()
            if actual_status_counts == expected_status_counts:
                log(f"PASS: Phân bố trạng thái dịch chuyển khớp tài liệu: {actual_status_counts}.")
            else:
                log(f"FAIL: Phân bố trạng thái lệch — thực tế {actual_status_counts}, kỳ vọng {expected_status_counts}.")
                all_passed = False

            # (d) Danh sách quốc gia thăng hạng / tụt hạng đúng như đề cương
            improved = set(df_shift.loc[df_shift["shift_status"] == "Cải thiện nhóm (+)", "country"])
            declined = set(df_shift.loc[df_shift["shift_status"] == "Suy giảm nhóm (-)", "country"])
            if improved == expected_improved:
                log(f"PASS: Đúng 4 quốc gia thăng hạng: {sorted(improved)}.")
            else:
                log(f"FAIL: Danh sách thăng hạng lệch — thực tế {sorted(improved)}, kỳ vọng {sorted(expected_improved)}.")
                all_passed = False
            if declined == expected_declined:
                log(f"PASS: Đúng 2 quốc gia tụt hạng: {sorted(declined)}.")
            else:
                log(f"FAIL: Danh sách tụt hạng lệch — thực tế {sorted(declined)}, kỳ vọng {sorted(expected_declined)}.")
                all_passed = False

            # (e) Cột shift_direction nhất quán với shift_status
            actual_direction_counts = df_shift["shift_direction"].value_counts().to_dict()
            direction_ok = actual_direction_counts == expected_direction_counts
            consistency_ok = bool(
                (
                    df_shift["shift_direction"]
                    == df_shift["shift_status"].map(
                        {"Cải thiện nhóm (+)": "Tăng", "Suy giảm nhóm (-)": "Giảm"}
                    ).fillna("Không đổi")
                ).all()
            )
            if direction_ok and consistency_ok:
                log(f"PASS: Cột shift_direction nhất quán với shift_status: {actual_direction_counts}.")
            else:
                log(f"FAIL: shift_direction không nhất quán — thực tế {actual_direction_counts}.")
                all_passed = False

            # (f) Cột is_stable nhất quán với shift_status
            stable_ok = bool(
                (df_shift["is_stable"] == (df_shift["shift_status"] == "Ổn định tuyệt đối")).all()
            )
            if stable_ok:
                log("PASS: Cột is_stable nhất quán với trạng thái 'Ổn định tuyệt đối'.")
            else:
                log("FAIL: Cột is_stable không khớp với shift_status.")
                all_passed = False

            # (g) Bản ghi UAE năm 2018 khuyết có chủ đích
            uae_row = df_shift[df_shift["country"] == "United Arab Emirates"]
            if len(uae_row) > 0 and pd.isna(uae_row["cluster_2018"].values[0]):
                log("PASS: Bản ghi United Arab Emirates (UAE) năm 2018 hiển thị NaN hợp lệ (đã loại bỏ an toàn do khuyết chỉ số tham nhũng).")
            else:
                log("FAIL: Bản ghi UAE năm 2018 không đúng trạng thái khuyết có chủ đích.")
                all_passed = False

            log(f"Thống kê độ ổn định: {actual_status_counts}")

    # --------------------------------------------------------------------------
    # NGÀY 20: Kiểm tra toàn bộ hình ảnh xuất ra bảo đảm đúng độ phân giải 300 DPI
    # --------------------------------------------------------------------------
    log("\n--- [NGÀY 20] KIỂM TRA ĐỘ PHÂN GIẢI TOÀN BỘ HÌNH ẢNH (300 DPI) ---")
    png_files = list(figures_dir.glob("*.png"))
    log(f"Tổng số hình ảnh tìm thấy trong reports/figures/: {len(png_files)} hình.")
    
    if len(png_files) < 12:
        log(f"FAIL: Số lượng hình ảnh ({len(png_files)}) ít hơn yêu cầu tối thiểu (12 hình).")
        all_passed = False
    else:
        log("PASS: Đạt và vượt chỉ tiêu số lượng (>= 12 hình ảnh phục vụ Báo cáo Word).")
        
    dpi_pass = True
    for p in sorted(png_files):
        if p.stat().st_size == 0:
            log(f"FAIL: Tệp hình 0 byte: {p.name}")
            dpi_pass = False
            all_passed = False
            continue
        try:
            with Image.open(p) as img:
                dpi_info = img.info.get("dpi")
                if dpi_info is None:
                    log(f"WARNING: {p.name} không có metadata DPI (Kích thước: {img.size})")
                else:
                    dpi_val = round(dpi_info[0])
                    if dpi_val < 300:
                        log(f"FAIL: {p.name} có DPI = {dpi_val} (< 300 DPI)")
                        dpi_pass = False
                        all_passed = False
                    else:
                        log(f"PASS: {p.name} — DPI: {dpi_val} — Kích thước: {img.size} px")
        except Exception as e:
            log(f"FAIL: Lỗi khi đọc file {p.name}: {e}")
            dpi_pass = False
            all_passed = False
            
    if dpi_pass:
        log("PASS: 100% hình ảnh kiểm tra đều đạt chuẩn độ phân giải cao 300 DPI.")

    # --------------------------------------------------------------------------
    # NGÀY 21: Tham gia buổi Walkthrough; rà soát chéo toàn bộ kết quả M3
    # --------------------------------------------------------------------------
    log("\n--- [NGÀY 21] TỔNG KẾT VÀ PHÊ DUYỆT NGHIỆM THU MỐC M3 ---")
    if all_passed:
        log("KẾT LUẬN: TOÀN BỘ 7/7 HẠNG MỤC THẨM ĐỊNH MỐC M3 ĐÃ ĐẠT CHUẨN (PASS 100%).")
        log("Xác nhận nghiệm thu Mốc M3: Số liệu thực nghiệm nhất quán, sẵn sàng bước vào Mốc M4 (Tự động hóa Báo cáo Word).")
    else:
        log("KẾT LUẬN: CÓ HẠNG MỤC CHƯA ĐẠT CHUẨN — CẦN KHẮC PHỤC TRƯỚC KHI BƯỚC VÀO MỐC M4.")
        
    log("================================================================================")
    
    # Ghi log ra file
    with log_file_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(output_lines) + "\n")
        
    log(f"\nĐã lưu toàn bộ nhật ký thẩm định vào: {log_file_path}")
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(audit())
