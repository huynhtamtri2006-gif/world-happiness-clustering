"""
Module nạp và tiền xử lý dữ liệu cho World Happiness Report (2015 - 2019).
Cung cấp các hàm chuẩn hóa tên cột, đồng bộ tên quốc gia, tra cứu mã ISO-3,
xây dựng và nạp bộ dữ liệu trung gian chuẩn (interim).
"""

from pathlib import Path
from typing import Dict, List, Optional, Union
import numpy as np
import pandas as pd

# Đường dẫn mặc định tương đối chuẩn
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DEFAULT_INTERIM_DIR = PROJECT_ROOT / "data" / "interim"
DEFAULT_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# 6 đặc trưng cơ sở đo lường chất lượng cuộc sống (theo CONTEXT.md và Đề tài 16)
CORE_FEATURES = [
    "gdp_per_capita",
    "social_support",
    "healthy_life_expectancy",
    "freedom",
    "corruption_perception",
    "generosity",
]

# Danh sách 13 cột chuẩn của bảng dữ liệu trung gian (interim)
INTERIM_COLUMNS = [
    "country",
    "region",
    "happiness_rank",
    "happiness_score",
    "gdp_per_capita",
    "social_support",
    "healthy_life_expectancy",
    "freedom",
    "corruption_perception",
    "generosity",
    "dystopia_residual",
    "year",
    "iso_alpha",
]

# Bảng quy đổi tên cột qua các năm về định dạng chuẩn thống nhất (snake_case)
COLUMN_MAPPING = {
    # 2015 & 2016
    "Country": "country",
    "Region": "region",
    "Happiness Rank": "happiness_rank",
    "Happiness Score": "happiness_score",
    "Economy (GDP per Capita)": "gdp_per_capita",
    "Family": "social_support",
    "Health (Life Expectancy)": "healthy_life_expectancy",
    "Freedom": "freedom",
    "Trust (Government Corruption)": "corruption_perception",
    "Generosity": "generosity",
    "Dystopia Residual": "dystopia_residual",

    # 2017
    "Happiness.Rank": "happiness_rank",
    "Happiness.Score": "happiness_score",
    "Economy..GDP.per.Capita.": "gdp_per_capita",
    "Health..Life.Expectancy.": "healthy_life_expectancy",
    "Trust..Government.Corruption.": "corruption_perception",
    "Dystopia.Residual": "dystopia_residual",

    # 2018 & 2019
    "Overall rank": "happiness_rank",
    "Country or region": "country",
    "Score": "happiness_score",
    "GDP per capita": "gdp_per_capita",
    "Social support": "social_support",
    "Healthy life expectancy": "healthy_life_expectancy",
    "Freedom to make life choices": "freedom",
    "Perceptions of corruption": "corruption_perception",
}

# Từ điển chuẩn hóa tên quốc gia bị lệch giữa các năm
COUNTRY_NAME_FIXES = {
    "Macedonia": "North Macedonia",
    "Swaziland": "Eswatini",
    "Taiwan Province of China": "Taiwan",
    "Hong Kong S.A.R., China": "Hong Kong",
    "Trinidad & Tobago": "Trinidad and Tobago",
    "Northern Cyprus": "North Cyprus",
    "Somaliland region": "Somaliland",
    "Somaliland Region": "Somaliland",
}

# Các ngoại lệ ghi đè mã ISO 3166-1 alpha-3
COUNTRY_ISO3_OVERRIDES = {
    "Kosovo": "XKX",
    "North Cyprus": "CYP",
    "Somaliland": "SOM",
}

