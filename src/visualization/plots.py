"""
Module trực quan hóa phục vụ phân tích khám phá dữ liệu (EDA) và diễn giải kết quả
gom cụm quốc gia theo 6 yếu tố hạnh phúc (World Happiness Report 2015 – 2019).

Mọi hàm đều lưu ảnh ở độ phân giải cao 300 DPI (tham số bbox_inches="tight")
để chèn trực tiếp vào Báo cáo Word mà không bị vỡ nét. Nhãn trục và tiêu đề
dùng tiếng Việt để khớp phần diễn giải trong báo cáo.
"""

from typing import List, Optional
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


def _save_figure(fig: plt.Figure, save_path: Optional[str], dpi: int = 300) -> plt.Figure:
    """
    Lưu hình ra tệp với độ phân giải cao (mặc định 300 DPI) nếu có đường dẫn.

    Dùng fig.savefig (thay vì plt.savefig) để luôn lưu đúng hình hiện tại,
    tránh nhầm sang figure khác khi trong phiên đã vẽ nhiều biểu đồ.
    """
    if save_path:
        fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
    return fig



def plot_elbow_silhouette(metrics_df: pd.DataFrame, save_path: Optional[str] = None):
    """
    Vẽ 2 biểu đồ liền kề: Đường khuỷu tay (Elbow Inertia) và Silhouette Score theo k.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Elbow
    axes[0].plot(metrics_df["k"], metrics_df["inertia"], "bo-", linewidth=2, markersize=8)
    axes[0].set_title("Phương pháp khuỷu tay (Elbow Method)", fontsize=13)
    axes[0].set_xlabel("Số lượng cụm k", fontsize=11)
    axes[0].set_ylabel("Inertia (WCSS)", fontsize=11)
    axes[0].grid(True, linestyle="--", alpha=0.6)

    # Silhouette
    axes[1].plot(metrics_df["k"], metrics_df["silhouette"], "ro-", linewidth=2, markersize=8)
    axes[1].set_title("Hệ số Silhouette trung bình theo k", fontsize=13)
    axes[1].set_xlabel("Số lượng cụm k", fontsize=11)
    axes[1].set_ylabel("Silhouette Score", fontsize=11)
    axes[1].grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig


def plot_clusters_2d(
    X_2d: np.ndarray,
    labels: np.ndarray,
    title: str = "Trực quan hóa phân cụm (2D PCA)",
    save_path: Optional[str] = None
):
    """
    Vẽ biểu đồ phân tán 2D cho các cụm với palette màu rõ ràng.
    """
    fig, ax = plt.subplots(figsize=(9, 6))
    df_plot = pd.DataFrame({"Dim 1": X_2d[:, 0], "Dim 2": X_2d[:, 1], "Cluster": [f"Cluster {l}" if l != -1 else "Noise" for l in labels]})
    
    sns.scatterplot(
        data=df_plot,
        x="Dim 1",
        y="Dim 2",
        hue="Cluster",
        palette="tab10",
        s=70,
        alpha=0.85,
        ax=ax
    )
    ax.set_title(title, fontsize=14, pad=12)
    ax.grid(True, linestyle="--", alpha=0.5)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig


def plot_cluster_radar(
    cluster_means: pd.DataFrame,
    features: List[str],
    save_path: Optional[str] = None
):
    """
    Vẽ biểu đồ Radar chart so sánh đặc trưng trung bình của từng cụm.
    """
    num_vars = len(features)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(9, 8.5), subplot_kw=dict(polar=True))

    for idx, row in cluster_means.iterrows():
        values = row[features].tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=2, label=f"Cluster {idx}")
        ax.fill(angles, values, alpha=0.15)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), features, fontsize=10.5, fontweight="bold")
    ax.tick_params(pad=14)
    ax.set_title("Biểu đồ Radar so sánh các yếu tố giữa các cụm", y=1.10, fontsize=14, fontweight="bold")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=3, frameon=True)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig


# ==============================================================================
# NHÓM HÀM PHÂN TÍCH KHÁM PHÁ DỮ LIỆU (EDA)
# ==============================================================================

def plot_feature_distributions(
    df: pd.DataFrame,
    features: List[str],
    save_path: Optional[str] = None,
    bins: int = 15
) -> plt.Figure:
    """
    Vẽ lưới subplot histogram kèm đường cong KDE cho từng đặc trưng cơ sở.

    Độ lệch skewness của mỗi đặc trưng được ghi ngay trên tiêu đề subplot để
    phục vụ nhận xét hình dạng phân bố (lệch phải/lệch trái) ở bước EDA.
    """
    n_features = len(features)
    n_cols = 3
    n_rows = int(np.ceil(n_features / n_cols))

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4.6 * n_rows))
    axes = np.atleast_1d(axes).flatten()

    for ax, column in zip(axes, features):
        values = df[column].dropna()
        skew_value = values.skew()
        sns.histplot(
            values, bins=bins, kde=True, ax=ax,
            color="#3498db", edgecolor="black", alpha=0.6
        )
        ax.set_title(f"{column}\n(Skewness = {skew_value:.2f})", fontsize=11, fontweight="bold")
        ax.set_xlabel("Giá trị đặc trưng", fontsize=10)
        ax.set_ylabel("Tần suất", fontsize=10)

    # Ẩn các ô subplot trống nếu số đặc trưng không chia hết cho số cột.
    for ax in axes[n_features:]:
        ax.axis("off")

    fig.suptitle(
        f"Phân bố {n_features} yếu tố cơ sở (Histogram & KDE)",
        fontsize=14, y=1.02, fontweight="bold"
    )
    fig.tight_layout()
    return _save_figure(fig, save_path)


def plot_correlation_heatmap(
    df: pd.DataFrame,
    features: List[str],
    save_path: Optional[str] = None,
    title: str = "Ma trận hệ số tương quan Pearson giữa các đặc trưng"
) -> plt.Figure:
    """
    Vẽ ma trận tương quan Pearson giữa các đặc trưng dưới dạng heatmap.

    Hệ số tương quan được ghi trực tiếp trên từng ô (annot=True) để tiện đối chiếu
    mức độ đa cộng tuyến khi chọn cấu hình gom cụm.
    """
    correlation_matrix = df[features].corr()

    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(
        correlation_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        linewidths=0.8,
        square=True,
        cbar_kws={"label": "Hệ số tương quan Pearson"},
        ax=ax
    )
    ax.set_title(title, fontsize=13, pad=15, fontweight="bold")
    fig.tight_layout()
    return _save_figure(fig, save_path)


def plot_outliers_boxplot(
    df: pd.DataFrame,
    features: List[str],
    save_path: Optional[str] = None,
    title: str = "Biểu đồ hộp phát hiện giá trị ngoại lai"
) -> plt.Figure:
    """
    Vẽ biểu đồ hộp đa biến cho các đặc trưng cơ sở để phát hiện ngoại lai.

    Ngoại lai được xác định theo quy tắc 1.5 * IQR tính trên giá trị gốc; số lượng
    ngoại lai của từng đặc trưng được ghi ngay dưới nhãn trục hoành. Để hiển thị
    đồng nhất trên cùng một trục tung, dữ liệu được đưa về [0, 1] bằng Min-Max
    trước khi vẽ (bản thân việc đếm ngoại lai vẫn dùng giá trị gốc).
    """
    outlier_counts = {}
    for column in features:
        values = df[column].dropna()
        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1
        lower_fence = q1 - 1.5 * iqr
        upper_fence = q3 + 1.5 * iqr
        outlier_counts[column] = int(
            ((values < lower_fence) | (values > upper_fence)).sum()
        )

    # Đưa từng đặc trưng về [0, 1] bằng Min-Max để vẽ chung một trục tung.
    scaled = pd.DataFrame(index=df.index)
    for column in features:
        column_min = df[column].min()
        column_max = df[column].max()
        value_range = column_max - column_min
        if pd.isna(value_range) or value_range == 0:
            scaled[column] = 0.0
        else:
            scaled[column] = (df[column] - column_min) / value_range

    fig, ax = plt.subplots(figsize=(12, 6.2))
    flierprops = dict(
        marker="o", markersize=5.5,
        markerfacecolor="#e74c3c", markeredgecolor="#c0392b", alpha=0.7
    )
    positions = list(range(1, len(features) + 1))
    box = ax.boxplot(
        [scaled[column].dropna().values for column in features],
        positions=positions,
        widths=0.6,
        patch_artist=True,
        flierprops=flierprops
    )
    for patch, color in zip(box["boxes"], sns.color_palette("Set2", len(features))):
        patch.set_facecolor(color)
        patch.set_alpha(0.75)

    tick_labels = [f"{column}\n({outlier_counts[column]} ngoại lai)" for column in features]
    ax.set_xticks(positions)
    ax.set_xticklabels(tick_labels, rotation=15, fontsize=9.5)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel("Thuộc tính cơ sở", fontsize=11, labelpad=10)
    ax.set_ylabel("Giá trị chuẩn hóa Min-Max [0, 1]", fontsize=11)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.set_title(title, fontsize=13, pad=15, fontweight="bold")
    fig.tight_layout()
    return _save_figure(fig, save_path)


# ==============================================================================
# HÀM PHỤ TRỢ VẼ DENDROGRAM TỪ MA TRẬN LIÊN KẾT (tự cài đặt, không dùng scipy)
# ==============================================================================

def _resolve_leaf_count(linkage_matrix: np.ndarray, n_leaves=None, labels=None) -> int:
    """
    Xác định số lá (điểm gốc) của cây từ ma trận liên kết.

    Thứ tự ưu tiên:
    1. Tham số n_leaves nếu người gọi truyền trực tiếp.
    2. len(labels) nếu có danh sách nhãn lá (mỗi lá một nhãn).
    3. Quy ước chuẩn của ma trận liên kết đầy đủ: n = số dòng + 1.

    Lưu ý: với cây gộp sớm (dừng ở k cụm, tức số dòng m = n - k), chỉ số nút trong
    ma trận không đủ để suy ra n một cách duy nhất, nên cần truyền n_leaves hoặc labels.
    """
    if n_leaves is not None:
        return int(n_leaves)
    if labels is not None:
        return len(labels)
    return linkage_matrix.shape[0] + 1


def _linkage_sizes(linkage_matrix: np.ndarray, n_leaves: int) -> dict:
    """Trả về từ điển kích thước cụm {id nút: số điểm gốc} cho toàn bộ cây."""
    n_leaves = int(n_leaves)
    sizes = {leaf: 1 for leaf in range(n_leaves)}
    for row_index, row in enumerate(linkage_matrix):
        sizes[n_leaves + row_index] = int(row[3])
    return sizes


def _validate_linkage(linkage_matrix: np.ndarray, n_leaves: int) -> None:
    """Kiểm tra tính nhất quán giữa ma trận liên kết và số lá đã xác định."""
    n_leaves = int(n_leaves)
    m = linkage_matrix.shape[0]
    referenced = set(int(value) for value in linkage_matrix[:, 0]) | set(
        int(value) for value in linkage_matrix[:, 1]
    )
    if max(referenced) >= n_leaves + m:
        raise ValueError(
            "linkage_matrix không nhất quán với số lá: có chỉ số cụm vượt phạm vi"
        )
    missing = [leaf for leaf in range(n_leaves) if leaf not in referenced]
    if missing:
        raise ValueError(
            f"linkage_matrix không khớp số lá: thiếu chỉ số lá {missing[:5]}"
        )



def _truncate_linkage(linkage_matrix, truncate_mode, p, n_leaves, labels=None):
    """
    Rút gọn cây trước khi vẽ khi số lá quá lớn.

    - truncate_mode="lastp": chỉ giữ p lần gộp cuối cùng (phần ngọn của cây).
    - truncate_mode="level": chỉ giữ các lần gộp có khoảng cách <= p.
    Mỗi nhánh bị cắt được thay bằng một lá đại diện, ghi chú số điểm gốc bên trong.

    Trả về (ma trận liên kết mới, danh sách nhãn lá của cây mới, số lá của cây mới).
    """
    sizes = _linkage_sizes(linkage_matrix, n_leaves)
    m = linkage_matrix.shape[0]

    if truncate_mode == "lastp":
        keep_rows = list(range(max(0, m - int(p)), m))
    elif truncate_mode == "level":
        keep_rows = [i for i in range(m) if linkage_matrix[i, 2] <= float(p)]
    else:
        raise ValueError("truncate_mode chỉ hỗ trợ None, 'lastp' hoặc 'level'")

    if not keep_rows:
        raise ValueError("Ngưỡng cắt không giữ lại nhánh nào để vẽ")

    kept_merged = {n_leaves + row_index for row_index in keep_rows}

    # Lá mới gồm các nút là con của một dòng được giữ nhưng không phải cụm gộp được giữ.
    leaf_nodes = []
    for row_index in keep_rows:
        for child in (int(linkage_matrix[row_index, 0]), int(linkage_matrix[row_index, 1])):
            if child in kept_merged:
                continue
            if child not in leaf_nodes:
                leaf_nodes.append(child)

    leaf_index = {node: idx for idx, node in enumerate(leaf_nodes)}
    merged_index = {
        n_leaves + row_index: len(leaf_nodes) + order
        for order, row_index in enumerate(keep_rows)
    }

    new_rows = []
    for row_index in keep_rows:
        left = int(linkage_matrix[row_index, 0])
        right = int(linkage_matrix[row_index, 1])
        new_left = merged_index[left] if left in kept_merged else leaf_index[left]
        new_right = merged_index[right] if right in kept_merged else leaf_index[right]
        new_rows.append([
            new_left,
            new_right,
            float(linkage_matrix[row_index, 2]),
            int(linkage_matrix[row_index, 3]),
        ])

    new_linkage = np.array(new_rows, dtype=float)

    leaf_labels = []
    for node in leaf_nodes:
        if node >= n_leaves:
            leaf_labels.append(f"nhóm {sizes[node]} điểm")
        elif labels is not None:
            leaf_labels.append(str(labels[node]))
        else:
            leaf_labels.append(str(node))

    return new_linkage, leaf_labels, len(leaf_nodes)


def _draw_dendrogram(ax, linkage_matrix: np.ndarray, n_leaves: int, leaf_labels: Optional[List[str]] = None):
    """
    Vẽ cây dendrogram lên trục ax từ ma trận liên kết.

    Thuật toán: duyệt đệ quy để gán tọa độ ngang cho từng nút (nút trong nằm giữa
    hai nút con, lá xếp lần lượt từ trái sang phải), sau đó vẽ các đoạn chữ U.
    """
    n_leaves = int(n_leaves)
    m = linkage_matrix.shape[0]

    children = {}
    heights = {leaf: 0.0 for leaf in range(n_leaves)}
    for row_index, row in enumerate(linkage_matrix):
        node = n_leaves + row_index
        children[node] = (int(row[0]), int(row[1]))
        heights[node] = float(row[2])

    parent_of = {}
    for node, (left, right) in children.items():
        parent_of[left] = node
        parent_of[right] = node

    roots = [node for node in range(n_leaves + m) if node not in parent_of]

    x_positions = {}
    counter = [0]

    def assign_x(node):
        if node in children:
            left, right = children[node]
            x_left = assign_x(left)
            x_right = assign_x(right)
            x_positions[node] = (x_left + x_right) / 2.0
        else:
            x_positions[node] = float(counter[0])
            counter[0] += 1
        return x_positions[node]

    for root in sorted(roots):
        assign_x(root)

    line_color = "#2c3e50"
    for node, (left, right) in children.items():
        node_height = heights[node]
        ax.plot(
            [x_positions[left], x_positions[left]], [heights[left], node_height],
            color=line_color, linewidth=1.3
        )
        ax.plot(
            [x_positions[right], x_positions[right]], [heights[right], node_height],
            color=line_color, linewidth=1.3
        )
        ax.plot(
            [x_positions[left], x_positions[right]], [node_height, node_height],
            color=line_color, linewidth=1.3
        )

    leaf_positions = [x_positions[leaf] for leaf in range(n_leaves)]
    if leaf_labels is not None:
        names = [str(leaf_labels[leaf]) for leaf in range(n_leaves)]
    else:
        names = [str(leaf) for leaf in range(n_leaves)]
    ax.set_xticks(leaf_positions)
    ax.set_xticklabels(names, rotation=90, fontsize=7.5)
    ax.set_xlim(-1, max(leaf_positions) + 1)
    ax.set_ylabel("Khoảng cách gộp cụm Ward", fontsize=11)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    return ax


def plot_dendrogram(
    linkage_matrix,
    labels: Optional[List[str]] = None,
    title: str = "Cây phân cấp tích tụ (Hierarchical Dendrogram - Ward Linkage)",
    save_path: Optional[str] = None,
    truncate_mode: Optional[str] = None,
    p: int = 30,
    n_leaves: Optional[int] = None
) -> plt.Figure:
    """
    Vẽ biểu đồ cây phân cấp (dendrogram) từ ma trận liên kết Ward.

    Tham số linkage_matrix là mảng (m x 4); mỗi dòng gồm
    [chỉ số cụm trái, chỉ số cụm phải, khoảng cách gộp, số điểm gốc].
    Cây được vẽ thủ công bằng matplotlib nên không phụ thuộc scipy.

    Số lá được xác định theo thứ tự ưu tiên: tham số n_leaves -> len(labels) ->
    quy ước ma trận đầy đủ (m + 1). Truyền labels để hàm tự suy đúng số lá, kể cả
    khi ma trận bị dừng gộp sớm.
    """
    linkage_array = np.asarray(linkage_matrix, dtype=float)
    if linkage_array.ndim != 2 or linkage_array.shape[0] == 0 or linkage_array.shape[1] < 4:
        raise ValueError("linkage_matrix phải là mảng 2 chiều (m x 4) với m >= 1")

    resolved_n = _resolve_leaf_count(linkage_array, n_leaves=n_leaves, labels=labels)
    _validate_linkage(linkage_array, resolved_n)

    leaf_labels = None
    if truncate_mode is not None:
        linkage_array, leaf_labels, resolved_n = _truncate_linkage(
            linkage_array, truncate_mode, p, resolved_n, labels
        )
    elif labels is not None:
        leaf_labels = [str(label) for label in labels]

    fig, ax = plt.subplots(figsize=(12, 6.5))
    _draw_dendrogram(ax, linkage_array, resolved_n, leaf_labels)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    fig.tight_layout()
    return _save_figure(fig, save_path)


# ==============================================================================
# NHÓM HÀM HẬU KIỂM VÀ CHÂN DUNG CỤM
# ==============================================================================

def plot_happiness_score_by_cluster(
    df: pd.DataFrame,
    cluster_col: str = "cluster",
    score_col: str = "happiness_score",
    title: str = "Phân bố điểm hạnh phúc theo từng cụm",
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Vẽ biểu đồ hộp phân bố điểm hạnh phúc giữa các cụm (bước hậu kiểm độc lập).

    Điểm hạnh phúc không tham gia gom cụm, nên biểu đồ này chứng minh các cụm
    hình thành từ 6 yếu tố cơ sở vẫn phản ánh đúng sự phân hóa mức sống thực tế.
    Điểm trung bình mỗi cụm được ghi phía trên mỗi hộp.
    """
    if cluster_col not in df.columns or score_col not in df.columns:
        raise ValueError(f"DataFrame phải có 2 cột '{cluster_col}' và '{score_col}'")

    plot_df = df[[cluster_col, score_col]].dropna().copy()
    plot_df[cluster_col] = plot_df[cluster_col].astype(int).astype(str)
    cluster_order = sorted(plot_df[cluster_col].unique(), key=lambda value: int(value))

    fig, ax = plt.subplots(figsize=(10, 6))
    flierprops = dict(
        marker="o", markersize=5,
        markerfacecolor="#e74c3c", markeredgecolor="#c0392b", alpha=0.7
    )
    sns.boxplot(
        data=plot_df, x=cluster_col, y=score_col,
        order=cluster_order, hue=cluster_col, hue_order=cluster_order,
        palette="Set2", width=0.55, flierprops=flierprops, legend=False, ax=ax
    )
    sns.stripplot(
        data=plot_df, x=cluster_col, y=score_col,
        order=cluster_order, color="#34495e", size=3, alpha=0.45, ax=ax
    )

    for position, cluster in enumerate(cluster_order):
        mean_score = plot_df[plot_df[cluster_col] == cluster][score_col].mean()
        ax.text(
            position, mean_score, f"TB = {mean_score:.2f}",
            ha="center", va="bottom", fontsize=10, fontweight="bold", color="#c0392b"
        )

    ax.set_xlabel("Cụm", fontsize=11)
    ax.set_ylabel("Điểm hạnh phúc (thang 0 – 10)", fontsize=11)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.set_title(title, fontsize=13, pad=14, fontweight="bold")
    fig.tight_layout()
    return _save_figure(fig, save_path)


