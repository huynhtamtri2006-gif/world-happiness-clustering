# Kế hoạch thực thi Đề tài 16 — Nhóm 12 (3 thành viên) — Bản chốt sau phỏng vấn

> **Học phần:** Khai thác dữ liệu — **Đề tài 16:** Phân nhóm quốc gia theo các yếu tố tạo nên mức độ hạnh phúc (World Happiness Report)
> **Nhóm:** 12 — Hà Mạnh Trường (nhóm trưởng), Huỳnh Tâm Trí, Ngô Quang Trung
> **Thời lượng:** 28 ngày (4 tuần), họp 1 buổi/tuần (4 buổi)
> **Sản phẩm:** mã nguồn + 4 notebook + demo Streamlit + báo cáo Word + slide

---

## 1. Baseline quyết định (đã chốt qua phỏng vấn)

| # | Quyết định | Giá trị đã chốt |
|:--:|:--|:--|
| 1 | Phạm vi dữ liệu | **5 thí nghiệm song song**, mỗi năm 2015-2019 gom cụm **độc lập**, sau đó so sánh xu hướng |
| 2 | Ma trận đặc trưng $X$ | Đúng 6 yếu tố cơ sở; **không** dùng `happiness_score`/`happiness_rank` (chỉ hậu kiểm ở notebook 04) |
| 3 | Chọn `k` | Khảo sát `k ∈ [2, 9]` mỗi năm bằng Elbow + Silhouette; **`k*` là kết quả chính**, **`k=3` là mục đối chứng** |
| 4 | Ma trận cấu hình lõi | 5 cấu hình × 5 năm: K-Means/Standard, K-Means/Min-Max, K-Means/không scale, Ward/Standard, DBSCAN/Standard |
| 5 | Quét DBSCAN | Đầy đủ: `eps ∈ {0.6, 0.8, 1.0, 1.2}` × `min_samples ∈ {3, 4, 5}` cho mỗi năm |
| 6 | Độ ổn định | ARI 10 seed cho các cấu hình **có khởi tạo ngẫu nhiên** (3 cấu hình K-Means); Ward và DBSCAN tất định → ghi 1.0 kèm giải thích |
| 7 | Ghép cụm liên năm | Ghép tham lam theo khoảng cách tâm cụm (đã chuẩn hóa), hoà thì xét `happiness_score` trung bình |
| 8 | Bảng dịch chuyển cụm | **Chính thức trong báo cáo**: bảng 156 quốc gia × 5 năm |
| 9 | Kiểm chứng | `scripts/verify_scratch_implementations.py` assert đối chứng sklearn/scipy + notebook chạy sạch bằng nbconvert |
| 10 | Báo cáo Word & Quy chuẩn nộp bài | Nhóm sinh viên trực tiếp biên soạn theo cấu trúc **5 Chương chuẩn hóa**; tuân thủ nghiêm ngặt văn phong người thật thực chứng (**Anti-AI Writing Style**), truy vết 100% số liệu về CSV; nộp gói nén duy nhất `Nhom12_WorldHappinessClustering.zip` gồm `Nhom12_BaoCao.docx`, video báo cáo $\le$ 12 phút (link mở trực tiếp ở trang bìa và phụ lục) và toàn bộ mã nguồn |
| 11 | Phân công | Trường 34% — Trí 33% — Trung 33% |
| 12 | Nơi lưu kế hoạch | GitHub Issue trên `world-happiness-clustering` + bản markdown trong repo |

**Nghiệm thu (đo được):**

1. `python scripts/verify_scratch_implementations.py` → PASS toàn bộ, exit code 0.
2. 4 notebook chạy sạch; sinh `data/interim/happiness_merged.csv`, `data/processed/**`, `reports/figures/*.png` (300 DPI), `reports/tables/*.csv`.
3. `streamlit run app/app.py` chạy, 4 tab thật; đổi năm / thuật toán / scaler / `k` thì số liệu và metric đổi theo (không hardcode).
4. `models/*.json` chứa tâm cụm + tham số scaler + metric cho từng năm, đọc lại được.
5. Bộ nộp đủ: Gói nén duy nhất `Nhom12_WorldHappinessClustering.zip` gồm `Nhom12_BaoCao.docx` (5 Chương chuẩn hóa), video $\le$ 12 phút (cả 3 thành viên thuyết trình, link mở trực tiếp ở bìa và phụ lục), `Slide_De_tai_16_Nhom_12.pptx`, `ke_hoach_nhom.md`, `phan_cong_cong_viec.md`, toàn bộ mã nguồn và README hướng dẫn chạy.
6. Checklist ký xác nhận nội dung báo cáo: cả 3 thành viên đã đọc, đối chiếu số với `reports/tables/*.csv` và giải thích được mục mình phụ trách.