# Bảng tra cứu toàn diện mã ISO 3166-1 alpha-3 cho 164 quốc gia trong WHR (2015-2019)
ISO3_MAP = {
    "Afghanistan": "AFG", "Albania": "ALB", "Algeria": "DZA", "Angola": "AGO",
    "Argentina": "ARG", "Armenia": "ARM", "Australia": "AUS", "Austria": "AUT",
    "Azerbaijan": "AZE", "Bahrain": "BHR", "Bangladesh": "BGD", "Belarus": "BLR",
    "Belgium": "BEL", "Belize": "BLZ", "Benin": "BEN", "Bhutan": "BTN",
    "Bolivia": "BOL", "Bosnia and Herzegovina": "BIH", "Botswana": "BWA", "Brazil": "BRA",
    "Bulgaria": "BGR", "Burkina Faso": "BFA", "Burundi": "BDI", "Cambodia": "KHM",
    "Cameroon": "CMR", "Canada": "CAN", "Central African Republic": "CAF", "Chad": "TCD",
    "Chile": "CHL", "China": "CHN", "Colombia": "COL", "Comoros": "COM",
    "Congo (Brazzaville)": "COG", "Congo (Kinshasa)": "COD", "Costa Rica": "CRI",
    "Croatia": "HRV", "Cyprus": "CYP", "Czech Republic": "CZE", "Denmark": "DNK",
    "Djibouti": "DJI", "Dominican Republic": "DOM", "Ecuador": "ECU", "Egypt": "EGY",
    "El Salvador": "SLV", "Estonia": "EST", "Eswatini": "SWZ", "Ethiopia": "ETH",
    "Finland": "FIN", "France": "FRA", "Gabon": "GAB", "Gambia": "GMB",
    "Georgia": "GEO", "Germany": "DEU", "Ghana": "GHA", "Greece": "GRC",
    "Guatemala": "GTM", "Guinea": "GIN", "Haiti": "HTI", "Honduras": "HND",
    "Hong Kong": "HKG", "Hungary": "HUN", "Iceland": "ISL", "India": "IND",
    "Indonesia": "IDN", "Iran": "IRN", "Iraq": "IRQ", "Ireland": "IRL",
    "Israel": "ISR", "Italy": "ITA", "Ivory Coast": "CIV", "Jamaica": "JAM",
    "Japan": "JPN", "Jordan": "JOR", "Kazakhstan": "KAZ", "Kenya": "KEN",
    "Kosovo": "XKX", "Kuwait": "KWT", "Kyrgyzstan": "KGZ", "Laos": "LAO",
    "Latvia": "LVA", "Lebanon": "LBN", "Lesotho": "LSO", "Liberia": "LBR",
    "Libya": "LBY", "Lithuania": "LTU", "Luxembourg": "LUX", "Madagascar": "MDG",
    "Malawi": "MWI", "Malaysia": "MYS", "Mali": "MLI", "Malta": "MLT",
    "Mauritania": "MRT", "Mauritius": "MUS", "Mexico": "MEX", "Moldova": "MDA",
    "Mongolia": "MNG", "Montenegro": "MNE", "Morocco": "MAR", "Mozambique": "MOZ",
    "Myanmar": "MMR", "Namibia": "NAM", "Nepal": "NPL", "Netherlands": "NLD",
    "New Zealand": "NZL", "Nicaragua": "NIC", "Niger": "NER", "Nigeria": "NGA",
    "North Cyprus": "CYP", "North Macedonia": "MKD", "Norway": "NOR", "Oman": "OMN",
    "Pakistan": "PAK", "Palestinian Territories": "PSE", "Panama": "PAN", "Paraguay": "PRY",
    "Peru": "PER", "Philippines": "PHL", "Poland": "POL", "Portugal": "PRT",
    "Puerto Rico": "PRI", "Qatar": "QAT", "Romania": "ROU", "Russia": "RUS",
    "Rwanda": "RWA", "Saudi Arabia": "SAU", "Senegal": "SEN", "Serbia": "SRB",
    "Sierra Leone": "SLE", "Singapore": "SGP", "Slovakia": "SVK", "Slovenia": "SVN",
    "Somalia": "SOM", "Somaliland": "SOM", "South Africa": "ZAF", "South Korea": "KOR",
    "South Sudan": "SSD", "Spain": "ESP", "Sri Lanka": "LKA", "Sudan": "SDN",
    "Suriname": "SUR", "Sweden": "SWE", "Switzerland": "CHE", "Syria": "SYR",
    "Taiwan": "TWN", "Tajikistan": "TJK", "Tanzania": "TZA", "Thailand": "THA",
    "Togo": "TGO", "Trinidad and Tobago": "TTO", "Tunisia": "TUN", "Turkey": "TUR",
    "Turkmenistan": "TKM", "Uganda": "UGA", "Ukraine": "UKR", "United Arab Emirates": "ARE",
    "United Kingdom": "GBR", "United States": "USA", "Uruguay": "URY", "Uzbekistan": "UZB",
    "Venezuela": "VEN", "Vietnam": "VNM", "Yemen": "YEM", "Zambia": "ZMB", "Zimbabwe": "ZWE"
}

