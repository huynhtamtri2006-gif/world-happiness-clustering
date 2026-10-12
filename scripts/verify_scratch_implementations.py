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
