"""
Các thuật toán gom cụm (K-Means, Hierarchical) và đánh giá chất lượng cụm
ĐƯỢC CÀI ĐẶT THUẦN TÚY BẰNG CÁC HÀM CƠ BẢN (VÒNG LẶP FOR, TOÁN HỌC CĂN BẢN).

Mục đích:
- Phục vụ quá trình tự học và hiểu sâu từng bước của thuật toán.
- Dễ dàng diễn giải, bảo vệ và trả lời vấn đáp trước giảng viên.
"""

import math
import random
from typing import List, Dict, Tuple, Any
import numpy as np
import pandas as pd


# ==============================================================================
# 1. HÀM TÍNH KHOẢNG CÁCH CƠ BẢN
# ==============================================================================

def euclidean_distance(point1: List[float], point2: List[float]) -> float:
    """
    Tính khoảng cách Euclidean giữa 2 điểm trong không gian d chiều:
    d(p1, p2) = sqrt( sum( (p1[i] - p2[i])^2 ) )
    Sử dụng vòng lặp for cơ bản.
    """
    sum_squared = 0.0
    for i in range(len(point1)):
        diff = point1[i] - point2[i]
        sum_squared += diff * diff
    return math.sqrt(sum_squared)


# ==============================================================================
# 2. THUẬT TOÁN K-MEANS BẰNG CÁC HÀM CƠ BẢN (FROM SCRATCH)
# ==============================================================================

class SimpleKMeans:
    """
    Thuật toán K-Means thuần túy:
    - Bước 1: Khởi tạo k tâm cụm ngẫu nhiên từ tập dữ liệu.
    - Bước 2: Duyệt từng điểm, tính khoảng cách đến từng tâm, gán vào tâm gần nhất.
    - Bước 3: Tính lại tọa độ tâm cụm bằng trung bình cộng các điểm trong cụm.
    - Bước 4: Lặp lại đến khi nhãn cụm không đổi hoặc đạt số vòng lặp tối đa.
    """
    def __init__(self, k: int = 3, max_iter: int = 100, random_state: int = 42):
        self.k = k
        self.max_iter = max_iter
        self.random_state = random_state
        self.centroids = []
        self.labels = []
        self.inertia = 0.0

    def fit(self, data):
        # Chuyển dữ liệu sang danh sách các điểm (mỗi điểm là một list số)
        if isinstance(data, np.ndarray):
            points = data.tolist()
        elif hasattr(data, "values"):
            points = data.values.tolist()
        else:
            points = [list(row) for row in data]

        n_samples = len(points)
        n_features = len(points[0])

        if self.random_state is not None:
            random.seed(self.random_state)

        # Bước 1: Chọn ngẫu nhiên k vị trí điểm làm tâm cụm ban đầu
        sample_indices = random.sample(range(n_samples), self.k)
        self.centroids = [list(points[idx]) for idx in sample_indices]

        # Vòng lặp tối ưu hóa
        for iteration in range(self.max_iter):
            # Bước 2: Gán nhãn cho từng điểm vào tâm gần nhất
            new_labels = []
            for point in points:
                min_dist = float("inf")
                best_cluster = 0
                for cluster_idx in range(self.k):
                    dist = euclidean_distance(point, self.centroids[cluster_idx])
                    if dist < min_dist:
                        min_dist = dist
                        best_cluster = cluster_idx
                new_labels.append(best_cluster)

            # Kiểm tra hội tụ: nếu nhãn không đổi so với vòng lặp trước thì dừng
            if new_labels == self.labels:
                break
            self.labels = new_labels

            # Bước 3: Cập nhật lại tâm cụm
            for cluster_idx in range(self.k):
                # Gom các điểm thuộc cụm cluster_idx
                cluster_points = [points[i] for i in range(n_samples) if self.labels[i] == cluster_idx]

                if len(cluster_points) > 0:
                    new_center = []
                    for col in range(n_features):
                        # Tính trung bình cộng của từng thuộc tính
                        col_sum = sum(pt[col] for pt in cluster_points)
                        new_center.append(col_sum / len(cluster_points))
                    self.centroids[cluster_idx] = new_center
                else:
                    # Nếu cụm bị rỗng, lấy ngẫu nhiên 1 điểm gán lại
                    self.centroids[cluster_idx] = list(points[random.randint(0, n_samples - 1)])

        # Bước 4: Tính Inertia (WCSS - Tổng bình phương khoảng cách đến tâm cụm)
        total_inertia = 0.0
        for i in range(n_samples):
            assigned_center = self.centroids[self.labels[i]]
            dist = euclidean_distance(points[i], assigned_center)
            total_inertia += dist * dist
        self.inertia = total_inertia

        return self

    def predict(self, data) -> List[int]:
        """Gán nhãn cụm cho dữ liệu mới."""
        if isinstance(data, np.ndarray):
            points = data.tolist()
        elif hasattr(data, "values"):
            points = data.values.tolist()
        else:
            points = [list(row) for row in data]

        predictions = []
        for point in points:
            min_dist = float("inf")
            best_cluster = 0
            for cluster_idx in range(self.k):
                dist = euclidean_distance(point, self.centroids[cluster_idx])
                if dist < min_dist:
                    min_dist = dist
                    best_cluster = cluster_idx
            predictions.append(best_cluster)
        return predictions

    def fit_predict(self, data) -> List[int]:
        return self.fit(data).labels



