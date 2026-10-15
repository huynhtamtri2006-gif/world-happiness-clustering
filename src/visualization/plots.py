"""
Visualization utilities for Clustering and Exploratory Data Analysis.
"""

from typing import List, Optional
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


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
