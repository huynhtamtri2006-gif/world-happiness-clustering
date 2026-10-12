import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score

import sys
from pathlib import Path as FilePath

sys.path.insert(0, str(FilePath(__file__).resolve().parents[1]))

from src.models.clustering import (
    SimpleKMeans,
    calculate_silhouette_score_simple,
    euclidean_distance,
)

# 1. Kiểm tra khoảng cách Euclid
assert abs(euclidean_distance([0, 0], [3, 4]) - 5.0) < 1e-12
print("PASS: Euclidean distance")

# 2. Đối chiếu Silhouette
X_silhouette = np.array([
    [0.0, 0.0], [0.2, 0.1], [0.1, 0.3],
    [5.0, 5.0], [5.2, 5.1], [4.9, 5.2],
])
labels_silhouette = [0, 0, 0, 1, 1, 1]

ours_silhouette = calculate_silhouette_score_simple(
    X_silhouette, labels_silhouette
)
reference_silhouette = silhouette_score(X_silhouette, labels_silhouette)

assert abs(ours_silhouette - reference_silhouette) < 1e-10
print(f"PASS: Silhouette ({ours_silhouette:.12f})")

# 3. Chẩn đoán K-Means hiện tại
X_kmeans = np.array([
    [0.0, 0.0], [0.1, 0.2], [0.2, 0.1],
    [5.0, 5.0], [5.1, 5.2], [5.2, 5.1],
    [10.0, 0.0], [10.1, 0.2], [10.2, 0.1],
])

ours_kmeans = SimpleKMeans(k=3, random_state=42).fit(X_kmeans)
reference_kmeans = KMeans(
    n_clusters=3, random_state=42, n_init=10
).fit(X_kmeans)

ari = adjusted_rand_score(ours_kmeans.labels, reference_kmeans.labels_)

print(f"Inertia tự viết: {ours_kmeans.inertia:.6f}")
print(f"Inertia sklearn: {reference_kmeans.inertia_:.6f}")
print(f"ARI: {ari:.6f}")

if ari >= 0.99 and ours_kmeans.inertia <= reference_kmeans.inertia_ + 1e-9:
    print("PASS: K-Means")
else:
    print("FAIL: K-Means — cần điều tra/sửa ở M2")

print("CHƯA KIỂM TRA: Ward, DBSCAN, Davies-Bouldin, Calinski-Harabasz, SimplePCA")


# 4. Rà soát bảng interim và các cột đầu vào
import pandas as pd

FEATURE_COLUMNS = [
    "gdp_per_capita",
    "social_support",
    "healthy_life_expectancy",
    "freedom",
    "generosity",
    "corruption_perception",
]
FORBIDDEN_COLUMNS = {"happiness_score", "happiness_rank"}

interim_path = FilePath(__file__).resolve().parents[1] / "data/interim/happiness_merged.csv"

if interim_path.exists():
    df = pd.read_csv(interim_path)
    missing_features = [c for c in FEATURE_COLUMNS if c not in df.columns]
    assert not missing_features, f"Thiếu cột đặc trưng: {missing_features}"
    assert not (set(FEATURE_COLUMNS) & FORBIDDEN_COLUMNS), "Danh sách đặc trưng chứa cột bị cấm"

    years = sorted(df["year"].dropna().astype(int).unique().tolist())
    print(f"Năm trong interim: {years}")
    print(f"Số dòng theo năm: {df.groupby('year').size().to_dict()}")

    missing_values = df[FEATURE_COLUMNS].isna().sum()
    print("Giá trị thiếu trong 6 đặc trưng:")
    print(missing_values[missing_values > 0].to_dict())

    missing_rows = df.loc[
        df["corruption_perception"].isna(),
        ["country", "year", "corruption_perception"],
    ]
    print("Dòng thiếu corruption_perception:")
    print(missing_rows.to_dict(orient="records"))
else:
    print(f"SKIP: Không tìm thấy file interim: {interim_path}")