class SimpleKMeans:
    """K-Means from scratch với K-Means++ và nhiều lần khởi tạo."""

    def __init__(
        self,
        k: int = 3,
        max_iter: int = 100,
        random_state: int = 42,
        n_init: int = 10,
        init: str = "kmeans++",
    ):
        if k < 1:
            raise ValueError("k phải >= 1")
        if max_iter < 1:
            raise ValueError("max_iter phải >= 1")
        if n_init < 1:
            raise ValueError("n_init phải >= 1")
        if init != "kmeans++":
            raise ValueError("Hiện chỉ hỗ trợ init='kmeans++'")

        self.k = k
        self.max_iter = max_iter
        self.random_state = random_state
        self.n_init = n_init
        self.init = init
        self.centroids = []
        self.cluster_centers_ = []
        self.labels = []
        self.inertia = float("inf")
        self.inertia_history = []
        self.n_iter_ = 0

    @staticmethod
    def _as_points(data):
        if isinstance(data, np.ndarray):
            points = data.astype(float).tolist()
        elif hasattr(data, "values"):
            points = data.values.astype(float).tolist()
        else:
            points = [[float(value) for value in row] for row in data]

        if not points or not points[0]:
            raise ValueError("Dữ liệu không được rỗng")

        width = len(points[0])
        if any(len(row) != width for row in points):
            raise ValueError("Các dòng dữ liệu phải có cùng số đặc trưng")

        if not all(math.isfinite(value) for row in points for value in row):
            raise ValueError("Dữ liệu không được chứa NaN hoặc vô cực")

        return points

    @staticmethod
    def _assign(points, centers):
        labels = []
        for point in points:
            distances = [
                euclidean_distance(point, center)
                for center in centers
            ]
            labels.append(min(range(len(distances)), key=distances.__getitem__))
        return labels

    @staticmethod
    def _calculate_inertia(points, labels, centers):
        total = 0.0
        for point, label in zip(points, labels):
            distance = euclidean_distance(point, centers[label])
            total += distance * distance
        return total

    def _initialize_kmeans_plus_plus(self, points, rng):
        n_samples = len(points)
        selected = [rng.randrange(n_samples)]
        centers = [points[selected[0]].copy()]

        while len(centers) < self.k:
            closest_sq = []
            for point in points:
                distance = min(
                    euclidean_distance(point, center)
                    for center in centers
                )
                closest_sq.append(distance * distance)

            candidates = [i for i in range(n_samples) if i not in selected]
            weights = [closest_sq[i] for i in candidates]
            total_weight = sum(weights)

            if total_weight == 0.0:
                chosen = rng.choice(candidates)
            else:
                target = rng.random() * total_weight
                running = 0.0
                chosen = candidates[-1]
                for index, weight in zip(candidates, weights):
                    running += weight
                    if running >= target:
                        chosen = index
                        break

            selected.append(chosen)
            centers.append(points[chosen].copy())

        return centers

    def fit(self, data):
        points = self._as_points(data)
        n_samples = len(points)
        n_features = len(points[0])

        if self.k > n_samples:
            raise ValueError("k không được lớn hơn số dòng dữ liệu")

        seed_rng = random.Random(self.random_state)
        best_result = None

        for _ in range(self.n_init):
            run_seed = seed_rng.randrange(0, 2**32)
            rng = random.Random(run_seed)
            centers = self._initialize_kmeans_plus_plus(points, rng)
            history = []
            labels = None

            for iteration in range(self.max_iter):
                current_labels = self._assign(points, centers)
                new_centers = []

                for cluster_id in range(self.k):
                    members = [
                        points[i]
                        for i, label in enumerate(current_labels)
                        if label == cluster_id
                    ]

                    if members:
                        center = [
                            sum(row[col] for row in members) / len(members)
                            for col in range(n_features)
                        ]
                    else:
                        # Đặt tâm cụm rỗng tại điểm xa tâm hiện tại nhất.
                        distances = [
                            min(
                                euclidean_distance(point, old_center)
                                for old_center in centers
                            )
                            for point in points
                        ]
                        farthest = max(
                            range(n_samples),
                            key=distances.__getitem__,
                        )
                        center = points[farthest].copy()

                    new_centers.append(center)

                new_labels = self._assign(points, new_centers)
                inertia = self._calculate_inertia(
                    points, new_labels, new_centers
                )
                history.append(inertia)

                converged = (
                    labels is not None and new_labels == labels
                )
                centers = new_centers
                labels = new_labels

                if converged:
                    break

            final_labels = self._assign(points, centers)
            final_inertia = self._calculate_inertia(
                points, final_labels, centers
            )

            result = {
                "inertia": final_inertia,
                "labels": final_labels,
                "centers": centers,
                "history": history,
                "n_iter": iteration + 1,
            }

            if best_result is None or result["inertia"] < best_result["inertia"]:
                best_result = result

        self.inertia = best_result["inertia"]
        self.labels = best_result["labels"]
        self.centroids = best_result["centers"]
        self.cluster_centers_ = self.centroids
        self.inertia_history = best_result["history"]
        self.n_iter_ = best_result["n_iter"]
        return self

    def predict(self, data):
        points = self._as_points(data)
        return self._assign(points, self.centroids)

    def fit_predict(self, data):
        return self.fit(data).labels