### Hiện trạng repo (đã kiểm chứng)

| Hạng mục | Trạng thái |
|:--|:--|
| Dữ liệu thô | `data/raw/2015..2019.csv` (158/157/155/156/156 dòng). 2018 thiếu `Perceptions of corruption` ở **United Arab Emirates** |
| `src/data/data_loader.py` | Chạy được (`COLUMN_MAPPING`, `standardize_columns`, `load_year_data`, `load_raw_data`) nhưng chưa có hàm dựng bảng interim |
| `src/features/feature_engineering.py` | Scaler tự viết OK; `apply_pca` đang gọi `sklearn.decomposition.PCA` (trái tinh thần ADR 0001) |
| `src/models/clustering.py` | **Thiếu** `run_kmeans`, `run_hierarchical`, `run_dbscan`, `evaluate_clustering`, `find_optimal_k_kmeans` → notebook 03/04 chạy là ImportError; `SimpleHierarchicalClustering` đang là centroid linkage nhưng notebook ghi `linkage='ward'`; vòng lặp O(n³) quá chậm |
| `data/interim/`, `data/processed/` | Trống |
| `app/app.py` | Placeholder: radar hardcode, tab bản đồ trống |
| `reports/` | `figures/`, `final_report/` trống; chưa có `tables/` |
| Kiểm thử | Không có `tests/`, chưa cài `pytest` |
| `requirements.txt` | Dải `>=`, không khớp môi trường thật (Python 3.12.10, numpy 2.5.3, pandas 3.0.5, plotly 7.1.0, streamlit 1.64.0, sklearn 1.9.1, scipy 1.18.1) |
| `.gitignore` | Đang ignore `README.md` dù README là sản phẩm bắt buộc nộp |
| Git | remote `https://github.com/mtzwyu/world-happiness-clustering.git`, nhánh `main`, tree sạch |

---

## 2. Bảng phân công công việc và tỷ lệ đóng góp

| Thành viên | Công việc chính | Công việc hỗ trợ | Tỷ lệ đóng góp (%) |
|:--|:--|:--|:--:|
| **Hà Mạnh Trường** (2045240326, nhóm trưởng) | WS1 — pipeline dữ liệu 5 năm: `src/data/data_loader.py`, notebook 01, `data/interim/`. WS8 — tái lập: chốt phiên bản `requirements.txt`, README, `scripts/verify_scratch_implementations.py`, `.gitignore`. Điều phối Git/PR. Ghép báo cáo Word (`build_report.py`), viết mục 1-4 báo cáo | Review `src/models/clustering.py`; chạy lại notebook 03 đối chiếu số liệu giữa 5 năm; hỗ trợ nạp dữ liệu cho app | **34** |
| **Huỳnh Tâm Trí** (2045240315) | WS2+WS3 — `src/features/feature_engineering.py` (PCA tự viết) và `src/models/clustering.py`: Ward thật, DBSCAN from scratch, Davies-Bouldin/Calinski-Harabasz/ARI, wrapper `run_*`, artifact JSON. Notebook 03: khảo sát `k` theo 5 năm, ma trận 5 cấu hình, quét DBSCAN đầy đủ. Viết mục 5-7 báo cáo | Review `data_loader.py`; kiểm chứng metric bằng sklearn; review wiring dữ liệu của app | **33** |
| **Ngô Quang Trung** (2045240325) | WS5+WS6 — EDA và diễn giải: notebook 02, notebook 04, `src/visualization/plots.py`, hậu kiểm `happiness_score`, **ghép cụm liên năm + bảng dịch chuyển 156 × 5**; `app/app.py` (4 tab, chọn năm 2015-2019); slide; viết mục 8-11 báo cáo | Review notebook 01; kiểm tra chất lượng dữ liệu; kiểm bản đồ ISO-3; điều hành rehearsal | **33** |