# Bổ sung mapping khu vực địa lý cho các quốc gia không có trong 2015-2016
REGION_FALLBACKS = {
    "Gambia": "Sub-Saharan Africa",
}


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Đổi tên các cột của DataFrame về chuẩn snake_case thống nhất theo COLUMN_MAPPING.
    """
    rename_dict = {col: COLUMN_MAPPING[col] for col in df.columns if col in COLUMN_MAPPING}
    return df.rename(columns=rename_dict)


def harmonize_country_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Đồng bộ hóa tên quốc gia bị lệch giữa các năm (như Macedonia -> North Macedonia).
    """
    df_copy = df.copy()
    target_cols = [col for col in ["country", "Country", "Country or region"] if col in df_copy.columns]
    for col in target_cols:
        df_copy[col] = df_copy[col].replace(COUNTRY_NAME_FIXES)
    return df_copy


def country_to_iso3(country_name: str) -> str:
    """
    Tra cứu mã ISO 3166-1 alpha-3 từ tên quốc gia.
    Ưu tiên tra cứu COUNTRY_ISO3_OVERRIDES rồi đến ISO3_MAP.
    """
    if not country_name or not isinstance(country_name, str):
        return ""
    name = country_name.strip()
    # Chuẩn hóa nếu tên cũ chưa sửa
    if name in COUNTRY_NAME_FIXES:
        name = COUNTRY_NAME_FIXES[name]
    if name in COUNTRY_ISO3_OVERRIDES:
        return COUNTRY_ISO3_OVERRIDES[name]
    return ISO3_MAP.get(name, "")


def load_year_data(year: int, raw_dir: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """
    Tải dữ liệu của một năm cụ thể và gắn thêm cột 'year'.
    """
    raw_path = Path(raw_dir) if raw_dir else DEFAULT_RAW_DIR
    file_path = raw_path / f"{year}.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu: {file_path}")

    df = pd.read_csv(file_path)
    df = standardize_columns(df)
    df = harmonize_country_names(df)
    df["year"] = year
    return df


def load_raw_data(
    years: List[int] = [2015, 2016, 2017, 2018, 2019],
    raw_dir: Optional[Union[str, Path]] = None
) -> Dict[int, pd.DataFrame]:
    """
    Tải toàn bộ dữ liệu thô các năm và trả về dictionary {year: df}.
    """
    data_dict = {}
    for y in years:
        data_dict[y] = load_year_data(y, raw_dir=raw_dir)
    return data_dict


