"""
Script tạo bảng dịch chuyển cụm liên năm và trực quan hóa M3 (300 DPI)
Học phần: Khai thác dữ liệu (Data Mining) — Đề tài 16: World Happiness Report
Phụ trách kiểm toán: Hà Mạnh Trường (Nhóm trưởng)
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
from pathlib import Path

# Thiết lập đường dẫn tương đối độc lập môi trường
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.models.clustering import match_clusters_greedy, euclidean_distance
from src.features.feature_engineering import SimplePCA
tables_dir = project_root / "reports" / "tables"
figures_dir = project_root / "reports" / "figures"
processed_dir = project_root / "data" / "processed"
interim_path = project_root / "data" / "interim" / "happiness_merged.csv"

tables_dir.mkdir(parents=True, exist_ok=True)
figures_dir.mkdir(parents=True, exist_ok=True)
processed_dir.mkdir(parents=True, exist_ok=True)

# 6 yếu tố cơ sở (Quy tắc vàng: KHÔNG đưa happiness_score vào gom cụm)
FEATURE_COLUMNS = [
    "gdp_per_capita",
    "social_support",
    "healthy_life_expectancy",
    "freedom",
    "generosity",
    "corruption_perception",
]

years = [2015, 2016, 2017, 2018, 2019]

def main():
    print("=== 1. TẢI DỮ LIỆU VÀ MÔ HÌNH K-MEANS 5 NĂM ===")
    df_interim = pd.read_csv(interim_path)
    
    models = {y: json.load(open(project_root / f"models/kmeans_{y}.json", encoding="utf-8")) for y in years}
    raw_contrast_dfs = {y: pd.read_csv(processed_dir / f"contrast_k3/contrast_k3_kmeans_{y}.csv") for y in years}
    
    # 2. GHÉP CỤM LIÊN NĂM THAM LAM (CROSS-YEAR MATCHING)
    print("=== 2. THỰC HIỆN GHÉP CỤM LIÊN NĂM BẰNG match_clusters_greedy ===")
    match_rows = []
    
    # Chuẩn hóa nhãn ngữ nghĩa về chuẩn 3 bậc:
    # 0: Hạnh phúc cao (Phát triển toàn diện)
    # 1: Hạnh phúc trung bình (Đang phát triển)
    # 2: Hạnh phúc thấp (Khó khăn & Thách thức)
    
    # Xác định mapping cho từng năm sao cho cluster ID 0 = Cao, 1 = TB, 2 = Thấp
    # Dựa trên xếp hạng điểm hạnh phúc trung bình thực tế của từng cụm
    aligned_dfs = {}
    for y in years:
        d = raw_contrast_dfs[y].copy()
        mean_scores = d.groupby("cluster_k3")["happiness_score"].mean().to_dict()
        # Sắp xếp cluster_id theo điểm hạnh phúc giảm dần: cao nhất -> 0, nhì -> 1, ba -> 2
        sorted_clusters = sorted(mean_scores.keys(), key=lambda c: mean_scores[c], reverse=True)
        to_canonical = {orig: canonical for canonical, orig in enumerate(sorted_clusters)}
        d["canonical_cluster"] = d["cluster_k3"].map(to_canonical)
        aligned_dfs[y] = d

    # Bảng cross_year_matching.csv giữa các cặp năm liên tiếp
    for i in range(len(years) - 1):
        y_prev, y_curr = years[i], years[i+1]
        c_prev = models[y_prev]["model"]["centroids"]
        c_curr = models[y_curr]["model"]["centroids"]
        sc_prev = raw_contrast_dfs[y_prev].groupby("cluster_k3")["happiness_score"].mean().to_dict()
        sc_curr = raw_contrast_dfs[y_curr].groupby("cluster_k3")["happiness_score"].mean().to_dict()
        
        mapping = match_clusters_greedy(c_prev, c_curr, sc_prev, sc_curr)
        
        for id_curr, id_prev in mapping.items():
            dist = euclidean_distance(c_curr[id_curr], c_prev[id_prev])
            score_diff = abs(sc_curr[id_curr] - sc_prev[id_prev])
            match_rows.append({
                "base_year": y_prev,
                "target_year": y_curr,
                "base_cluster_raw": id_prev,
                "target_cluster_raw": id_curr,
                "base_happiness_mean": round(sc_prev[id_prev], 4),
                "target_happiness_mean": round(sc_curr[id_curr], 4),
                "centroid_euclidean_distance": round(dist, 4),
                "happiness_score_diff": round(score_diff, 4)
            })

    df_matching = pd.DataFrame(match_rows)
    matching_csv_path = tables_dir / "cross_year_matching.csv"
    df_matching.to_csv(matching_csv_path, index=False)
    print(f"Đã lưu bảng ghép cụm liên năm ({len(df_matching)} dòng): {matching_csv_path}")

    # 3. TẠO BẢNG DỊCH CHUYỂN CỤM 156 QUỐC GIA (country_cluster_shift.csv)
    print("=== 3. XÂY DỰNG BẢNG DỊCH CHUYỂN CỤM 156 QUỐC GIA ===")
    # Lấy danh sách 156 quốc gia của năm 2019 làm chuẩn đối sánh đề cương
    df_2019_base = aligned_dfs[2019]
    country_list = sorted(df_2019_base["country"].unique())
    print(f"Số lượng quốc gia năm cơ sở 2019: {len(country_list)}")

    shift_records = []
    for c in country_list:
        row = {"country": c}
        c_labels = []
        for y in years:
            sub = aligned_dfs[y][aligned_dfs[y]["country"] == c]
            if len(sub) > 0:
                lbl = int(sub.iloc[0]["canonical_cluster"])
                row[f"cluster_{y}"] = lbl
                c_labels.append(lbl)
            else:
                row[f"cluster_{y}"] = np.nan
                c_labels.append(None)
        
        # Đánh giá trạng thái dịch chuyển (shift status)
        valid_labels = [l for l in c_labels if l is not None]
        if len(set(valid_labels)) == 1:
            status = "Ổn định tuyệt đối"
        elif valid_labels[-1] < valid_labels[0]:
            status = "Cải thiện nhóm (+)"
        elif valid_labels[-1] > valid_labels[0]:
            status = "Suy giảm nhóm (-)"
        else:
            status = "Biến động trung gian"
            
        row["shift_status"] = status
        row["is_stable"] = (len(set(valid_labels)) == 1)
        shift_records.append(row)

    df_shift = pd.DataFrame(shift_records)
    shift_csv_path = processed_dir / "country_cluster_shift.csv"
    df_shift.to_csv(shift_csv_path, index=False)
    print(f"Đã lưu bảng dịch chuyển cụm 156 quốc gia: {shift_csv_path}")
    print("Phân bố trạng thái dịch chuyển:")
    print(df_shift["shift_status"].value_counts())

    # 4. TẠO BẢNG XU HƯỚNG CỤM (cluster_trends.csv)
    print("=== 4. XÂY DỰNG BẢNG XU HƯỚNG CỤM THEO THỜI GIAN ===")
    trend_rows = []
    cluster_names = {
        0: "Cụm 1 — Hạnh phúc cao (Phát triển toàn diện)",
        1: "Cụm 2 — Hạnh phúc trung bình (Đang phát triển)",
        2: "Cụm 3 — Hạnh phúc thấp (Khó khăn & Thách thức)"
    }
    
    for y in years:
        d = aligned_dfs[y].merge(df_interim[df_interim["year"] == y][["country"] + FEATURE_COLUMNS], on="country", how="left")
        for c_id in [0, 1, 2]:
            sub = d[d["canonical_cluster"] == c_id]
            t_row = {
                "year": y,
                "cluster_id": c_id,
                "cluster_name": cluster_names[c_id],
                "country_count": len(sub),
                "mean_happiness_score": round(sub["happiness_score"].mean(), 4)
            }
            for feat in FEATURE_COLUMNS:
                t_row[f"mean_{feat}"] = round(sub[feat].mean(), 4) if feat in sub.columns else np.nan
            trend_rows.append(t_row)

    df_trends = pd.DataFrame(trend_rows)
    trends_csv_path = tables_dir / "cluster_trends.csv"
    df_trends.to_csv(trends_csv_path, index=False)
    print(f"Đã lưu bảng xu hướng cụm ({len(df_trends)} dòng): {trends_csv_path}")

    # 5. XUẤT CÁC BIỂU ĐỒ TRỰC QUAN HÓA CHUẨN 300 DPI
    print("=== 5. VẼ CÁC HÌNH ẢNH TRỰC QUAN HÓA M3 (CHUẨN 300 DPI) ===")
    sns.set_theme(style="whitegrid")
    plt.rcParams["font.family"] = "sans-serif"

    # Hình A: Biểu đồ xu hướng số lượng quốc gia theo từng cụm (cluster_count_trend.png)
    plt.figure(figsize=(10, 6))
    for c_id, color in [(0, "#2ecc71"), (1, "#f39c12"), (2, "#e74c3c")]:
        sub = df_trends[df_trends["cluster_id"] == c_id]
        plt.plot(sub["year"], sub["country_count"], marker="o", linewidth=2.5, markersize=8,
                 label=cluster_names[c_id], color=color)
        for _, r in sub.iterrows():
            plt.text(r["year"], r["country_count"] + 0.8, f"{int(r['country_count'])}", ha="center", fontsize=10, fontweight="bold")
            
    plt.title("Xu Hướng Số Lượng Quốc Gia Trong Từng Cụm (2015–2019)", fontsize=14, pad=15, fontweight="bold")
    plt.xlabel("Năm Khảo Sát", fontsize=12)
    plt.ylabel("Số Lượng Quốc Gia", fontsize=12)
    plt.ylim(20, 95)
    plt.xticks(years)
    plt.legend(loc="upper right", frameon=True, fontsize=10)
    plt.tight_layout()
    plt.savefig(figures_dir / "cluster_count_trend.png", dpi=300)
    plt.close()
    print("Đã xuất hình: cluster_count_trend.png (300 DPI)")

    # Hình B: Lưới PCA 2D phân bố cụm 5 năm (pca_clusters_grid.png)
    fig, axes = plt.subplots(1, 5, figsize=(22, 4.5), sharey=True)
    palette_map = {0: "#2ecc71", 1: "#f39c12", 2: "#e74c3c"}
    
    for idx, y in enumerate(years):
        sub_interim = df_interim[df_interim["year"] == y].dropna(subset=FEATURE_COLUMNS).reset_index(drop=True)
        # Chuẩn hóa standard
        X_mat = sub_interim[FEATURE_COLUMNS].values
        X_scaled = (X_mat - X_mat.mean(axis=0)) / X_mat.std(axis=0)
        pca = SimplePCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)
        
        # Gán nhãn canonical
        merged_lbl = sub_interim.merge(aligned_dfs[y][["country", "canonical_cluster"]], on="country", how="left")
        lbls = merged_lbl["canonical_cluster"].fillna(1).astype(int).values
        
        ax = axes[idx]
        for c_id in [0, 1, 2]:
            mask = (lbls == c_id)
            ax.scatter(X_pca[mask, 0], X_pca[mask, 1], c=palette_map[c_id], label=f"Cụm {c_id+1}" if idx==0 else "", s=50, alpha=0.8)
        ax.set_title(f"Năm {y} (n={len(sub_interim)})", fontsize=12, fontweight="bold")
        ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)", fontsize=10)
        if idx == 0:
            ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)", fontsize=10)
        ax.grid(True, linestyle="--", alpha=0.5)

    fig.suptitle("Lưới Phân Bố 3 Cụm Quốc Gia Trên Không Gian 2D PCA (2015–2019)", fontsize=15, y=1.03, fontweight="bold")
    fig.legend(loc="upper center", bbox_to_anchor=(0.5, 0.02), ncol=3, frameon=True, fontsize=11)
    plt.tight_layout()
    plt.savefig(figures_dir / "pca_clusters_grid.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("Đã xuất hình: pca_clusters_grid.png (300 DPI)")

    # Hình C: Hậu kiểm Happiness Score theo cụm (validation_happiness_score_by_cluster.png)
    plt.figure(figsize=(10, 6))
    all_aligned = pd.concat([aligned_dfs[y] for y in years], ignore_index=True)
    all_aligned["cluster_label"] = all_aligned["canonical_cluster"].map(cluster_names)
    
    sns.boxplot(
        data=all_aligned,
        x="year",
        y="happiness_score",
        hue="cluster_label",
        palette=["#2ecc71", "#f39c12", "#e74c3c"]
    )
    plt.title("Hậu Kiểm Độc Lập: Phân Bố Điểm Hạnh Phúc (Happiness Score) Giữa 3 Cụm (2015–2019)", fontsize=13, pad=15, fontweight="bold")
    plt.xlabel("Năm Khảo Sát", fontsize=11)
    plt.ylabel("Điểm Hạnh Phúc (Happiness Score)", fontsize=11)
    plt.legend(title="Phân Cụm Tự Nhiên", loc="lower right", frameon=True, fontsize=9)
    plt.tight_layout()
    plt.savefig(figures_dir / "validation_happiness_score_by_cluster.png", dpi=300)
    plt.close()
    print("Đã xuất hình: validation_happiness_score_by_cluster.png (300 DPI)")

    # Hình D: Radar chart chân dung 3 cụm (radar_chart_clusters.png)
    feature_vn = ["GDP/người", "Hỗ trợ XH", "Tuổi thọ", "Tự do", "Hào phóng", "Chống tham nhũng"]
    mean_profiles = df_interim.merge(all_aligned[["country", "year", "canonical_cluster"]], on=["country", "year"]).groupby("canonical_cluster")[FEATURE_COLUMNS].mean()
    
    num_vars = len(FEATURE_COLUMNS)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    radar_colors = {0: "#2ecc71", 1: "#f39c12", 2: "#e74c3c"}
    
    for idx, row in mean_profiles.iterrows():
        vals = row[FEATURE_COLUMNS].tolist()
        vals += vals[:1]
        ax.plot(angles, vals, linewidth=2.5, label=cluster_names[idx], color=radar_colors[idx])
        ax.fill(angles, vals, alpha=0.15, color=radar_colors[idx])
        
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), feature_vn, fontsize=11, fontweight="bold")
    ax.set_title("Chân Dung Radar 6 Yếu Tố Giữa 3 Cụm Quốc Gia (Trung Bình 5 Năm)", y=1.08, fontsize=14, fontweight="bold")
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), frameon=True)
    plt.tight_layout()
    plt.savefig(figures_dir / "radar_chart_clusters.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("Đã xuất hình: radar_chart_clusters.png (300 DPI)")

    # Hình E, F, G: EDA figures nếu chưa có
    for fig_name, draw_fn in [
        ("feature_distributions.png", lambda: _draw_distributions(df_interim)),
        ("correlation_heatmap.png", lambda: _draw_correlation(df_interim)),
        ("boxplots_outliers.png", lambda: _draw_outliers(df_interim))
    ]:
        if not (figures_dir / fig_name).exists():
            draw_fn()
            print(f"Đã xuất hình EDA bổ sung: {fig_name} (300 DPI)")

    print("\n=== HOÀN TẤT SINH DỮ LIỆU VÀ TRỰC QUAN HÓA M3 ===")

def _draw_distributions(df):
    plt.figure(figsize=(14, 8))
    for i, col in enumerate(FEATURE_COLUMNS, 1):
        plt.subplot(2, 3, i)
        sns.histplot(df[col], kde=True, color="#3498db")
        plt.title(f"Phân bố: {col}", fontsize=11, fontweight="bold")
    plt.tight_layout()
    plt.savefig(figures_dir / "feature_distributions.png", dpi=300)
    plt.close()

def _draw_correlation(df):
    plt.figure(figsize=(8, 6))
    corr = df[FEATURE_COLUMNS + ["happiness_score"]].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
    plt.title("Ma Trận Tương Quan Pearson (6 Yếu Tố & Điểm Hạnh Phúc)", fontsize=12, pad=12, fontweight="bold")
    plt.tight_layout()
    plt.savefig(figures_dir / "correlation_heatmap.png", dpi=300)
    plt.close()

def _draw_outliers(df):
    plt.figure(figsize=(12, 6))
    # Min-max scale để vẽ chung boxplot
    sub = df[FEATURE_COLUMNS]
    scaled = (sub - sub.min()) / (sub.max() - sub.min())
    sns.boxplot(data=scaled, palette="Set3")
    plt.title("Biểu Đồ Hộp Phát Hiện Giá Trị Ngoại Lai (6 Đặc Trưng Sau Chuẩn Hóa)", fontsize=13, pad=12, fontweight="bold")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(figures_dir / "boxplots_outliers.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    main()
