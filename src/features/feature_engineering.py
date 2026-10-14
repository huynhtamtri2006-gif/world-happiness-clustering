"""
Các hàm tiền xử lý dữ liệu và chuẩn hóa thang đo viết bằng CÁC HÀM CƠ BẢN.
Không dùng black-box, giúp sinh viên hiểu rõ bản chất toán học của từng phép biến đổi.
"""

import math
from typing import List, Tuple, Dict, Any
import numpy as np
import pandas as pd


FEATURE_COLUMNS = [
    "gdp_per_capita",
    "social_support",
    "healthy_life_expectancy",
    "freedom",
    "generosity",
    "corruption_perception",
]


# ==============================================================================
# 1. TÍNH TOÁN THỐNG KÊ CƠ BẢN BẰNG VÒNG LẶP (MEAN, STD, MIN, MAX)
# ==============================================================================

def calculate_mean(values: List[float]) -> float:
    """Tính giá trị trung bình bằng vòng lặp cơ bản: mu = (1/n) * sum(x_i)"""
    total = 0.0
    for v in values:
        total += v
    return total / len(values) if len(values) > 0 else 0.0


def calculate_std(values: List[float], mean_val: float) -> float:
    """Tính độ lệch chuẩn bằng vòng lặp cơ bản: sigma = sqrt((1/n) * sum((x_i - mu)^2))"""
    sum_sq_diff = 0.0
    for v in values:
        diff = v - mean_val
        sum_sq_diff += diff * diff
    variance = sum_sq_diff / len(values) if len(values) > 0 else 0.0
    return math.sqrt(variance)


def calculate_min_max(values: List[float]) -> Tuple[float, float]:
    """Tìm giá trị nhỏ nhất và lớn nhất bằng vòng lặp cơ bản"""
    min_val = float('inf')
    max_val = float('-inf')
    for v in values:
        if v < min_val:
            min_val = v
        if v > max_val:
            max_val = v
    return min_val, max_val


# ==============================================================================
# 2. CHUẨN HÓA THANG ĐO BẰNG CÔNG THỨC CƠ BẢN
# ==============================================================================

class SimpleStandardScaler:
    """
    Chuẩn hóa Z-score thuần túy: z = (x - mean) / std
    Viết bằng các vòng lặp cơ bản để sinh viên dễ giải thích trước giảng viên.
    """
    def __init__(self):
        self.means = []
        self.stds = []

    def fit(self, data: List[List[float]]):
        """Học giá trị mean và std của từng cột đặc trưng."""
        n_features = len(data[0])
        self.means = []
        self.stds = []

        for col_idx in range(n_features):
            col_values = [row[col_idx] for row in data]
            mean_val = calculate_mean(col_values)
            std_val = calculate_std(col_values, mean_val)
            # Tránh chia cho 0 nếu tất cả giá trị trong cột giống nhau
            if std_val == 0.0:
                std_val = 1.0

            self.means.append(mean_val)
            self.stds.append(std_val)
        return self

    def transform(self, data: List[List[float]]) -> List[List[float]]:
        """Áp dụng công thức z = (x - mean) / std cho từng phần tử."""
        scaled_data = []
        for row in data:
            scaled_row = []
            for col_idx in range(len(row)):
                z = (row[col_idx] - self.means[col_idx]) / self.stds[col_idx]
                scaled_row.append(z)
            scaled_data.append(scaled_row)
        return scaled_data

    def fit_transform(self, data: List[List[float]]) -> List[List[float]]:
        return self.fit(data).transform(data)