# ==============================================================================
# 3. THUẬT TOÁN PHÂN CỤM PHÂN CẤP (HIERARCHICAL AGGLOMERATIVE) TỰ CODE
# ==============================================================================


class SimpleHierarchicalClustering:
    """Phân cụm phân cấp với tiêu chí Ward và Lance–Williams."""

    def __init__(self, k: int = 3):
        self.k = k
        self.labels = []
        self.cluster_centroids = []
        self.merge_history = []

    @staticmethod
    def _as_points(data):
        if isinstance(data, np.ndarray):
            points = data.astype(float).tolist()
        elif hasattr(data, "values"):
            points = data.values.astype(float).tolist()
        else:
            points = [[float(value) for value in row] for row in data]

        if not points or not points[0]:
            raise ValueError("Dữ liệu không được rỗng")

        width = len(points[0])
        if any(len(row) != width for row in points):
            raise ValueError("Các dòng phải có cùng số đặc trưng")
        if not all(math.isfinite(value) for row in points for value in row):
            raise ValueError("Dữ liệu không được chứa NaN hoặc vô cực")

        return points

    @staticmethod
    def _key(cluster_a, cluster_b):
        return (min(cluster_a, cluster_b), max(cluster_a, cluster_b))

    def fit(self, data):
        points = self._as_points(data)
        n_samples = len(points)

        if not 1 <= self.k <= n_samples:
            raise ValueError("k phải nằm trong khoảng từ 1 đến số dòng dữ liệu")

        # Ban đầu mỗi điểm là một cụm riêng.
        clusters = {i: [i] for i in range(n_samples)}
        sizes = {i: 1 for i in range(n_samples)}
        active = set(range(n_samples))
        distances_sq = {}

        # Khoảng cách bình phương Euclid ban đầu giữa các điểm.
        for i in range(n_samples):
            for j in range(i + 1, n_samples):
                distance = euclidean_distance(points[i], points[j])
                distances_sq[(i, j)] = distance * distance

        self.merge_history = []
        next_cluster_id = n_samples

        while len(active) > self.k:
            active_ids = sorted(active)
            best_pair = None
            best_distance_sq = float("inf")

            # Tìm cặp có khoảng cách Ward nhỏ nhất.
            for pos, cluster_a in enumerate(active_ids):
                for cluster_b in active_ids[pos + 1:]:
                    key = self._key(cluster_a, cluster_b)
                    distance_sq = distances_sq[key]

                    if distance_sq < best_distance_sq:
                        best_distance_sq = distance_sq
                        best_pair = (cluster_a, cluster_b)

            cluster_a, cluster_b = best_pair
            size_a = sizes[cluster_a]
            size_b = sizes[cluster_b]
            merged_id = next_cluster_id

            remaining = [
                cluster_id for cluster_id in active_ids
                if cluster_id not in (cluster_a, cluster_b)
            ]

            # Lance–Williams cho Ward, dùng khoảng cách bình phương.
            for cluster_c in remaining:
                size_c = sizes[cluster_c]
                d_ac = distances_sq[self._key(cluster_a, cluster_c)]
                d_bc = distances_sq[self._key(cluster_b, cluster_c)]
                d_ab = best_distance_sq

                updated_sq = (
                    (size_a + size_c) * d_ac
                    + (size_b + size_c) * d_bc
                    - size_c * d_ab
                ) / (size_a + size_b + size_c)

                distances_sq[self._key(merged_id, cluster_c)] = max(
                    updated_sq, 0.0
                )

            members = clusters[cluster_a] + clusters[cluster_b]
            clusters[merged_id] = members
            sizes[merged_id] = size_a + size_b

            self.merge_history.append({
                "left": cluster_a,
                "right": cluster_b,
                "distance": math.sqrt(max(best_distance_sq, 0.0)),
                "size": size_a + size_b,
                "merged_id": merged_id,
            })

            active.remove(cluster_a)
            active.remove(cluster_b)
            active.add(merged_id)
            next_cluster_id += 1

        # Gán nhãn ổn định theo chỉ số điểm nhỏ nhất trong mỗi cụm.
        final_clusters = sorted(
            (clusters[cluster_id] for cluster_id in active),
            key=min,
        )
        self.labels = [0] * n_samples
        self.cluster_centroids = []

        for label, members in enumerate(final_clusters):
            center = [
                sum(points[index][col] for index in members) / len(members)
                for col in range(len(points[0]))
            ]
            self.cluster_centroids.append(center)

            for index in members:
                self.labels[index] = label

        return self

    def fit_predict(self, data):
        return self.fit(data).labels