**Cơ chế bắt buộc để mỗi thành viên hiểu toàn bộ pipeline (Mục 1.1):**

- Mỗi module khi xong phải có **walkthrough 20 phút** do chính người viết trình bày cho 2 người còn lại; ghi biên bản vào mục 7.
- **Rehearsal đổi vai:** Trường trình bày phương pháp, Trí trình bày demo, Trung trình bày tiền xử lý.
- Mỗi người phải giải thích được công thức Silhouette + profile một cụm của **một năm bất kỳ** + một đoạn code bất kỳ trong `src/models/clustering.py`.
- Mỗi PR bắt buộc một người khác review.

**Cam kết biên tập, truy vết số liệu và loại bỏ dấu hiệu AI:**

- Mọi con số trong Báo cáo Word 5 Chương phải truy được về một dòng trong `reports/tables/*.csv` hoặc một hình trong `reports/figures/`.
- Tuân thủ triệt để quy chuẩn **Anti-AI Writing Style**: không mở bài sáo rỗng, không tính từ phóng đại, không dùng từ nối máy móc lặp lại; thể hiện rõ bản chất kỹ thuật và quá trình thử-sai của sinh viên thực hiện.
- Mỗi thành viên biên tập các chương mục mình phụ trách, rồi **ký xác nhận** vào checklist ở `phan_cong_cong_viec.md`: đã đọc, đã đối chiếu số, giải thích được.
- Trước khi nộp, mỗi người phải chạy lại được notebook của phần mình và trả lời 20 câu vấn đáp.

---

## 3. Lịch 28 ngày — 5 mốc, 4 buổi họp (Ngày 1, 8, 15, 22)

### M0 — Chốt baseline và ghi quyết định (Ngày 1-2)

| Ngày | Trường | Trí | Trung |
|:--:|:--|:--|:--|
| 1 (họp) | Chủ trì chốt baseline ở Mục 1; ghi `docs/adr/0002-*.md`; cập nhật `CONTEXT.md` | Rà công thức phải tự viết: Ward/Lance–Williams, DBSCAN, DB, CH, ARI, PCA; chốt chữ ký hàm | Chốt danh mục hình (12 hình) và layout 4 tab demo |
| 2 | Hoàn thiện `ke_hoach_nhom.md` + `phan_cong_cong_viec.md` | Chuẩn bị khung dữ liệu test nhỏ để đối chứng sklearn/scipy | Liệt kê câu hỏi kỹ thuật cần trả lời trong báo cáo (mục 11) |

### M1 — Nền dữ liệu 5 năm và tái lập (Ngày 3-7)

| Ngày | Trường | Trí | Trung |
|:--:|:--|:--|:--|
| 3 | Thêm API vào `data_loader.py`: `INTERIM_COLUMNS`, `build_interim_dataset` (5 năm), `harmonize_country_names`, `COUNTRY_NAME_FIXES`, `COUNTRY_ISO3_OVERRIDES`, `country_to_iso3`, `load_interim`, `load_processed` | Khung `scripts/verify_scratch_implementations.py`: assert bất biến $X$ + Euclid + Silhouette | Bảng chất lượng dữ liệu theo từng năm (missing, trùng, lệch tên cột, lệch tên quốc gia) |
| 4 | Sửa notebook 01, sinh `data/interim/happiness_merged.csv` (5 năm); bỏ cột `Standard Error`, CI, `Whisker.*` kèm lý do | Assert K-Means: inertia ≤ sklearn + dung sai, ARI ≥ 0.99 sau khớp nhãn | Thu thập nguồn: Data Card Kaggle WHR + phương pháp Cantril Ladder/Dystopia → `docs/nghien_cuu/whr_nguon_du_lieu.md` |
| 5 | Sửa `.gitignore` (bỏ ignore `README.md`); `requirements.txt` chốt `==` + `python-docx`, `python-pptx` | Assert Ward vs `scipy linkage('ward')`, DBSCAN vs sklearn | Kiểm lệch tên quốc gia giữa 5 năm (`Macedonia`/`North Macedonia`, `Swaziland`) và chốt `COUNTRY_NAME_FIXES` |
| 6 | `README.md`: bảng đóng góp 34/33/33, hướng dẫn chạy lại từ đầu; `notebooks/README.md`: bỏ khẳng định cứng `k=3` | Assert DB, CH, PCA khớp sklearn | Xác nhận 2018 loại UAE; ghi rõ cỡ mẫu mỗi năm (158/157/155/156/156) |
| 7 | Review chéo: notebook 01 chạy sạch từ đầu trên máy sạch | Verify script chạy hết (có thể còn FAIL ở Ward — chuyển sang M2) | Bản nháp 20 câu vấn đáp |

