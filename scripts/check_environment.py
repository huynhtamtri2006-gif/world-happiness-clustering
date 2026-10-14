"""
Script kiểm tra nhanh môi trường cài đặt cho máy chấm và buổi demo
(Mốc M2 — Ngày 11, nhiệm vụ Hà Mạnh Trường: Kiểm soát chất lượng & Tối ưu hiệu năng).

Phạm vi kiểm tra:
1. Phiên bản Python >= 3.10.
2. Đầy đủ các gói phụ thuộc trong requirements.txt (đúng phiên bản ghim).
3. Dữ liệu đầu vào: 5 tệp raw 2015–2019 và tệp interim happiness_merged.csv.
4. Smoke test nạp các module src.data, src.features, src.models và các API then chốt.

Cách chạy:
    python scripts/check_environment.py

Mã thoát (exit code):
- 0: tất cả hạng mục PASS, môi trường đạt chuẩn chạy pipeline.
- 1: có ít nhất một hạng mục FAIL, cần xử lý trước khi demo/nộp bài.
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import re
from importlib import import_module, metadata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

MIN_PYTHON = (3, 10)
RAW_YEARS = [2015, 2016, 2017, 2018, 2019]
INTERIM_PATH = ROOT / "data" / "interim" / "happiness_merged.csv"

# 6 đặc trưng cơ sở dùng để gom cụm (không gồm điểm/thứ hạng hạnh phúc).
FEATURE_COLUMNS = [
    "gdp_per_capita",
    "social_support",
    "healthy_life_expectancy",
    "freedom",
    "generosity",
    "corruption_perception",
]

# Smoke test: mỗi module phải nạp được và phơi ra đủ các API then chốt.
SMOKE_TESTS = {
    "src.data": ["load_raw_data", "load_year_data", "standardize_columns"],
    "src.features": ["scale_features", "apply_pca", "SimplePCA"],
    "src.models": [
        "euclidean_distance",
        "SimpleKMeans",
        "SimpleHierarchicalClustering",
        "SimpleDBSCAN",
    ],
}

failures = []


def check(name, passed, details=""):
    """In kết quả PASS/FAIL của một hạng mục và ghi nhận nếu thất bại."""
    status = "PASS" if passed else "FAIL"
    print(f"{status}: {name}" + (f" — {details}" if details else ""))
    if not passed:
        failures.append(name)


def parse_requirements(path):
    """Đọc requirements.txt -> danh sách (tên gói, phiên bản ghim hoặc None)."""
    requirements = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r"^([A-Za-z0-9_.\-]+)==(.+)$", line)
        if match:
            requirements.append((match.group(1), match.group(2).strip()))
        else:
            requirements.append((line, None))
    return requirements


print("=== KIỂM TRA MÔI TRƯỜNG CÀI ĐẶT — ĐỀ TÀI 16: WORLD HAPPINESS REPORT ===")
print(f"Trình thông dịch: {sys.executable}")
print()

# 1. Phiên bản Python
check(
    "Python >= 3.10",
    sys.version_info >= MIN_PYTHON,
    f"đang dùng Python {sys.version.split()[0]}",
)

# 2. Các gói phụ thuộc trong requirements.txt
requirements_path = ROOT / "requirements.txt"
if not requirements_path.exists():
    check("Tệp requirements.txt tồn tại", False, "không tìm thấy requirements.txt")
else:
    for package, pinned_version in parse_requirements(requirements_path):
        try:
            installed_version = metadata.version(package)
        except metadata.PackageNotFoundError:
            check(f"Gói {package}", False, "chưa được cài đặt")
            continue

        if pinned_version is None:
            check(f"Gói {package}", True, f"phiên bản {installed_version}")
        elif installed_version == pinned_version:
            check(f"Gói {package}", True, installed_version)
        else:
            check(
                f"Gói {package}",
                False,
                f"cài đặt {installed_version}, yêu cầu {pinned_version}",
            )

# 3. Dữ liệu đầu vào
for year in RAW_YEARS:
    raw_path = ROOT / "data" / "raw" / f"{year}.csv"
    exists = raw_path.exists()
    size = raw_path.stat().st_size if exists else 0
    check(
        f"Dữ liệu raw {year}.csv",
        exists and size > 0,
        f"{size} bytes" if exists else "không tìm thấy tệp",
    )

if not INTERIM_PATH.exists():
    check("Dữ liệu interim happiness_merged.csv", False, "không tìm thấy tệp")
else:
    try:
        import pandas as pd

        interim_df = pd.read_csv(INTERIM_PATH)
        required_columns = ["country", "year"] + FEATURE_COLUMNS
        missing_columns = [
            column for column in required_columns
            if column not in interim_df.columns
        ]
        check(
            "Dữ liệu interim: đủ cột bắt buộc",
            not missing_columns,
            f"{len(interim_df)} dòng, {len(interim_df.columns)} cột"
            if not missing_columns
            else f"thiếu cột: {', '.join(missing_columns)}",
        )

        if not missing_columns:
            missing_values = int(interim_df[FEATURE_COLUMNS].isna().sum().sum())
            check(
                "Dữ liệu interim: 6 đặc trưng không khuyết thiếu",
                missing_values == 0,
                "đủ giá trị" if missing_values == 0
                else f"khuyết {missing_values} giá trị",
            )
    except Exception as error:
        check(
            "Dữ liệu interim: đọc bằng pandas",
            False,
            f"{type(error).__name__}: {error}",
        )

# 4. Smoke test nạp các module chính
for module_name, required_attributes in SMOKE_TESTS.items():
    try:
        module = import_module(module_name)
    except Exception as error:
        check(
            f"Smoke test nạp {module_name}",
            False,
            f"{type(error).__name__}: {error}",
        )
        continue

    missing_attributes = [
        attribute for attribute in required_attributes
        if not hasattr(module, attribute)
    ]
    check(
        f"Smoke test nạp {module_name}",
        not missing_attributes,
        f"nạp thành công, {len(required_attributes)} API then chốt"
        if not missing_attributes
        else f"thiếu API: {', '.join(missing_attributes)}",
    )

# 5. Tổng kết và mã thoát chuẩn
print()
if failures:
    print(f"Tổng kết: {len(failures)} hạng mục FAIL: {failures}")
    raise SystemExit(1)

print("Tổng kết: môi trường đạt chuẩn — tất cả kiểm tra PASS.")
raise SystemExit(0)