class SimpleMinMaxScaler:
    """
    Chuẩn hóa Min-Max thuần túy: x_norm = (x - min) / (max - min)
    Đưa giá trị về khoảng [0, 1].
    """
    def __init__(self):
        self.mins = []
        self.maxs = []

    def fit(self, data: List[List[float]]):
        n_features = len(data[0])
        self.mins = []
        self.maxs = []

        for col_idx in range(n_features):
            col_values = [row[col_idx] for row in data]
            min_val, max_val = calculate_min_max(col_values)
            self.mins.append(min_val)
            self.maxs.append(max_val)
        return self

    def transform(self, data: List[List[float]]) -> List[List[float]]:
        scaled_data = []
        for row in data:
            scaled_row = []
            for col_idx in range(len(row)):
                range_val = self.maxs[col_idx] - self.mins[col_idx]
                if range_val == 0.0:
                    scaled_val = 0.0
                else:
                    scaled_val = (row[col_idx] - self.mins[col_idx]) / range_val
                scaled_row.append(scaled_val)
            scaled_data.append(scaled_row)
        return scaled_data

    def fit_transform(self, data: List[List[float]]) -> List[List[float]]:
        return self.fit(data).transform(data)


def scale_features(
    df: pd.DataFrame,
    feature_cols: List[str] = None,
    method: str = "standard"
) -> Tuple[np.ndarray, Any]:
    """
    Hàm tiện ích chuyển đổi DataFrame sang dạng list và chuẩn hóa.
    method: 'standard' (Z-score) hoặc 'minmax' (Min-Max [0, 1])
    """
    if feature_cols is None:
        feature_cols = [c for c in FEATURE_COLUMNS if c in df.columns]

    raw_data = df[feature_cols].values.tolist()

    if method == "standard":
        scaler = SimpleStandardScaler()
    elif method == "minmax":
        scaler = SimpleMinMaxScaler()
    else:
        raise ValueError(f"Phương pháp không hỗ trợ: {method}")

    scaled_list = scaler.fit_transform(raw_data)
    return np.array(scaled_list), scaler



class SimplePCA:
    """PCA from scratch bằng ma trận hiệp phương sai và np.linalg.eigh."""

    def __init__(self, n_components: int = 2):
        self.n_components = n_components
        self.mean_ = None
        self.components_ = None
        self.explained_variance_ = None
        self.explained_variance_ratio_ = None

    def fit(self, data):
        X = np.asarray(data, dtype=float)

        if X.ndim != 2 or X.shape[0] < 2:
            raise ValueError("PCA cần ma trận 2D có ít nhất 2 dòng")
        if not np.isfinite(X).all():
            raise ValueError("Dữ liệu PCA không được chứa NaN hoặc vô cực")
        if not 1 <= self.n_components <= min(X.shape):
            raise ValueError("n_components vượt giới hạn của dữ liệu")

        self.mean_ = X.mean(axis=0)
        centered = X - self.mean_
        covariance = (centered.T @ centered) / (X.shape[0] - 1)

        eigenvalues, eigenvectors = np.linalg.eigh(covariance)
        order = np.argsort(eigenvalues)[::-1]

        eigenvalues = eigenvalues[order]
        eigenvectors = eigenvectors[:, order]

        # Chọn thành phần chính và đặt dấu nhất quán:
        # phần tử có trị tuyệt đối lớn nhất trong mỗi thành phần là dương.
        self.components_ = eigenvectors[:, :self.n_components].T
        for component in self.components_:
            pivot = np.argmax(np.abs(component))
            if component[pivot] < 0:
                component *= -1

        self.explained_variance_ = eigenvalues[:self.n_components]
        total_variance = np.sum(eigenvalues)

        if total_variance == 0:
            self.explained_variance_ratio_ = np.zeros(self.n_components)
        else:
            self.explained_variance_ratio_ = (
                self.explained_variance_ / total_variance
            )

        return self

    def transform(self, data):
        X = np.asarray(data, dtype=float)
        if self.mean_ is None:
            raise RuntimeError("Cần gọi fit trước transform")
        return (X - self.mean_) @ self.components_.T

    def fit_transform(self, data):
        return self.fit(data).transform(data)


def apply_pca(
    X_scaled: np.ndarray,
    n_components: int = 2,
    random_state: int = 42,
):
    """Giảm chiều bằng SimplePCA; giữ nguyên API của hàm cũ."""
    pca = SimplePCA(n_components=n_components)
    X_pca = pca.fit_transform(X_scaled)
    return X_pca, pca