def plot_cluster_profiles_bar(
    cluster_means: pd.DataFrame,
    features: List[str],
    save_path: Optional[str] = None,
    title: str = "Biểu đồ cột so sánh trung bình đặc trưng giữa các cụm"
) -> plt.Figure:
    """
    Vẽ biểu đồ cột phân nhóm so sánh giá trị trung bình các đặc trưng giữa các cụm.

    cluster_means là DataFrame có chỉ mục là nhãn cụm và các cột là đặc trưng.
    Biểu đồ này dùng để mô tả chân dung cụm (cluster profile) sau khi gom cụm.
    """
    clusters = list(cluster_means.index)
    n_features = len(features)
    n_clusters = len(clusters)
    x_positions = np.arange(n_features)
    bar_width = 0.8 / max(n_clusters, 1)
    colors = sns.color_palette("Set2", n_clusters)

    fig, ax = plt.subplots(figsize=(12, 6.2))
    for position, cluster in enumerate(clusters):
        values = cluster_means.loc[cluster, features].astype(float).values
        offset = (position - (n_clusters - 1) / 2.0) * bar_width
        ax.bar(
            x_positions + offset, values, width=bar_width,
            label=f"Cụm {cluster}", color=colors[position],
            edgecolor="black", alpha=0.9
        )

    ax.set_xticks(x_positions)
    ax.set_xticklabels(features, rotation=15, fontsize=9.5)
    ax.set_xlabel("Đặc trưng cơ sở", fontsize=11)
    ax.set_ylabel("Giá trị trung bình đặc trưng", fontsize=11)
    ax.legend(title="Cụm", fontsize=9.5, title_fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.set_title(title, fontsize=13, pad=14, fontweight="bold")
    fig.tight_layout()
    return _save_figure(fig, save_path)
