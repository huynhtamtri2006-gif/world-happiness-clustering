"""
Script kiểm thử trực quan hóa độc lập — Mốc M2
Học phần: Khai thác dữ liệu (Data Mining) — Đề tài 16: World Happiness Report
Phụ trách: Ngô Quang Trung (MSSV: 2045240325)
Tài liệu căn cứ: reports/final_report/nhiem_vu_ngo_quang_trung.md (Mốc M2, Ngày 8 – Ngày 14)

Phạm vi kiểm thử:
1. Sự tồn tại và export của toàn bộ 9 hàm trong src/visualization/plots.py.
2. Gọi thử nghiệm lần lượt từng hàm vẽ trên dữ liệu interim thật
   (data/interim/happiness_merged.csv, dùng src.data.data_loader.load_interim()).
3. Xuất ảnh test vào thư mục tạm .scratch/_test_plots/ và kiểm tra:
   - Tệp PNG được tạo thành công, kích thước > 0 bytes.
   - Metadata DPI của tệp đạt >= 300 (đọc trực tiếp bằng Pillow).
4. Kiểm tra plot_dendrogram trên ma trận liên kết Ward, gồm cả chế độ cắt cây
   (truncate_mode="lastp").

Cách chạy:
    python scripts/audit_m2_visualization_plots.py

Mã thoát (exit code):
- 0: toàn bộ bài test PASS, module trực quan hóa đạt chuẩn M2.
- 1: có ít nhất một bài test FAIL, cần khắc phục.
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from pathlib import Path

import matplotlib

# Dùng backend không cần cửa sổ đồ họa để chạy được cả trên máy chấm headless.
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from PIL import Image  # noqa: E402

# Thiết lập đường dẫn tương đối độc lập môi trường (không dùng đường dẫn tuyệt đối máy cá nhân)
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from src.data import data_loader  # noqa: E402
from src.features import feature_engineering  # noqa: E402
from src.models import clustering  # noqa: E402
from src.visualization import plots  # noqa: E402

TEST_OUTPUT_DIR = project_root / ".scratch" / "_test_plots"
LOG_DIR = project_root / "logs"
LOG_FILE = LOG_DIR / "audit_m2_plots.log"
MIN_DPI = 300

# Danh sách 9 hàm trực quan hóa cần kiểm thử (7 hàm theo checklist M2 + 2 hàm còn lại).
EXPECTED_FUNCTIONS = [
    "plot_feature_distributions",
    "plot_correlation_heatmap",
    "plot_outliers_boxplot",
    "plot_elbow_silhouette",
    "plot_clusters_2d",
    "plot_cluster_radar",
    "plot_happiness_score_by_cluster",
    "plot_cluster_profiles_bar",
    "plot_dendrogram",
]


def load_metrics_table(features, df_2019) -> pd.DataFrame:
    """
    Chuẩn bị bảng metric (k, inertia, silhouette) cho plot_elbow_silhouette.

    Ưu tiên đọc bảng khảo sát k có sẵn (reports/tables/k_sensitivity_by_year.csv)
    để không phải tính lại; nếu thiếu thì tự tính bằng find_optimal_k_kmeans trên
    dữ liệu năm 2019 đã chuẩn hóa.
    """
    sensitivity_path = project_root / "reports" / "tables" / "k_sensitivity_by_year.csv"
    if sensitivity_path.exists():
        table = pd.read_csv(sensitivity_path)
        table_2019 = table[table["year"] == 2019][["k", "inertia", "silhouette"]]
        if not table_2019.empty:
            return table_2019.reset_index(drop=True)

    X_scaled, _ = feature_engineering.scale_features(df_2019, features, method="standard")
    return clustering.find_optimal_k_kmeans(X_scaled, k_range=range(2, 10), random_state=42)


def build_dendrogram_payload(features, df_2019):
    """
    Tạo ma trận liên kết Ward trên một mẫu nhỏ để vẽ dendrogram.

    Dùng 40 quốc gia đầu của năm 2019 và gộp đến 1 cụm (k=1) để thu được cây đầy đủ
    gồm 39 dòng, kèm nhãn tên quốc gia cho các lá.
    """
    sample = df_2019.head(40).reset_index(drop=True)
    X_sample, _ = feature_engineering.scale_features(sample, features, method="standard")
    _, ward_model = clustering.run_hierarchical(X_sample, n_clusters=1)
    linkage_matrix = np.array(
        [
            [record["left"], record["right"], record["distance"], record["size"]]
            for record in ward_model.merge_history
        ],
        dtype=float,
    )
    return linkage_matrix, sample["country"].tolist()


def build_test_data():
    """Nạp dữ liệu thật và chuẩn bị các đầu vào dùng chung cho các bài test."""
    interim = data_loader.load_interim()
    features = list(data_loader.CORE_FEATURES)

    df_2019 = interim[interim["year"] == 2019].reset_index(drop=True)
    X_scaled, _ = feature_engineering.scale_features(df_2019, features, method="standard")
    labels, _ = clustering.run_kmeans(X_scaled, n_clusters=3, random_state=42)
    labels = np.array(labels)
    X_2d, _ = feature_engineering.apply_pca(X_scaled, n_components=2)

    cluster_means = pd.DataFrame(
        {
            cluster: X_scaled[labels == cluster].mean(axis=0)
            for cluster in sorted(set(labels.tolist()))
        },
        index=features,
    ).T

    df_cluster = df_2019.copy()
    df_cluster["cluster"] = labels

    metrics_df = load_metrics_table(features, df_2019)
    linkage_matrix, sample_labels = build_dendrogram_payload(features, df_2019)

    return {
        "interim": interim,
        "features": features,
        "df_2019": df_2019,
        "X_2d": X_2d,
        "labels": labels,
        "cluster_means": cluster_means,
        "df_cluster": df_cluster,
        "metrics_df": metrics_df,
        "linkage_matrix": linkage_matrix,
        "sample_labels": sample_labels,
    }


def verify_png(png_path: Path) -> tuple:
    """Kiểm tra tệp PNG: tồn tại, > 0 bytes và metadata DPI >= 300."""
    if not png_path.exists():
        return False, "không tìm thấy tệp ảnh"
    size_bytes = png_path.stat().st_size
    if size_bytes <= 0:
        return False, "tệp ảnh rỗng (0 byte)"
    try:
        with Image.open(png_path) as image:
            dpi_info = image.info.get("dpi")
            if dpi_info is None:
                return False, f"thiếu metadata DPI (kích thước {size_bytes} bytes)"
            dpi_value = round(dpi_info[0])
            if dpi_value < MIN_DPI:
                return False, f"DPI = {dpi_value} (< {MIN_DPI})"
            return True, (
                f"{size_bytes} bytes, DPI = {dpi_value}, "
                f"kích thước {image.size[0]}x{image.size[1]} px"
            )
    except Exception as error:  # noqa: BLE001 - cần báo mọi lỗi đọc ảnh ra log
        return False, f"lỗi đọc tệp PNG: {type(error).__name__}: {error}"


def audit() -> int:
    output_lines = []

    def log(message: str) -> None:
        print(message)
        output_lines.append(message)

    all_passed = True

    log("================================================================================")
    log("BÁO CÁO KIỂM THỬ TRỰC QUAN HÓA (300 DPI) — MỐC M2")
    log("Người thực hiện: Ngô Quang Trung (MSSV: 2045240325)")
    log("Đề tài 16: Phân nhóm quốc gia theo các yếu tố hạnh phúc (World Happiness Report)")
    log("Thời gian thực hiện: Mốc M2 (Ngày 8 – Ngày 14)")
    log("================================================================================")

    # --------------------------------------------------------------------------
    # MỤC 0: Kiểm tra sự tồn tại và export của 9 hàm trực quan hóa
    # --------------------------------------------------------------------------
    log("\n--- [MỤC 0] SỰ TỒN TẠI VÀ EXPORT CỦA 9 HÀM TRONG src/visualization/plots.py ---")
    missing_functions = [name for name in EXPECTED_FUNCTIONS if not hasattr(plots, name)]
    if missing_functions:
        log(f"FAIL: thiếu hàm trong plots.py: {missing_functions}")
        all_passed = False
    else:
        log(f"PASS: đầy đủ 9/9 hàm: {', '.join(EXPECTED_FUNCTIONS)}")

    # Kiểm tra export qua src.visualization
    import src.visualization as visualization_package

    not_exported = [
        name for name in EXPECTED_FUNCTIONS if not hasattr(visualization_package, name)
    ]
    if not_exported:
        log(f"FAIL: hàm chưa được export ở src/visualization/__init__.py: {not_exported}")
        all_passed = False
    else:
        log("PASS: cả 9 hàm đã được export qua src/visualization/__init__.py.")

    # --------------------------------------------------------------------------
    # Chuẩn bị dữ liệu thật cho các bài test
    # --------------------------------------------------------------------------
    log("\n--- CHUẨN BỊ DỮ LIỆU KIỂM THỬ ---")
    data = build_test_data()
    log(
        f"Dữ liệu interim: {len(data['interim'])} dòng; "
        f"năm 2019 có {len(data['df_2019'])} quốc gia, {len(data['features'])} đặc trưng cơ sở."
    )
    log(
        f"Bảng metric elbow/silhouette: {len(data['metrics_df'])} dòng; "
        f"ma trận liên kết Ward mẫu: {data['linkage_matrix'].shape[0]} dòng "
        f"({len(data['sample_labels'])} lá)."
    )

    # Dọn thư mục test để bảo đảm mọi ảnh đều do lần chạy này sinh ra
    TEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for old_png in TEST_OUTPUT_DIR.glob("*.png"):
        old_png.unlink()

    # --------------------------------------------------------------------------
    # Danh sách bài test: (tên hàm, đường dẫn ảnh, hàm gọi thực thi)
    # --------------------------------------------------------------------------
    features = data["features"]
    test_plan = [
        (
            "plot_feature_distributions",
            "test_feature_distributions.png",
            lambda path: plots.plot_feature_distributions(
                data["interim"], features, save_path=path
            ),
        ),
        (
            "plot_correlation_heatmap",
            "test_correlation_heatmap.png",
            lambda path: plots.plot_correlation_heatmap(
                data["interim"], features + ["happiness_score"], save_path=path
            ),
        ),
        (
            "plot_outliers_boxplot",
            "test_outliers_boxplot.png",
            lambda path: plots.plot_outliers_boxplot(
                data["interim"], features, save_path=path
            ),
        ),
        (
            "plot_elbow_silhouette",
            "test_elbow_silhouette.png",
            lambda path: plots.plot_elbow_silhouette(
                data["metrics_df"], save_path=path
            ),
        ),
        (
            "plot_clusters_2d",
            "test_clusters_2d.png",
            lambda path: plots.plot_clusters_2d(
                data["X_2d"], data["labels"], save_path=path
            ),
        ),
        (
            "plot_cluster_radar",
            "test_cluster_radar.png",
            lambda path: plots.plot_cluster_radar(
                data["cluster_means"], features, save_path=path
            ),
        ),
        (
            "plot_happiness_score_by_cluster",
            "test_happiness_score_by_cluster.png",
            lambda path: plots.plot_happiness_score_by_cluster(
                data["df_cluster"], save_path=path
            ),
        ),
        (
            "plot_cluster_profiles_bar",
            "test_cluster_profiles_bar.png",
            lambda path: plots.plot_cluster_profiles_bar(
                data["cluster_means"], features, save_path=path
            ),
        ),
        (
            "plot_dendrogram",
            "test_dendrogram.png",
            lambda path: plots.plot_dendrogram(
                data["linkage_matrix"],
                labels=data["sample_labels"],
                save_path=path,
            ),
        ),
        (
            "plot_dendrogram (truncate_mode='lastp')",
            "test_dendrogram_lastp.png",
            lambda path: plots.plot_dendrogram(
                data["linkage_matrix"],
                labels=data["sample_labels"],
                truncate_mode="lastp",
                p=8,
                save_path=path,
            ),
        ),
    ]

    log("\n--- GỌI THỬ NGHIỆM LẦN LƯỢT CÁC HÀM VẼ VÀ KIỂM TRA ẢNH 300 DPI ---")
    passed_count = 0
    for index, (function_name, file_name, runner) in enumerate(test_plan, start=1):
        png_path = TEST_OUTPUT_DIR / file_name
        log(f"\n[{index}/{len(test_plan)}] {function_name}")
        try:
            figure = runner(png_path)
            if figure is not None:
                plt.close(figure)
        except Exception as error:  # noqa: BLE001 - ghi nhận mọi lỗi để báo cáo
            log(f"  FAIL: hàm ném lỗi khi thực thi — {type(error).__name__}: {error}")
            all_passed = False
            continue

        ok, detail = verify_png(png_path)
        if ok:
            passed_count += 1
            log(f"  PASS: {file_name} — {detail}")
        else:
            log(f"  FAIL: {file_name} — {detail}")
            all_passed = False

    # --------------------------------------------------------------------------
    # TỔNG KẾT VÀ GHI LOG
    # --------------------------------------------------------------------------
    log("\n================================================================================")
    log(f"TỔNG KẾT: {passed_count}/{len(test_plan)} bài test sinh ảnh đạt chuẩn 300 DPI.")
    if all_passed:
        log("KẾT LUẬN: TOÀN BỘ HÀM TRỰC QUAN HÓA MỐC M2 ĐẠT CHUẨN (PASS 100%).")
        log("Xác nhận: module plots.py sẵn sàng phục vụ Notebook 02, Notebook 04 và Báo cáo Word.")
    else:
        log("KẾT LUẬN: CÓ BÀI TEST CHƯA ĐẠT CHUẨN — CẦN KHẮC PHỤC TRƯỚC KHI CHỐT MỐC M2.")
    log("================================================================================")

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("w", encoding="utf-8") as log_handle:
        log_handle.write("\n".join(output_lines) + "\n")

    log(f"\nẢnh kiểm thử lưu tại: {TEST_OUTPUT_DIR}")
    log(f"Đã lưu toàn bộ nhật ký kiểm thử vào: {LOG_FILE}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(audit())