### M2 — Thuật toán và độ đo (Ngày 8-14)

| Ngày | Trường | Trí | Trung |
|:--:|:--|:--|:--|
| 8 (họp) | Chốt tiến độ M1, chốt chữ ký API cuối cùng trước khi Trí code | Bắt đầu `SimpleKMeans`: `n_init=10`, `init='kmeans++'`, `inertia_history`, `n_iter_` | `plots.py`: thêm `plot_dendrogram`, `plot_cluster_profiles_bar`, `plot_happiness_score_by_cluster` |
| 9 | Rà `.gitignore` lần cuối; kiểm đường dẫn tương đối trong mọi notebook | `SimpleHierarchicalClustering`: **Ward thật** bằng cache tâm cụm + Lance–Williams, `merge_history` | Notebook 02 (EDA): skew, histogram/KDE, heatmap tương quan, boxplot outlier |
| 10 | Hỗ trợ Trí gỡ lỗi hiệu năng | `SimpleDBSCAN` from scratch (vùng lân cận, nhãn `-1` = nhiễu) | Hoàn thiện hình EDA 300 DPI |
| 11 | Viết `scripts/demo_setup_wizard` cho máy demo (cùng Trung) | `run_kmeans`/`run_hierarchical`/`run_dbscan` + `evaluate_clustering` (giá trị phẳng, `sizes` dạng `"3/45/108"`) | Kiểm thời gian chạy 5 năm × n điểm, ghi log |
| 12 | Soát docstring tiếng Việt + công thức trong `clustering.py` | `calculate_davies_bouldin_score_simple`, `calculate_calinski_harabasz_score_simple`, `calculate_adjusted_rand_index` | Kiểm Ward trên 156 điểm: mục tiêu < 30 giây/lần chạy |
| 13 | Chạy verify script lần 1, ghi log vào `reports/tables/` | `SimplePCA` tự viết (`np.linalg.eigh`), giữ nguyên chữ ký `apply_pca`; sửa hết FAIL của verify | Review chéo code Trí |
| 14 | Chốt ADR 0002 + `CONTEXT.md`; cập nhật `requirements.txt` nếu cần | `save_cluster_artifacts`/`load_cluster_artifacts` (JSON) + ghi `models/*.json` | Walkthrough nhận xét code |

### M3 — Thực nghiệm 5 năm × 5 cấu hình và diễn giải (Ngày 15-21)

| Ngày | Trường | Trí | Trung |
|:--:|:--|:--|:--|
| 15 (họp) | Chốt tiến độ M2; chốt cách trình bày `k*` chính + `k=3` đối chứng | Notebook 03: vòng lặp 5 năm; Elbow + Silhouette cho `k ∈ [2,9]` mỗi năm; chốt `k*` mỗi năm | Notebook 04 khung: PCA 2D theo năm, radar profile |
| 16 | Kiểm số liệu `k*` giữa các năm có hợp lý (2-5) | Ma trận lõi 5 cấu hình × 5 năm → `reports/tables/model_comparison_metrics_by_year.csv` | Hậu kiểm `happiness_score` theo cụm cho từng năm |
| 17 | Kiểm CSV khớp notebook | Quét DBSCAN đầy đủ (4 eps × 3 min_samples) → `reports/tables/dbscan_sweep.csv` | Vẽ `elbow_silhouette_by_year.png`, `scaling_comparison.png` |
| 18 | Rà tên cột/khóa giữa các bảng CSV | ARI 10 seed cho 3 cấu hình K-Means × 5 năm → `reports/tables/stability_ari.csv` (Ward/DBSCAN ghi 1.0 + giải thích) | Ghép cụm liên năm (tham lam theo tâm cụm, tie-break `happiness_score`) → `reports/tables/cross_year_matching.csv` |
| 19 | Kiểm bảng dịch chuyển 156 × 5 đủ dòng, không trùng do lệch tên | Mục đối chứng `k=3`: ARI so với `k*` + mức phân hóa `happiness_score` | Bảng dịch chuyển cụm từng quốc gia → `data/processed/country_cluster_shift.csv` + `cluster_count_trend.png` |
| 20 | Rà hình 300 DPI đủ 12 hình | Xuất `data/processed/per_year/*.csv` (kết quả gom cụm + profile từng năm) | Radar profile từng năm; `pca_clusters_grid.png` |
| 21 | Review chéo toàn bộ M3: số liệu khớp, hình có tên | Viết mục 5-7 báo cáo từ CSV | Viết mục 8-11 báo cáo; chốt tên `Cluster Profile` cho từng cụm mỗi năm |

