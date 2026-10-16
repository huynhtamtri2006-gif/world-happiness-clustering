"""
Script kiểm toán chất lượng dữ liệu & bảng mã ISO-3 — Mốc M1
Học phần: Khai thác dữ liệu (Data Mining) — Đề tài 16: World Happiness Report
Phụ trách: Ngô Quang Trung (MSSV: 2045240325)
Tài liệu căn cứ: reports/final_report/nhiem_vu_ngo_quang_trung.md (Mốc M1, Ngày 3 – Ngày 7)

Phạm vi kiểm tra:
1. [Ngày 3] Cỡ mẫu 5 năm trong dữ liệu thô: 158/157/155/156/156; không trùng quốc gia trong từng năm.
2. [Ngày 4 + Ngày 6] UAE năm 2018 khuyết corruption_perception và đã bị loại an toàn khỏi
   bảng interim; bảng interim còn đúng 781 dòng sạch, 6 đặc trưng cơ sở không khuyết thiếu.
3. [Ngày 5] Kiểm tra 100% dòng interim (781 dòng) ánh xạ thành công sang mã ISO-3 hợp lệ
   (đúng 3 chữ cái in hoa), không có giá trị None hoặc rỗng, phục vụ vẽ bản đồ Choropleth.
4. [Ngày 4] Schema interim đúng 13 cột chuẩn INTERIM_COLUMNS, đã loại sạch các cột sai số
   khảo sát (Standard Error, Confidence Interval, Whisker).

Cách chạy:
    python scripts/audit_m1_data_quality_and_iso3.py

Mã thoát (exit code):
- 0: toàn bộ hạng mục PASS, dữ liệu M1 đạt chuẩn.
- 1: có ít nhất một hạng mục FAIL, cần khắc phục trước khi chốt M1.
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import re
from pathlib import Path

import pandas as pd

# Thiết lập đường dẫn tương đối độc lập môi trường (không dùng đường dẫn tuyệt đối máy cá nhân)
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from src.data import data_loader  # noqa: E402

YEARS = [2015, 2016, 2017, 2018, 2019]

# Cỡ mẫu chuẩn của dữ liệu thô 5 năm (đã kiểm chứng ngày 3)
EXPECTED_RAW_SIZES = {2015: 158, 2016: 157, 2017: 155, 2018: 156, 2019: 156}

# Cỡ mẫu chuẩn của bảng interim sau khi loại United Arab Emirates năm 2018
EXPECTED_INTERIM_SIZES = {2015: 158, 2016: 157, 2017: 155, 2018: 155, 2019: 156}
EXPECTED_INTERIM_TOTAL = 781

# Mẫu mã ISO 3166-1 alpha-3: đúng 3 chữ cái in hoa
ISO3_PATTERN = re.compile(r"^[A-Z]{3}$")

# Từ khóa nhận diện các cột sai số khảo sát phải bị loại khỏi bảng interim
FORBIDDEN_COLUMN_KEYWORDS = ["standard error", "whisker", "confidence"]

logs_dir = project_root / "logs"
log_file_path = logs_dir / "audit_m1_quality.log"


def audit() -> int:
    output_lines = []

    def log(message: str) -> None:
        print(message)
        output_lines.append(message)

    def check(name: str, passed: bool, detail: str = "") -> bool:
        status = "PASS" if passed else "FAIL"
        log(f"{status}: {name}" + (f" — {detail}" if detail else ""))
        return passed

    all_passed = True

    log("================================================================================")
    log("BÁO CÁO KIỂM TOÁN CHẤT LƯỢNG DỮ LIỆU & BẢNG MÃ ISO-3 — MỐC M1")
    log("Người thực hiện: Ngô Quang Trung (MSSV: 2045240325)")
    log("Đề tài 16: Phân nhóm quốc gia theo các yếu tố hạnh phúc (World Happiness Report)")
    log("Thời gian thực hiện: Mốc M1 (Ngày 3 – Ngày 7)")
    log("================================================================================")

    # --------------------------------------------------------------------------
    # MỤC 1 (Ngày 3): Cỡ mẫu và tính duy nhất của dữ liệu thô 5 năm
    # --------------------------------------------------------------------------
    log("\n--- [MỤC 1 — NGÀY 3] CỠ MẪU VÀ TÍNH DUY NHẤT CỦA DỮ LIỆU THÔ 5 NĂM ---")
    raw_data = data_loader.load_raw_data(years=YEARS)

    raw_total = 0
    for year in YEARS:
        df_year = raw_data[year]
        n_rows = len(df_year)
        raw_total += n_rows
        expected = EXPECTED_RAW_SIZES[year]
        if not check(
            f"Cỡ mẫu dữ liệu thô năm {year}",
            n_rows == expected,
            f"{n_rows} dòng (kỳ vọng {expected})",
        ):
            all_passed = False

    log(f"Tổng số dòng thô 5 năm: {raw_total} dòng.")

    raw_duplicated = False
    for year in YEARS:
        n_dup = int(raw_data[year]["country"].duplicated().sum())
        if n_dup > 0:
            raw_duplicated = True
            if not check(f"Trùng quốc gia năm {year}", False, f"{n_dup} dòng trùng tên"):
                all_passed = False
    if not raw_duplicated:
        check("Không có quốc gia trùng lặp trong từng năm dữ liệu thô", True, "0 trùng lặp")

    # Kiểm tra phân bố giá trị khuyết của 6 đặc trưng cơ sở trên toàn bộ dữ liệu thô
    raw_nan_locations = []
    for year in YEARS:
        df_year = raw_data[year]
        nan_mask = df_year[data_loader.CORE_FEATURES].isna()
        for idx in df_year[nan_mask.any(axis=1)].index:
            for column in data_loader.CORE_FEATURES:
                if pd.isna(df_year.loc[idx, column]):
                    raw_nan_locations.append((year, df_year.loc[idx, "country"], column))

    nan_detail = ""
    if raw_nan_locations:
        nan_detail = "; ".join(f"{y} - {c} - {col}" for y, c, col in raw_nan_locations)
    if not check(
        "Giá trị khuyết của 6 đặc trưng cơ sở trong dữ liệu thô",
        len(raw_nan_locations) == 1
        and raw_nan_locations[0] == (2018, "United Arab Emirates", "corruption_perception"),
        f"đúng 1 giá trị khuyết duy nhất: {nan_detail}" if raw_nan_locations
        else "0 giá trị khuyết (không đúng kỳ vọng)",
    ):
        all_passed = False

    # --------------------------------------------------------------------------
    # MỤC 2 (Ngày 4 + Ngày 6): Loại trừ UAE 2018 và cỡ mẫu interim 781 dòng
    # --------------------------------------------------------------------------
    log("\n--- [MỤC 2 — NGÀY 4 + NGÀY 6] LOẠI TRỪ UAE 2018 VÀ CỠ MẪU INTERIM 781 DÒNG ---")

    uae_2018_raw = raw_data[2018][raw_data[2018]["country"] == "United Arab Emirates"]
    if not check(
        "Bản ghi UAE năm 2018 tồn tại trong dữ liệu thô",
        len(uae_2018_raw) == 1,
        f"{len(uae_2018_raw)} dòng",
    ):
        all_passed = False
    if not check(
        "UAE năm 2018 khuyết đúng cột corruption_perception",
        len(uae_2018_raw) == 1 and pd.isna(uae_2018_raw.iloc[0]["corruption_perception"]),
        "corruption_perception = NaN",
    ):
        all_passed = False

    interim_path = project_root / "data" / "interim" / "happiness_merged.csv"
    if not check("Tệp interim happiness_merged.csv tồn tại", interim_path.exists(), str(interim_path)):
        all_passed = False
        interim_df = pd.DataFrame()
    else:
        # Dùng hàm nạp chuẩn trong src/data/data_loader.py (tự dựng lại từ raw nếu thiếu tệp)
        interim_df = data_loader.load_interim(interim_path)

        if not check(
            "Tổng số dòng bảng interim",
            len(interim_df) == EXPECTED_INTERIM_TOTAL,
            f"{len(interim_df)} dòng (kỳ vọng {EXPECTED_INTERIM_TOTAL} dòng sạch)",
        ):
            all_passed = False

        interim_counts = interim_df.groupby("year").size().to_dict()
        count_detail = ", ".join(f"{y}: {interim_counts.get(y, 0)}" for y in YEARS)
        if not check(
            "Cỡ mẫu từng năm trong bảng interim",
            all(interim_counts.get(y) == EXPECTED_INTERIM_SIZES[y] for y in YEARS),
            f"{count_detail} (kỳ vọng 158/157/155/155/156)",
        ):
            all_passed = False

        uae_2018_interim = interim_df[
            (interim_df["year"] == 2018) & (interim_df["country"] == "United Arab Emirates")
        ]
        if not check(
            "Bản ghi UAE năm 2018 đã bị loại an toàn khỏi bảng interim",
            len(uae_2018_interim) == 0,
            "0 dòng UAE 2018 tồn tại trong interim",
        ):
            all_passed = False

        interim_feature_nan = int(interim_df[data_loader.CORE_FEATURES].isna().sum().sum())
        if not check(
            "6 đặc trưng cơ sở trong bảng interim không khuyết thiếu",
            interim_feature_nan == 0,
            f"{interim_feature_nan} giá trị khuyết",
        ):
            all_passed = False

        # ----------------------------------------------------------------------
        # MỤC 3 (Ngày 5): Ánh xạ 100% dòng interim sang mã ISO-3 hợp lệ
        # ----------------------------------------------------------------------
        log("\n--- [MỤC 3 — NGÀY 5] ÁNH XẠ MÃ ISO-3 PHỤC VỤ BẢN ĐỒ CHOROPLETH ---")

        if "iso_alpha" not in interim_df.columns:
            check("Cột iso_alpha tồn tại trong bảng interim", False, "không tìm thấy cột")
            all_passed = False
        else:
            iso_series = interim_df["iso_alpha"]
            n_missing = int(iso_series.isna().sum())
            n_empty = int((iso_series.astype(str).str.strip() == "").sum())

            if not check(
                "Không có mã ISO-3 bị None hoặc rỗng",
                n_missing == 0 and n_empty == 0,
                f"{n_missing} giá trị None, {n_empty} giá trị rỗng",
            ):
                all_passed = False

            invalid_mask = ~iso_series.astype(str).apply(lambda value: bool(ISO3_PATTERN.match(value)))
            n_invalid = int(invalid_mask.sum())
            invalid_examples = interim_df.loc[invalid_mask, ["country", "year", "iso_alpha"]].head(5)
            if not check(
                "100% mã ISO-3 hợp lệ (đúng 3 chữ cái in hoa)",
                n_invalid == 0,
                f"{n_invalid} mã không hợp lệ"
                if n_invalid
                else f"{len(interim_df)}/{len(interim_df)} dòng đạt mẫu [A-Z]{{3}}",
            ):
                all_passed = False
                if n_invalid:
                    log(f"  Ví dụ mã không hợp lệ:\n{invalid_examples.to_string(index=False)}")

            n_iso_per_country = interim_df.groupby("country")["iso_alpha"].nunique()
            multi_iso = n_iso_per_country[n_iso_per_country > 1]
            if not check(
                "Mỗi quốc gia chỉ ánh xạ về một mã ISO-3 duy nhất xuyên 5 năm",
                len(multi_iso) == 0,
                "0 quốc gia bị gán nhiều mã"
                if len(multi_iso) == 0
                else f"{len(multi_iso)} quốc gia bị gán nhiều mã: {list(multi_iso.index)}",
            ):
                all_passed = False

            # Đối chiếu cột iso_alpha trong CSV với hàm tra cứu chuẩn (chống chỉnh sửa thủ công)
            mismatched = []
            for country, iso_value in interim_df.groupby("country")["iso_alpha"].first().items():
                if data_loader.country_to_iso3(country) != iso_value:
                    mismatched.append((country, iso_value, data_loader.country_to_iso3(country)))
            if not check(
                "Mã ISO-3 khớp với hàm tra cứu country_to_iso3",
                len(mismatched) == 0,
                f"{len(mismatched)} quốc gia lệch" if mismatched else "khớp 100%",
            ):
                all_passed = False

            log(
                f"Thông tin: interim có {interim_df['country'].nunique()} quốc gia duy nhất "
                f"trên {len(interim_df)} dòng; {iso_series.nunique()} mã ISO-3 phân biệt."
            )

        # ----------------------------------------------------------------------
        # MỤC 4 (Ngày 4): Schema interim đúng 13 cột, không lẫn cột sai số khảo sát
        # ----------------------------------------------------------------------
        log("\n--- [MỤC 4 — NGÀY 4] SCHEMA INTERIM VÀ LOẠI BỎ CỘT SAI SỐ KHẢO SÁT ---")

        actual_columns = list(interim_df.columns)
        expected_columns = list(data_loader.INTERIM_COLUMNS)
        if not check(
            "Schema interim đúng 13 cột chuẩn INTERIM_COLUMNS",
            actual_columns == expected_columns,
            f"thực tế {len(actual_columns)} cột"
            if actual_columns != expected_columns
            else f"đúng {len(expected_columns)} cột theo thứ tự chuẩn",
        ):
            all_passed = False
            if actual_columns != expected_columns:
                log(f"  Cột thực tế: {actual_columns}")
                log(f"  Cột kỳ vọng: {expected_columns}")

        forbidden_columns = [
            column
            for column in actual_columns
            if any(keyword in str(column).lower() for keyword in FORBIDDEN_COLUMN_KEYWORDS)
        ]
        if not check(
            "Không còn cột sai số khảo sát (Standard Error / Whisker / Confidence Interval)",
            len(forbidden_columns) == 0,
            "0 cột sai số"
            if not forbidden_columns
            else f"còn cột: {forbidden_columns}",
        ):
            all_passed = False

    # --------------------------------------------------------------------------
    # TỔNG KẾT VÀ GHI LOG
    # --------------------------------------------------------------------------
    log("\n================================================================================")
    if all_passed:
        log("KẾT LUẬN: TOÀN BỘ HẠNG MỤC KIỂM TOÁN MỐC M1 ĐÃ ĐẠT CHUẨN (PASS 100%).")
        log("Xác nhận: Cỡ mẫu 158/157/155/156/156 đúng; UAE 2018 đã loại an toàn (interim 781 dòng);")
        log("mã ISO-3 của 781 dòng hợp lệ 100%, sẵn sàng cho bản đồ Choropleth.")
    else:
        log("KẾT LUẬN: CÓ HẠNG MỤC CHƯA ĐẠT CHUẨN — CẦN KHẮC PHỤC TRƯỚC KHI CHỐT MỐC M1.")
    log("================================================================================")

    # Ghi toàn bộ nhật ký kiểm toán ra logs/audit_m1_quality.log
    logs_dir.mkdir(parents=True, exist_ok=True)
    with log_file_path.open("w", encoding="utf-8") as log_file:
        log_file.write("\n".join(output_lines) + "\n")

    log(f"\nĐã lưu toàn bộ nhật ký kiểm toán vào: {log_file_path}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(audit())