# 3b. DBSCAN FROM SCRATCH

class SimpleDBSCAN:
    """DBSCAN from scratch; nhãn -1 biểu thị điểm nhiễu."""

    def __init__(self, eps: float = 0.5, min_samples: int = 5):
        if eps <= 0:
            raise ValueError("eps phải > 0")
        if min_samples < 1:
            raise ValueError("min_samples phải >= 1")

        self.eps = eps
        self.min_samples = min_samples
        self.labels = []
        self.labels_ = []
        self.core_sample_indices_ = []

    @staticmethod
    def _as_points(data):
        if isinstance(data, np.ndarray):
            points = data.astype(float).tolist()
        elif hasattr(data, "values"):
            points = data.values.astype(float).tolist()
        else:
            points = [[float(value) for value in row] for row in data]

        if not points or not points[0]:
            raise ValueError("Dữ liệu không được rỗng")

        width = len(points[0])
        if any(len(row) != width for row in points):
            raise ValueError("Các dòng phải có cùng số đặc trưng")
        if not all(math.isfinite(value) for row in points for value in row):
            raise ValueError("Dữ liệu không được chứa NaN hoặc vô cực")

        return points

    def fit(self, data):
        points = self._as_points(data)
        n_samples = len(points)
        visited = [False] * n_samples
        labels = [None] * n_samples
        core_indices = []
        cluster_id = 0

        def region_query(point_index):
            return [
                other_index
                for other_index in range(n_samples)
                if euclidean_distance(
                    points[point_index], points[other_index]
                ) <= self.eps
            ]

        for point_index in range(n_samples):
            if visited[point_index]:
                continue

            visited[point_index] = True
            neighbors = region_query(point_index)

            if len(neighbors) < self.min_samples:
                labels[point_index] = -1
                continue

            core_indices.append(point_index)
            labels[point_index] = cluster_id
            seeds = list(neighbors)
            seeds_seen = set(seeds)
            position = 0

            while position < len(seeds):
                neighbor_index = seeds[position]

                if not visited[neighbor_index]:
                    visited[neighbor_index] = True
                    nearby = region_query(neighbor_index)

                    if len(nearby) >= self.min_samples:
                        core_indices.append(neighbor_index)
                        for candidate in nearby:
                            if candidate not in seeds_seen:
                                seeds.append(candidate)
                                seeds_seen.add(candidate)

                if labels[neighbor_index] is None or labels[neighbor_index] == -1:
                    labels[neighbor_index] = cluster_id

                position += 1

            cluster_id += 1

        self.labels = labels
        self.labels_ = labels
        self.core_sample_indices_ = sorted(set(core_indices))
        return self

    def fit_predict(self, data):
        return self.fit(data).labels