### M4 — Demo, báo cáo, slide (Ngày 22-26)

| Ngày | Trường | Trí | Trung |
|:--:|:--|:--|:--|
| 22 (họp) | Chốt tiến độ M3; chốt phạm vi tối thiểu của báo cáo nếu trễ | Rà `src/models/__init__.py` export đủ; thêm docstring công thức | `app/app.py`: 4 tab (radar theo năm, bản đồ ISO-3, tra cứu quốc gia, gán quốc gia mới) + metric theo cấu hình + cache `mtime` |
| 23 | Chuẩn bị khung Báo cáo Word (`build_report.py`, trang bìa, 5 Chương chuẩn hóa, chèn bảng/hình) | Kiểm app không dùng sklearn; kiểm đổi năm/thuật toán/scaler/`k` ra số khác nhau | Viết `slides.md` + `build_slides.py` (12-15 slide, khớp kịch bản video) |
| 24 | Soạn thảo Báo cáo Word `Nhom12_BaoCao.docx` theo 5 Chương chuẩn hóa từ kết quả thực nghiệm | Soát lại Chương 3 (Phương pháp) và Chương 4 (Kết quả) | Soát lại Chương 4 (Diễn giải), demo và Chương 5 (Kết luận) |
| 25 | Ghép bản cuối; rà soát định dạng, hình/bảng và số liệu | Biên tập + ký xác nhận Chương 3 | Biên tập + ký xác nhận Chương 4, 5 |
| 26 | Biên tập + ký xác nhận Chương 1, 2; kiểm tra số liệu khớp 100% | Kiểm app lần cuối, chuẩn bị phần quay demo video | Hoàn thiện slide, tập dượt quay video $\le$ 12 phút |

### M5 — Đóng băng, quay video, rehearsal, nộp (Ngày 27-28)

| Ngày | Trường | Trí | Trung |
|:--:|:--|:--|:--|
| 27 | Chạy lại toàn bộ từ đầu trên môi trường sạch: 4 notebook + verify + app; phối hợp quay video báo cáo $\le$ 12 phút (cả 3 thành viên tham gia); gắn link video mở trực tiếp vào bìa và phụ lục Word | Tham gia quay video (phần thuật toán & thực nghiệm); trả lời vấn đáp phần phương pháp | Tham gia quay video (phần diễn giải & demo app); điều hành rehearsal |
| 28 | Đóng gói duy nhất `Nhom12_WorldHappinessClustering.zip`; merge `main`, push GitHub; nộp bài | Bị hỏi vấn đáp phần demo | Bị hỏi vấn đáp phần kết luận/hạn chế |

**Nhịp chung:** họp 1 buổi/tuần vào đầu tuần (Ngày 1, 8, 15, 22), mỗi buổi 45 phút: chốt tiến độ mốc trước, gỡ blocker, chốt việc tuần. Ngoài buổi họp, trao đổi qua PR + checklist trong tài liệu này. Commit bằng Tiếng Việt theo chuẩn **Human-Centric Commit Protocol** (ví dụ: `thuật toán: tự cài đặt Ward linkage và DBSCAN from scratch`), tuyệt đối không nhắc đến AI hay bot. Nhánh `feat/<tên>-<nội-dung>` → PR → chỉ nhóm trưởng merge `main`.

---

## 4. Thay đổi kỹ thuật theo file

Quy ước: docstring/comment tiếng Việt, tên hàm/biến tiếng Anh; `scikit-learn`/`scipy` **chỉ** trong `scripts/verify_scratch_implementations.py`.

