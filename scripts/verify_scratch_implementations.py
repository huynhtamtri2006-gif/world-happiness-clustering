import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import (
    adjusted_rand_score,
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)
from scipy.cluster.hierarchy import fcluster, linkage

from src.models import (
    SimpleDBSCAN,
    SimpleHierarchicalClustering,
    SimpleKMeans,
    calculate_adjusted_rand_index,
    calculate_calinski_harabasz_score_simple,
    calculate_davies_bouldin_score_simple,
    calculate_silhouette_score_simple,
    load_cluster_artifacts,
    save_cluster_artifacts,
)
from src.models.clustering import euclidean_distance
from src.features.feature_engineering import SimplePCA

failures = []

def check(name, passed, details=""):
    status = "PASS" if passed else "FAIL"
    print(f"{status}: {name}" + (f" — {details}" if details else ""))
    if not passed:
        failures.append(name)

# Euclid
check(
    "Euclidean distance",
    abs(euclidean_distance([0, 0], [3, 4]) - 5.0) < 1e-12,
)

# Dữ liệu thử cho Silhouette, K-Means và các độ đo
X = np.array([
    [0.0, 0.0], [0.1, 0.2], [0.2, 0.1],
    [5.0, 5.0], [5.1, 5.2], [5.2, 5.1],
    [10.0, 0.0], [10.1, 0.2], [10.2, 0.1],
])
labels = [0, 0, 0, 1, 1, 1, 2, 2, 2]

sil_ours = calculate_silhouette_score_simple(X, labels)
sil_ref = silhouette_score(X, labels)
check("Silhouette", abs(sil_ours - sil_ref) <= 1e-10)

# K-Means
km = SimpleKMeans(k=3, random_state=42, n_init=10).fit(X)
km_ref = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X)
km_ari = adjusted_rand_score(km.labels, km_ref.labels_)
check(
    "K-Means",
    km_ari >= 0.99 and km.inertia <= km_ref.inertia_ + 1e-9,
    f"ARI={km_ari:.6f}, inertia={km.inertia:.6f}, sklearn={km_ref.inertia_:.6f}",
)

# Ward
X_ward = np.array([
    [0.0, 0.0], [0.0, 0.2],
    [4.0, 4.0], [4.1, 4.0],
    [10.0, 0.0], [10.1, 0.1],
])
ward = SimpleHierarchicalClustering(k=3)
ward_labels = ward.fit_predict(X_ward)
ward_ref = fcluster(
    linkage(X_ward, method="ward"), t=3, criterion="maxclust"
)
ward_ari = adjusted_rand_score(ward_labels, ward_ref)
check(
    "Ward vs SciPy",
    ward_ari >= 0.99 and len(ward.merge_history) == 3,
    f"ARI={ward_ari:.6f}, merges={len(ward.merge_history)}",
)

# DBSCAN
X_db = np.array([
    [0.0, 0.0], [0.1, 0.1], [-0.1, 0.0],
    [5.0, 5.0], [5.1, 5.0], [4.9, 5.0],
    [20.0, 20.0],
])
db_labels = SimpleDBSCAN(eps=0.3, min_samples=3).fit_predict(X_db)
db_ref = DBSCAN(eps=0.3, min_samples=3).fit_predict(X_db)
db_ari = adjusted_rand_score(db_labels, db_ref)
check(
    "DBSCAN vs sklearn",
    db_ari >= 0.99 and db_labels.count(-1) == 1,
    f"ARI={db_ari:.6f}, noise={db_labels.count(-1)}",
)

# Davies–Bouldin, Calinski–Harabasz và ARI
db_error = abs(
    calculate_davies_bouldin_score_simple(X, labels)
    - davies_bouldin_score(X, labels)
)
ch_error = abs(
    calculate_calinski_harabasz_score_simple(X, labels)
    - calinski_harabasz_score(X, labels)
)
labels_reordered = [7, 7, 7, 3, 3, 3, 9, 9, 9]
ari_error = abs(
    calculate_adjusted_rand_index(labels, labels_reordered)
    - adjusted_rand_score(labels, labels_reordered)
)
check("Davies–Bouldin", db_error <= 1e-10, f"sai số={db_error:.3g}")
check("Calinski–Harabasz", ch_error <= 1e-10, f"sai số={ch_error:.3g}")
check("ARI", ari_error <= 1e-10, f"sai số={ari_error:.3g}")

# SimplePCA: căn dấu thành phần trước khi so tọa độ
X_pca = np.array([
    [2.5, 2.4, 1.2, 0.7], [0.5, 0.7, 0.3, 1.1],
    [2.2, 2.9, 1.8, 0.4], [1.9, 2.2, 1.1, 0.9],
    [3.1, 3.0, 2.2, 1.2], [2.3, 2.7, 1.5, 0.8],
    [2.0, 1.6, 0.7, 1.4], [1.0, 1.1, 0.4, 0.5],
])
pca = SimplePCA(n_components=2)
coords = pca.fit_transform(X_pca)
pca_ref = PCA(n_components=2)
coords_ref = pca_ref.fit_transform(X_pca)

signs = np.sign(np.sum(pca.components_ * pca_ref.components_, axis=1))
signs[signs == 0] = 1
variance_error = np.max(
    np.abs(pca.explained_variance_ratio_ - pca_ref.explained_variance_ratio_)
)
coordinate_error = np.max(np.abs(coords * signs - coords_ref))
check("SimplePCA explained variance", variance_error <= 1e-6,
      f"sai số={variance_error:.3g}")
check("SimplePCA projected coordinates", coordinate_error <= 1e-6,
      f"sai số={coordinate_error:.3g}")

# JSON round-trip
with tempfile.TemporaryDirectory() as temp_dir:
    artifact_path = Path(temp_dir) / "model.json"
    save_cluster_artifacts(
        artifact_path, km, metadata={"year": 2019}
    )
    artifact = load_cluster_artifacts(artifact_path)
    json_ok = (
        artifact["model"]["class"] == "SimpleKMeans"
        and artifact["model"]["parameters"]["k"] == 3
        and artifact["metadata"]["year"] == 2019
        and artifact["model"]["centroids"] is not None
    )
    check("JSON artifact round-trip", json_ok)

# Quy tắc vàng và interim
feature_columns = [
    "gdp_per_capita",
    "social_support",
    "healthy_life_expectancy",
    "freedom",
    "generosity",
    "corruption_perception",
]
forbidden = {"happiness_score", "happiness_rank"}
check("Golden rule feature list", not (set(feature_columns) & forbidden))

interim_path = ROOT / "data" / "interim" / "happiness_merged.csv"
if interim_path.exists():
    import pandas as pd
    df = pd.read_csv(interim_path)
    missing = df[feature_columns].isna().sum().to_dict()
    print("Interim years:", sorted(df["year"].dropna().unique().tolist()))
    print("Missing feature values:", {k: v for k, v in missing.items() if v})
else:
    print("SKIP: interim CSV không có trong checkout này")

if failures:
    print(f"\nTổng kết: {len(failures)} kiểm tra FAIL: {failures}")
    raise SystemExit(1)

print("\nTổng kết: tất cả kiểm tra tự động đều PASS.")