# ==============================================================================
# 4. HÀM TÍNH HỆ SỐ SILHOUETTE SCORE TỰ CODE (CÔNG THỨC TOÁN CƠ BẢN)
# ==============================================================================

def calculate_silhouette_score_simple(data, labels: List[int]) -> float:
    """
    Tính hệ số Silhouette trung bình bằng công thức toán căn bản:
    Với mỗi điểm i trong cụm C_A:
    - a(i): Khoảng cách trung bình từ i đến tất cả các điểm khác trong cùng cụm C_A (độ kết dính).
    - b(i): Khoảng cách trung bình nhỏ nhất từ i đến các điểm trong cụm láng giềng khác (độ phân tách).
    - s(i) = (b(i) - a(i)) / max(a(i), b(i))
    Silhouette Score = trung bình s(i) của toàn bộ tập dữ liệu.
    """
    if isinstance(data, np.ndarray):
        points = data.tolist()
    elif hasattr(data, "values"):
        points = data.values.tolist()
    else:
        points = [list(row) for row in data]

    n_samples = len(points)
    unique_clusters = list(set(labels))

    if len(unique_clusters) < 2 or len(unique_clusters) >= n_samples:
        return 0.0

    silhouette_coefficients = []

    for i in range(n_samples):
        current_cluster = labels[i]

        # 1. Tính a(i): khoảng cách nội cụm
        same_cluster_indices = [idx for idx in range(n_samples) if labels[idx] == current_cluster and idx != i]
        if len(same_cluster_indices) == 0:
            a_i = 0.0
        else:
            total_dist_same = sum(euclidean_distance(points[i], points[idx]) for idx in same_cluster_indices)
            a_i = total_dist_same / len(same_cluster_indices)

        # 2. Tính b(i): khoảng cách đến cụm láng giềng gần nhất
        b_i = float("inf")
        for other_cluster in unique_clusters:
            if other_cluster == current_cluster:
                continue
            other_indices = [idx for idx in range(n_samples) if labels[idx] == other_cluster]
            if len(other_indices) > 0:
                total_dist_other = sum(euclidean_distance(points[i], points[idx]) for idx in other_indices)
                avg_dist_other = total_dist_other / len(other_indices)
                if avg_dist_other < b_i:
                    b_i = avg_dist_other

        # 3. Tính s(i)
        max_ab = max(a_i, b_i)
        if max_ab == 0.0:
            s_i = 0.0
        else:
            s_i = (b_i - a_i) / max_ab
        silhouette_coefficients.append(s_i)

    return sum(silhouette_coefficients) / len(silhouette_coefficients)