| File | Thay đổi |
|:--|:--|
| `src/data/data_loader.py` | Giữ API cũ; thêm `INTERIM_COLUMNS`, `build_interim_dataset(years=[2015..2019], raw_dir=None)`, `harmonize_country_names`, `COUNTRY_NAME_FIXES`, `COUNTRY_ISO3_OVERRIDES`, `country_to_iso3`, `load_interim`, `load_processed` |
| `src/features/feature_engineering.py` | Giữ scaler tự viết + `scale_features`; thay `apply_pca` bằng `SimplePCA` (hiệp phương sai → `np.linalg.eigh` → chiếu), giữ nguyên chữ ký `apply_pca(X_scaled, n_components=2, random_state=42)` |
| `src/models/clustering.py` | `SimpleKMeans` (+`n_init`, `kmeans++`, `inertia_history`, `n_iter_`); `SimpleHierarchicalClustering` **Ward thật** (cache tâm cụm + Lance–Williams, `merge_history`); `SimpleDBSCAN`; `run_kmeans`/`run_hierarchical`/`run_dbscan`; `calculate_davies_bouldin_score_simple`, `calculate_calinski_harabasz_score_simple`, `calculate_adjusted_rand_index`, `evaluate_clustering`; `find_optimal_k_kmeans` (giữ alias `find_optimal_k_scratch`); `save_cluster_artifacts`/`load_cluster_artifacts`; `match_clusters_greedy(centroids_a, centroids_b, scores_a, scores_b)` cho ghép cụm liên năm |
| `src/models/__init__.py` | Export toàn bộ API mới |
| `src/visualization/plots.py` | Thêm `plot_dendrogram`, `plot_cluster_profiles_bar`, `plot_happiness_score_by_cluster`; giữ 3 hàm cũ; tất cả 300 DPI |
| `notebooks/01` | Dựng bảng interim 5 năm; bảng chất lượng dữ liệu theo năm; ghi lý do bỏ cột và lý do loại UAE 2018 |
| `notebooks/02` | EDA trên 5 năm: skew, histogram/KDE, heatmap tương quan, boxplot; kết luận chọn scaler |
| `notebooks/03` | Vòng lặp 5 năm: Elbow/Silhouette `k ∈ [2,9]`, chốt `k*`; ma trận 5 cấu hình × 5 năm; quét DBSCAN đầy đủ; ARI 10 seed; mục đối chứng `k=3`; xuất toàn bộ CSV |
| `notebooks/04` | PCA 2D theo năm; radar profile; hậu kiểm `happiness_score`; tên `Cluster Profile`; ghép cụm liên năm; bảng dịch chuyển 156 × 5; xuất `data/processed/**`; viết Mục 11 theo số liệu thật |
| `app/app.py` | 4 tab + chọn năm 2015-2019 + chọn cấu hình/scaler/`k` + hiển thị metric + bảng dịch chuyển; cache `mtime`; dự phòng dựng từ `data/raw` |
| `scripts/verify_scratch_implementations.py` | Bất biến $X$; K-Means vs sklearn; Ward vs scipy; DBSCAN vs sklearn; Silhouette/DB/CH khớp sklearn; PCA khớp `explained_variance_ratio` |
| `.gitignore`, `README.md`, `notebooks/README.md`, `requirements.txt` | Bỏ ignore `README.md`; README: % đóng góp + hướng dẫn chạy; chốt phiên bản `==` |
| `reports/final_report/` | `ke_hoach_nhom.md`, `phan_cong_cong_viec.md`, `bao_cao.md` + `build_report.py` (2 backend: OOXML thuần Python mặc định, `python-docx` nếu cài được; chèn bảng từ CSV, chèn hình từ `reports/figures/`, chú thích Hình/Bảng, tạo mục lục bằng field TOC), `slides.md` + `build_slides.py`, `q_and_a.md` |
| `docs/` | `docs/adr/0002-*.md`, `CONTEXT.md`, `docs/nghien_cuu/*.md` |

---

## 5. Luồng dữ liệu và artifact