def build_interim_dataset(
    years: List[int] = [2015, 2016, 2017, 2018, 2019],
    raw_dir: Optional[Union[str, Path]] = None,
    output_path: Optional[Union[str, Path]] = None
) -> pd.DataFrame:
    """
    Xây dựng bộ dữ liệu trung gian chuẩn (interim) hợp nhất 5 năm (2015-2019).

    Các bước xử lý:
    1. Đọc dữ liệu từng năm từ data/raw/{year}.csv.
    2. Chuẩn hóa tên cột snake_case và đồng bộ tên quốc gia.
    3. Loại bỏ các cột sai số đo lường khảo sát (Standard Error, Whisker, CI).
    4. Loại bỏ bản ghi United Arab Emirates (UAE) năm 2018 do thiếu corruption_perception.
    5. Điền cột region cho các năm 2017-2019 dựa vào dữ liệu 2015-2016 và REGION_FALLBACKS.
    6. Tính toán dystopia_residual nếu năm đó không có sẵn.
    7. Bổ sung mã ISO 3166-1 alpha-3 (iso_alpha) cho từng quốc gia.
    8. Giữ đúng 13 cột theo INTERIM_COLUMNS và lưu ra tệp happiness_merged.csv.
    """
    raw_path = Path(raw_dir) if raw_dir else DEFAULT_RAW_DIR
    out_file = Path(output_path) if output_path else DEFAULT_INTERIM_DIR / "happiness_merged.csv"

    # Bước 1: Nạp và chuẩn hóa dữ liệu từng năm
    dfs = []
    region_map: Dict[str, str] = dict(REGION_FALLBACKS)

    for y in sorted(years):
        df_y = load_year_data(y, raw_dir=raw_path)

        # Thu thập ánh xạ region từ năm 2015-2016
        if "region" in df_y.columns:
            valid_regions = df_y.dropna(subset=["country", "region"])
            for _, row in valid_regions.iterrows():
                region_map[row["country"]] = row["region"]

        dfs.append(df_y)

    # Bước 2: Ghép các năm lại
    merged_df = pd.concat(dfs, ignore_index=True)

    # Bước 3: Loại bỏ mẫu UAE 2018 do khuyết thiếu hoàn toàn corruption_perception
    uae_2018_mask = (merged_df["year"] == 2018) & (merged_df["country"] == "United Arab Emirates")
    merged_df = merged_df[~uae_2018_mask].copy()

    # Bước 4: Điền khu vực địa lý (region) cho các năm thiếu
    if "region" not in merged_df.columns:
        merged_df["region"] = np.nan
    merged_df["region"] = merged_df["region"].fillna(merged_df["country"].map(region_map))

    # Bước 5: Tính toán dystopia_residual nếu bị thiếu
    if "dystopia_residual" not in merged_df.columns:
        merged_df["dystopia_residual"] = np.nan

    missing_residual = merged_df["dystopia_residual"].isna()
    if missing_residual.any():
        calculated_res = merged_df["happiness_score"] - merged_df[CORE_FEATURES].sum(axis=1)
        merged_df.loc[missing_residual, "dystopia_residual"] = calculated_res.loc[missing_residual].round(5)

    # Bước 6: Thêm mã ISO-3
    merged_df["iso_alpha"] = merged_df["country"].apply(country_to_iso3)

    # Bước 7: Chỉ lọc đúng 13 cột chuẩn theo INTERIM_COLUMNS
    # Đảm bảo các cột sai số mẫu (Standard Error, Whisker, CI) bị loại bỏ hoàn toàn
    interim_df = merged_df[INTERIM_COLUMNS].copy()

    # Đảm bảo kiểu dữ liệu chuẩn
    interim_df["happiness_rank"] = interim_df["happiness_rank"].astype(int)
    interim_df["year"] = interim_df["year"].astype(int)

    # Bước 8: Ghi ra đĩa
    out_file.parent.mkdir(parents=True, exist_ok=True)
    interim_df.to_csv(out_file, index=False, encoding="utf-8")

    return interim_df


def load_interim(interim_path: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """
    Nạp bảng dữ liệu trung gian chuẩn data/interim/happiness_merged.csv.
    Nếu chưa tồn tại, tự động xây dựng từ dữ liệu thô.
    """
    path = Path(interim_path) if interim_path else DEFAULT_INTERIM_DIR / "happiness_merged.csv"
    if not path.exists():
        return build_interim_dataset(output_path=path)
    return pd.read_csv(path, encoding="utf-8")


def load_processed(
    filename: str,
    processed_dir: Optional[Union[str, Path]] = None
) -> pd.DataFrame:
    """
    Nạp dữ liệu đã qua xử lý từ thư mục data/processed/.
    """
    proc_dir = Path(processed_dir) if processed_dir else DEFAULT_PROCESSED_DIR
    file_path = proc_dir / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu đã xử lý: {file_path}")
    return pd.read_csv(file_path, encoding="utf-8")