# 4b. CÁC ĐỘ ĐO ĐÁNH GIÁ FROM SCRATCH

def _prepare_metric_inputs(data, labels):
    if isinstance(data, np.ndarray):
        points = data.astype(float).tolist()
    elif hasattr(data, "values"):
        points = data.values.astype(float).tolist()
    else:
        points = [[float(value) for value in row] for row in data]

    labels = list(labels)
    if len(points) != len(labels):
        raise ValueError("Số nhãn phải bằng số dòng dữ liệu")
    if not points:
        raise ValueError("Dữ liệu không được rỗng")
    return points, labels


def calculate_davies_bouldin_score_simple(data, labels):
    """Tính Davies–Bouldin Index bằng khoảng cách tới tâm cụm."""
    points, labels = _prepare_metric_inputs(data, labels)
    clusters = sorted(set(labels))

    if len(clusters) < 2 or len(clusters) >= len(points):
        return 0.0

    centers = {}
    scatters = {}

    for cluster in clusters:
        members = [
            points[i] for i, label in enumerate(labels)
            if label == cluster
        ]
        center = [
            sum(row[col] for row in members) / len(members)
            for col in range(len(points[0]))
        ]
        centers[cluster] = center
        scatters[cluster] = sum(
            euclidean_distance(row, center) for row in members
        ) / len(members)

    cluster_scores = []
    for cluster_a in clusters:
        ratios = []
        for cluster_b in clusters:
            if cluster_a == cluster_b:
                continue

            center_distance = euclidean_distance(
                centers[cluster_a], centers[cluster_b]
            )
            numerator = scatters[cluster_a] + scatters[cluster_b]

            if center_distance == 0.0:
                ratio = 0.0 if numerator == 0.0 else float("inf")
            else:
                ratio = numerator / center_distance

            ratios.append(ratio)

        cluster_scores.append(max(ratios))

    return sum(cluster_scores) / len(cluster_scores)


def calculate_calinski_harabasz_score_simple(data, labels):
    """Tính Calinski–Harabasz Index từ tổng phương sai giữa/trong cụm."""
    points, labels = _prepare_metric_inputs(data, labels)
    clusters = sorted(set(labels))
    n_samples = len(points)
    n_clusters = len(clusters)

    if n_clusters < 2 or n_clusters >= n_samples:
        return 0.0

    n_features = len(points[0])
    overall_center = [
        sum(row[col] for row in points) / n_samples
        for col in range(n_features)
    ]

    between = 0.0
    within = 0.0

    for cluster in clusters:
        members = [
            points[i] for i, label in enumerate(labels)
            if label == cluster
        ]
        center = [
            sum(row[col] for row in members) / len(members)
            for col in range(n_features)
        ]

        between += len(members) * (
            euclidean_distance(center, overall_center) ** 2
        )
        within += sum(
            euclidean_distance(row, center) ** 2
            for row in members
        )

    if within == 0.0:
        return 1.0

    return (
        (between / (n_clusters - 1))
        / (within / (n_samples - n_clusters))
    )