```text
data/raw/2015..2019.csv
  └─(build_interim_dataset)→ data/interim/happiness_merged.csv  (5 năm, schema thống nhất)
       ├─(notebook 02)→ reports/figures/{feature_distributions,correlation_heatmap,boxplots_outliers}.png
       └─(notebook 03, lặp theo từng năm 2015-2019)
             ├─ reports/tables/{k_sensitivity_by_year, model_comparison_metrics_by_year,
             │                  dbscan_sweep, stability_ari}.csv
             ├─ reports/figures/{elbow_silhouette_by_year, scaling_comparison, dbscan_sweep_heatmap,
             │                  stability_ari_heatmap, dendrogram_ward_*.png}
             └─ models/*.json (tâm cụm + scaler + metric theo năm và cấu hình)
                   └─(notebook 04: SimplePCA + profile + hậu kiểm + ghép cụm liên năm)
                         ├─ data/processed/per_year/{final_clustered_<year>, cluster_profiles_<year>}.csv
                         ├─ data/processed/country_cluster_shift.csv         (156 quốc gia × 5 năm)
                         ├─ data/processed/cluster_trends.csv                (số lượng + profile theo năm)
                         ├─ reports/tables/cross_year_matching.csv
                         └─ reports/figures/{pca_clusters_grid, radar_chart_clusters_*,
                                             validation_happiness_score_by_cluster, cluster_count_trend}.png
                               └─(app/app.py, reports/final_report/*)
```

Tổng 12 hình cho báo cáo; CSV là nguồn số liệu duy nhất, mọi con số trong `bao_cao.md` phải truy được về CSV.

---

## 6. Trường hợp biên và kiểm thử

**Trường hợp biên:**

1. Cỡ mẫu khác nhau giữa các năm (158/157/155/156/156) → mọi so sánh xu hướng phải ghi rõ cỡ mẫu.
2. `region` chỉ có ở 2015-2016 → không dùng cho phân tích chính; ghi rõ trong hạn chế.
3. UAE thiếu `corruption_perception` ở 2018 → loại khỏi thực nghiệm 2018, ghi rõ.
4. Lệch tên quốc gia giữa các năm (`Macedonia`/`North Macedonia`, `Swaziland`/`Eswatini`) → `COUNTRY_NAME_FIXES` để bảng dịch chuyển không tách dòng.
5. Nhãn cụm không so sánh trực tiếp giữa các năm → ghép tham lam theo tâm cụm; nếu `k*` khác nhau giữa 2 năm thì chỉ ghép được `min(k1, k2)` cụm, phần còn lại ghi là "không có cặp tương ứng".
6. `k*` khác nhau giữa các năm → mục đối chứng `k=3` là cấu hình duy nhất so sánh được xuyên năm, dùng làm chuẩn diễn giải.
7. Cụm rỗng trong K-Means → gán lại điểm + ghi log; Silhouette với cụm 1 điểm → $s(i)=0$.
8. std = 0 (Z-score) và max = min (Min-Max) → giữ guard hiện có.
9. K-Means trên dữ liệu **không scale** có thể cho 1 cụm áp đảo (do `gdp_per_capita` lệch mạnh) → đây là kết quả cần báo cáo, không phải lỗi; phải nêu trong phần phân tích độ nhạy.
10. DBSCAN toàn nhiễu hoặc 1 cụm → cảnh báo, không tính Silhouette vô nghĩa.
11. Ward chậm → cache tâm cụm + Lance–Williams; mục tiêu < 30 giây cho 156 điểm; nếu vượt, giảm số cấu hình chạy ARI và để app dùng JSON artifact.
12. Chi phí tính toán 5 năm: cache toàn bộ kết quả vào CSV/JSON để app và báo cáo không phải fit lại.
13. ARI: Ward và DBSCAN tất định → ARI = 1.0, ghi rõ lý do thay vì chạy thừa.
14. Notebook phụ thuộc thứ tự chạy → 01 sinh interim, 02/03/04 đọc lại; assert kèm hướng dẫn.
15. pandas 3.0 / numpy 2.x → tránh API đã bỏ.
16. Streamlit cache cũ → cache theo `mtime`; dự phòng dựng từ `data/raw`.
17. Conflict `.ipynb` giữa 3 người → mỗi notebook 1 owner tại một thời điểm.

**Kiểm thử:**

| Loại | Cách chạy | Kỳ vọng |
|:--|:--|:--|
| Đối chứng thuật toán | `python scripts/verify_scratch_implementations.py` | PASS toàn bộ, exit 0 |
| Bất biến quy tắc vàng | trong verify script | $X$ không chứa `happiness_score`/`happiness_rank` |
| Notebook chạy sạch | `python -m nbconvert --to notebook --execute --output-dir .scratch/_exec notebooks/0X_*.ipynb`; khi đóng gói dùng `--inplace` | Không cell lỗi |
| Demo | `streamlit run app/app.py`; thao tác 4 tab, đổi năm/thuật toán/scaler/`k` | Số liệu đổi theo cấu hình, không hardcode |
| Truy vết số liệu | Đối chiếu từng con số trong `bao_cao.md` với `reports/tables/*.csv` | 100% khớp |
| Báo cáo/slide | `python reports/final_report/build_report.py`, `build_slides.py` | Sinh `.docx`/`.pptx`; hình có chú thích |
| Checklist nộp | Đối chiếu 10 mục Mục 5 đề cương | 100% tick |

---

## 7. Biên bản walkthrough và rehearsal

| Ngày | Nội dung | Người trình bày | Người nghe | Ghi chú |
|:--:|:--|:--|:--|:--|
| 7 | Walkthrough WS1 + notebook 01 (5 năm) | Trường | Trí, Trung | |
| 14 | Walkthrough WS2 + WS3 + verify script | Trí | Trường, Trung | |
| 21 | Walkthrough WS5 + notebook 04 + ghép cụm liên năm | Trung | Trường, Trí | |
| 28 | Rehearsal đổi vai (3 phần) + 20 câu vấn đáp | cả nhóm | cả nhóm | |

---

## 8. Rủi ro và giả định

| Rủi ro | Giảm thiểu |
|:--|:--|
| 5 năm × 5 cấu hình × quét DBSCAN quá nhiều bảng/hình | Cố định 12 hình và 5 file CSV; phần còn lại để trong phụ lục; cache kết quả vào CSV/JSON |
| Ward chậm | Lance–Williams + cache; hạ phạm vi ARI nếu vượt 30 giây/lần |
| Báo cáo Word bị nghi ngờ có dấu hiệu văn phong AI dẫn đến mất điểm nội dung (3,0đ) | Tuân thủ triệt để Anti-AI Writing Style, viết từ góc nhìn sinh viên KHDL thực chứng, bám sát số liệu định lượng, mô tả quá trình thử-sai, truy vết 100% về CSV + ký xác nhận từng mục |
| `k*` khác nhau giữa các năm gây khó kể chuyện | Dùng `k=3` làm cấu hình đối chứng xuyên năm; `k*` là kết quả chính theo từng năm |
| Trễ tiến độ ở M3 | Đường găng tối thiểu: K-Means/Standard + Ward/Standard × 5 năm + `k=3` đối chứng; phần quét DBSCAN đầy đủ và ARI lùi sang M4 |
| Conflict notebook giữa 3 người | 1 owner/notebook tại một thời điểm |

**Giả định:** 28 ngày; mỗi người ~50 giờ (tổng ~150 giờ, tăng so với 18 ngày do phạm vi 5 năm); **không phụ thuộc mạng để build báo cáo** (máy đã có Word 16.0 nhưng chưa cài được `python-docx`/`python-pptx`); nộp qua GitHub + file Word/Slide; tài liệu và commit bằng tiếng Việt theo `AGENTS.md`.

---

## 9. Việc đầu tiên (Ngày 1)

1. Họp chốt baseline ở Mục 1; ghi `docs/adr/0002-*.md`, cập nhật `CONTEXT.md`.
2. Hoàn thiện hai tài liệu này (kế hoạch + bảng phân công) và tạo GitHub Issue lưu kế hoạch.
3. Sửa `.gitignore` (bỏ ignore `README.md`); chốt `requirements.txt` theo `==`.
4. WS1: thêm API vào `src/data/data_loader.py`, sinh `data/interim/happiness_merged.csv` 5 năm, sửa và chạy sạch notebook 01.
5. Trí: viết khung `scripts/verify_scratch_implementations.py` (assert trước), rồi sửa `SimpleHierarchicalClustering` sang Ward thật, thêm `SimpleDBSCAN`, `run_*`, `evaluate_clustering`, `SimplePCA`.