def calculate_adjusted_rand_index(labels_true, labels_pred):
    """Tính Adjusted Rand Index từ bảng chéo nhãn."""
    labels_true = list(labels_true)
    labels_pred = list(labels_pred)

    if len(labels_true) != len(labels_pred):
        raise ValueError("Hai bộ nhãn phải có cùng số phần tử")

    n_samples = len(labels_true)
    if n_samples < 2:
        return 1.0

    true_values = sorted(set(labels_true))
    pred_values = sorted(set(labels_pred))

    contingency = [
        [
            sum(
                1 for true_label, pred_label
                in zip(labels_true, labels_pred)
                if true_label == true_value and pred_label == pred_value
            )
            for pred_value in pred_values
        ]
        for true_value in true_values
    ]

    choose_two = lambda value: value * (value - 1) / 2
    sum_cells = sum(
        choose_two(value)
        for row in contingency
        for value in row
    )
    row_sums = [sum(row) for row in contingency]
    col_sums = [
        sum(contingency[row][col] for row in range(len(true_values)))
        for col in range(len(pred_values))
    ]

    sum_rows = sum(choose_two(value) for value in row_sums)
    sum_cols = sum(choose_two(value) for value in col_sums)
    total_pairs = choose_two(n_samples)

    expected = (sum_rows * sum_cols) / total_pairs
    maximum = 0.5 * (sum_rows + sum_cols)

    if maximum == expected:
        return 1.0

    return (sum_cells - expected) / (maximum - expected)


# ==============================================================================
# 5. KHẢO SÁT K TỐI ƯU (ELBOW & SILHOUETTE) DÙNG CÁC HÀM CƠ BẢN
# ==============================================================================

def find_optimal_k_scratch(data, k_range: range = range(2, 9), random_state: int = 42) -> List[Dict[str, Any]]:
    """
    Khảo sát k tối ưu bằng thuật toán SimpleKMeans và hàm tính Silhouette tự viết.
    Trả về danh sách kết quả gồm {k, inertia, silhouette}.
    """
    results = []
    for k in k_range:
        km = SimpleKMeans(k=k, random_state=random_state)
        km.fit(data)
        sil = calculate_silhouette_score_simple(data, km.labels)
        results.append({
            "k": k,
            "inertia": km.inertia,
            "silhouette": sil
        })
    return results


# 6. WRAPPER CHẠY MÔ HÌNH VÀ ĐÁNH GIÁ

def run_kmeans(data, n_clusters=3, random_state=42, n_init=10):
    model = SimpleKMeans(
        k=n_clusters,
        random_state=random_state,
        n_init=n_init,
        init="kmeans++",
    )
    labels = model.fit_predict(data)
    return labels, model


def run_hierarchical(data, n_clusters=3, linkage="ward"):
    if linkage.lower() != "ward":
        raise ValueError("Hiện chỉ hỗ trợ linkage='ward'")
    model = SimpleHierarchicalClustering(k=n_clusters)
    labels = model.fit_predict(data)
    return labels, model


def run_dbscan(data, eps=0.5, min_samples=5):
    model = SimpleDBSCAN(eps=eps, min_samples=min_samples)
    labels = model.fit_predict(data)
    return labels, model


def find_optimal_k_kmeans(
    data,
    k_range=range(2, 10),
    random_state=42,
    n_init=10,
):
    results = []

    for k in k_range:
        labels, model = run_kmeans(
            data,
            n_clusters=k,
            random_state=random_state,
            n_init=n_init,
        )
        unique_labels = set(labels)

        if 2 <= len(unique_labels) < len(labels):
            silhouette = calculate_silhouette_score_simple(data, labels)
        else:
            silhouette = 0.0

        results.append({
            "k": k,
            "inertia": model.inertia,
            "silhouette": silhouette,
        })

    return pd.DataFrame(results)


def evaluate_clustering(data, labels):
    points, labels = _prepare_metric_inputs(data, labels)
    n_noise = sum(label == -1 for label in labels)

    # Bỏ điểm nhiễu khỏi các metric nội tại; vẫn đếm riêng n_noise.
    kept = [i for i, label in enumerate(labels) if label != -1]
    eval_points = [points[i] for i in kept]
    eval_labels = [labels[i] for i in kept]
    clusters = sorted(set(eval_labels))
    sizes = [eval_labels.count(cluster) for cluster in clusters]

    result = {
        "silhouette": 0.0,
        "davies_bouldin": 0.0,
        "calinski_harabasz": 0.0,
        "inertia": 0.0,
        "n_clusters": len(clusters),
        "n_noise": n_noise,
        "sizes": "/".join(str(size) for size in sizes),
    }

    if len(clusters) >= 2 and len(clusters) < len(eval_points):
        result["silhouette"] = calculate_silhouette_score_simple(
            eval_points, eval_labels
        )
        result["davies_bouldin"] = calculate_davies_bouldin_score_simple(
            eval_points, eval_labels
        )
        result["calinski_harabasz"] = calculate_calinski_harabasz_score_simple(
            eval_points, eval_labels
        )

    centers = {}
    for cluster in clusters:
        members = [
            eval_points[i] for i, label in enumerate(eval_labels)
            if label == cluster
        ]
        centers[cluster] = [
            sum(row[col] for row in members) / len(members)
            for col in range(len(points[0]))
        ]

    result["inertia"] = sum(
        euclidean_distance(eval_points[i], centers[label]) ** 2
        for i, label in enumerate(eval_labels)
    )

    return result


# 7. LƯU VÀ NẠP THÔNG TIN MÔ HÌNH BẰNG JSON

def _make_json_safe(value):
    import numpy as np

    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {str(key): _make_json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_make_json_safe(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value

    raise TypeError(f"Không thể lưu kiểu dữ liệu {type(value).__name__} vào JSON")


def save_cluster_artifacts(path, model, scaler=None, metadata=None):
    """Lưu tham số và kết quả mô hình vào tệp JSON."""
    import json
    from pathlib import Path

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    model_data = {
        "class": type(model).__name__,
        "parameters": {},
        "centroids": getattr(model, "centroids", None),
        "cluster_centroids": getattr(model, "cluster_centroids", None),
        "labels": getattr(model, "labels", None),
        "inertia": getattr(model, "inertia", None),
        "inertia_history": getattr(model, "inertia_history", None),
        "n_iter": getattr(model, "n_iter_", None),
        "merge_history": getattr(model, "merge_history", None),
        "eps": getattr(model, "eps", None),
        "min_samples": getattr(model, "min_samples", None),
    }

    for name in ("k", "n_init", "max_iter", "random_state", "init"):
        if hasattr(model, name):
            model_data["parameters"][name] = getattr(model, name)

    scaler_data = None
    if scaler is not None:
        scaler_data = {
            name: getattr(scaler, name)
            for name in ("means", "stds", "mins", "maxs")
            if hasattr(scaler, name)
        }

    artifact = {
        "model": model_data,
        "scaler": scaler_data,
        "metadata": metadata or {},
    }

    with path.open("w", encoding="utf-8") as file:
        json.dump(_make_json_safe(artifact), file, ensure_ascii=False, indent=2)

    return str(path)


def load_cluster_artifacts(path):
    """Đọc artifact JSON; trả về từ điển dữ liệu mô hình."""
    import json
    from pathlib import Path

    with Path(path).open("r", encoding="utf-8") as file:
        return json.load(file)
