# BẢN PHÂN TÍCH NHIỆM VỤ CÁ NHÂN — HUỲNH TÂM TRÍ
## Đề tài 16: Phân nhóm quốc gia theo các yếu tố hạnh phúc (World Happiness Report)

---

### 👤 THÔNG TIN THÀNH VIÊN
- **Họ và tên:** Huỳnh Tâm Trí
- **Mã số sinh viên:** 2045240315
- **Vai trò trong nhóm:** Thành viên
- **Tỷ lệ đóng góp cam kết:** **33%**
- **Trách nhiệm chính:** Kỹ sư Thuật toán & Mô hình hóa (From-Scratch Clustering & Evaluation), Thực nghiệm 5 cấu hình × 5 năm, Khảo sát tham số, Viết Mục 5–7 báo cáo.
- **Trách nhiệm hỗ trợ:** Rà soát bộ nạp dữ liệu của Trường, kiểm chứng các độ đo bằng thư viện chuẩn, rà soát luồng nối dữ liệu cho ứng dụng Demo của Trung.

---

### 🎯 MỤC TIÊU & PHẠM VI PHỤ TRÁCH THEO ĐỀ CƯƠNG
Phụ trách chính **Giai đoạn 6, 7, 8** của pipeline khai phá dữ liệu:
1. **Mục 5 — Phương pháp luận mô hình hóa (From-Scratch Algorithms):** Tự cài đặt 100% các thuật toán gom cụm (K-Means, Phân cấp Ward, DBSCAN), giảm chiều PCA và các độ đo đánh giá mà không gọi API black-box có sẵn.
2. **Mục 6 — Tinh chỉnh tham số & Đo độ ổn định:** Khảo sát chọn số cụm tối ưu $k^*$ theo từng năm (Elbow + Silhouette), quét siêu tham số DBSCAN toàn diện, kiểm tra tính bền vững của các cụm qua nhiều seed khởi tạo (Adjusted Rand Index).
3. **Mục 7 — So sánh và đánh giá các phương án:** Đánh giá định lượng 5 cấu hình gom cụm lõi qua 5 năm độc lập (Z-score vs Min-Max vs Raw; K-Means vs Ward vs DBSCAN).

---

### 📅 KẾ HOẠCH CHI TIẾT THEO 5 MỐC THỜI GIAN (28 NGÀY)

#### 🔹 Mốc M0: Nghiên cứu công thức & Thiết kế chữ ký hàm (Ngày 1 – Ngày 2)
- [x] **Ngày 1 (Họp nhóm):** Rà soát cơ sở lý thuyết toán học cần tự lập trình từ đầu:
  - Công thức khoảng cách Euclidean đa chiều.
  - Cơ chế chọn tâm cụm K-Means++ và bước cập nhật tâm theo trọng tâm cụm.
  - Công thức đệ quy Lance–Williams cập nhật khoảng cách trong phân cấp liên kết Ward.
  - Lan truyền mật độ trong DBSCAN (vùng lân cận $\epsilon$, điểm lõi, điểm biên, điểm nhiễu $-1$).
  - Thuật toán giảm chiều PCA bằng phân tích ma trận hiệp phương sai và tìm trị riêng `np.linalg.eigh`.
  - Công thức tính các độ đo: Silhouette Coefficient $s(i)$, Davies-Bouldin Index, Calinski-Harabasz Index, Adjusted Rand Index (ARI).
  - Chốt chữ ký hàm (*API signature*) và thống nhất cấu trúc trả về từ điển phẳng cho `evaluate_clustering`.
- [x] **Ngày 2:** Soạn thảo quyết định kiến trúc [`docs/adr/0003-mo-rong-tu-cai-dat-pca-dbscan-json.md`](../../docs/adr/0003-mo-rong-tu-cai-dat-pca-dbscan-json.md).

#### 🔹 Mốc M1: Xây dựng khung kiểm chứng thuật toán đối chứng (Ngày 3 – Ngày 7)
- [x] **Ngày 3:** Xây dựng khung script kiểm thử [`scripts/verify_scratch_implementations.py`](../../scripts/verify_scratch_implementations.py):
  - Lập assert kiểm tra bất biến quy tắc vàng: Ma trận đặc trưng $X$ tuyệt đối không chứa `happiness_score` và `happiness_rank`.
  - Viết bài test đối chứng hàm tính khoảng cách Euclid và Silhouette với `sklearn.metrics`.
- [x] **Ngày 4:** Thêm bài test đối chứng cho K-Means: So sánh hàm mục tiêu `inertia` (đảm bảo hàm tự viết đạt inertia không vượt quá `sklearn`) và tính chỉ số ARI $\ge 0.99$.
- [x] **Ngày 5:** Thêm bài test đối chứng cho Phân cấp Ward (so với `scipy.cluster.hierarchy.linkage(method='ward')`) và DBSCAN (so với `sklearn.cluster.DBSCAN`).
- [x] **Ngày 6:** Thêm bài test đối chứng cho Davies-Bouldin, Calinski-Harabasz và SimplePCA (kiểm tra phương sai giải thích và tọa độ chiếu khớp $\le 10^{-6}$).
- [x] **Ngày 7:** Rà soát chéo kết quả nạp dữ liệu interim của Trường; chuẩn bị triển khai code thuật toán from-scratch.

#### 🔹 Mốc M2: Tự cài đặt thuật toán & Độ đo From-Scratch (Ngày 8 – Ngày 14)
- [x] **Ngày 8 (Họp nhóm):** Bắt đầu triển khai lớp `SimpleKMeans` trong [`src/models/clustering.py`](../../src/models/clustering.py):
  - Khởi tạo thông minh `kmeans++`.
  - Lặp `n_init=10` lần để tránh rơi vào cực tiểu địa phương xấu.
  - Lưu lại lịch sử suy giảm `inertia_history` và số vòng lặp hội tụ `n_iter_`.
- [x] **Ngày 9:** Cài đặt lớp `SimpleHierarchicalClustering` với **tiêu chí liên kết Ward thật**:
  - Ứng dụng công thức Lance–Williams và kỹ thuật cache khoảng cách để tăng tốc độ gộp cụm.
  - Lưu lại nhật ký các bước gộp `merge_history` để phục vụ vẽ cây Dendrogram.
- [x] **Ngày 10:** Cài đặt lớp `SimpleDBSCAN`:
  - Tìm láng giềng bán kính $\epsilon$ bằng ma trận khoảng cách Euclid.
  - Lan truyền nhãn cụm cho các điểm lõi (*core samples*); gán nhãn $-1$ cho điểm ngoại lai nhiễu.
- [x] **Ngày 11:** Viết các hàm wrapper và đánh giá mô hình:
  - Các hàm tiện ích: `run_kmeans`, `run_hierarchical`, `run_dbscan`.
  - Hàm đánh giá toàn diện `evaluate_clustering`: trả về từ điển phẳng gồm 7 khóa (`silhouette`, `davies_bouldin`, `calinski_harabasz`, `inertia`, `n_clusters`, `n_noise`, `sizes`).
- [x] **Ngày 12:** Hoàn thiện các hàm tính toán độ đo độc lập:
  - `calculate_silhouette_score_simple`, `calculate_davies_bouldin_score_simple`, `calculate_calinski_harabasz_score_simple`, `calculate_adjusted_rand_index`.
- [x] **Ngày 13:** Cài đặt lớp `SimplePCA` trong [`src/features/feature_engineering.py`](../../src/features/feature_engineering.py) (chuẩn hóa dữ liệu ➔ tính ma trận hiệp phương sai ➔ giải bài toán trị riêng với `np.linalg.eigh` ➔ sắp xếp vector riêng và chiếu dữ liệu); chạy script kiểm thử đối chứng đạt **PASS 20/20 hạng mục**.
- [x] **Ngày 14:** Cài đặt cơ chế lưu và nạp mô hình dưới dạng JSON: `save_cluster_artifacts` và `load_cluster_artifacts`; tổ chức buổi **Walkthrough 20 phút** trình bày mã nguồn thuật toán cho Trường và Trung.

#### 🔹 Mốc M3: Thực thi ma trận thực nghiệm 5 năm × 5 cấu hình (Ngày 15 – Ngày 21)
- [ ] **Ngày 15 (Họp nhóm):** Xây dựng [`notebooks/03_clustering_experiments_and_comparison.ipynb`](../../notebooks/03_clustering_experiments_and_comparison.ipynb):
  - Viết vòng lặp quét qua 5 năm độc lập (2015–2019).
  - Khảo sát Elbow (Inertia) và Silhouette với $k \in [2, 9]$ cho từng năm ➔ xuất file [`reports/tables/k_sensitivity_by_year.csv`](../../reports/tables/k_sensitivity_by_year.csv).
  - Xác định số cụm tối ưu $k^*$ của mỗi năm.
- [ ] **Ngày 16:** Chạy ma trận 5 cấu hình gom cụm lõi qua 5 năm (K-Means Z-score, K-Means Min-Max, K-Means Raw, Ward Z-score, DBSCAN Z-score) ➔ xuất file [`reports/tables/model_comparison_metrics_by_year.csv`](../../reports/tables/model_comparison_metrics_by_year.csv).
- [ ] **Ngày 17:** Thực hiện quét siêu tham số DBSCAN toàn diện (4 giá trị $\epsilon \in \{0.6, 0.8, 1.0, 1.2\}$ kết hợp 3 giá trị `min_samples` $\in \{3, 4, 5\}$ cho cả 5 năm) ➔ xuất file [`reports/tables/dbscan_sweep.csv`](../../reports/tables/dbscan_sweep.csv).
- [ ] **Ngày 18:** Đánh giá độ ổn định cụm (*Cluster Stability*):
  - Chạy K-Means trên 10 seed ngẫu nhiên khác nhau, tính giá trị ARI trung bình giữa các lần chạy.
  - Ghi nhận ARI = 1.0 cho Phân cấp Ward và DBSCAN kèm lý giải toán học về tính tất định ➔ xuất file [`reports/tables/stability_ari.csv`](../../reports/tables/stability_ari.csv).
- [ ] **Ngày 19:** Thực hiện cấu hình đối chứng $k=3$ cho cả 5 năm ➔ xuất file [`reports/tables/contrast_k3_by_year.csv`](../../reports/tables/contrast_k3_by_year.csv) và các tệp gán nhãn `contrast_k3_*.csv`.
- [ ] **Ngày 20:** Xuất toàn bộ tệp mô hình JSON vào thư mục [`models/`](../../models) (gồm 10 tệp `kmeans_*.json` và `hierarchical_*.json`).
- [ ] **Ngày 21:** Soạn thảo bản nháp Mục 5, 6, 7 trong báo cáo dựa trên số liệu bảng CSV; tham gia rà soát chéo Mốc M3.

#### 🔹 Mốc M4: Soạn thảo Mục 5–7 Báo cáo Word & Kiểm chứng Demo (Ngày 22 – Ngày 26)
- [ ] **Ngày 22 (Họp nhóm):** Rà soát export toàn bộ hàm API trong `src/models/__init__.py`.
- [ ] **Ngày 23:** Kiểm chứng ứng dụng Demo Streamlit của Trung để bảo đảm app gọi đúng các hàm from-scratch trong `src/models/` và không gọi thư viện ngoài.
- [ ] **Ngày 24:** Hoàn thiện nội dung Mục 5, 6, 7 trong file [`reports/final_report/bao_cao.md`](./bao_cao.md).
- [ ] **Ngày 25:** Kiểm tra tính ăn khớp giữa số liệu viết trong báo cáo với các file CSV xuất ra.
- [ ] **Ngày 26:** Ký xác nhận hoàn thành biên tập Mục 5–7 theo checklist phân công.

#### 🔹 Mốc M5: Tổng duyệt, Rehearsal & Vấn đáp (Ngày 27 – Ngày 28)
- [ ] **Ngày 27:** Tham gia buổi tổng duyệt, chuẩn bị trả lời các câu hỏi kỹ thuật về công thức toán học và tối ưu thuật toán.
- [ ] **Ngày 28:**
  - **Rehearsal đổi vai:** Đảm nhiệm thuyết trình phần **Ứng dụng Demo Streamlit** (thay cho Trung).
  - Trình bày phần Phương pháp, Tham số và Đánh giá mô hình trước hội đồng chấm đồ án.

---

### 📦 SẢN PHẨM BÀN GIAO CỤ THỂ (DELIVERABLES)
1. **Mã nguồn thuật toán & Giảm chiều:** [`src/models/clustering.py`](../../src/models/clustering.py) và [`src/features/feature_engineering.py`](../../src/features/feature_engineering.py) (phần SimplePCA).
2. **Bộ kiểm thử đối chứng:** [`scripts/verify_scratch_implementations.py`](../../scripts/verify_scratch_implementations.py) (với 20 bài test tự động).
3. **Notebook thực nghiệm:** [`notebooks/03_clustering_experiments_and_comparison.ipynb`](../../notebooks/03_clustering_experiments_and_comparison.ipynb) (chạy sạch, đầy đủ phân tích 5 năm).
4. **Tệp mô hình lưu trữ:** 10 tệp JSON trong thư mục [`models/`](../../models).
5. **Các bảng số liệu thực nghiệm CSV trong `reports/tables/`:**
   - `k_sensitivity_by_year.csv`
   - `model_comparison_metrics_by_year.csv`
   - `dbscan_sweep.csv`
   - `stability_ari.csv`
   - `contrast_k3_by_year.csv`
6. **Văn bản báo cáo Word:** Phụ trách trọn vẹn Mục 5, 6, 7 trong báo cáo tổng kết.

---

### 🎓 CHUẨN BỊ BẢO VỆ & VẤN ĐÁP CÁ NHÂN

#### 1. Câu hỏi trọng tâm phần phụ trách chính:
- **Câu hỏi 1:** Tại sao nhóm lại tự cài đặt thuật toán mà không dùng hàm có sẵn của `scikit-learn`?
  *Trả lời:* Đề tài phục vụ mục tiêu học tập và làm chủ giải thuật. Việc tự viết từ đầu (*from-scratch*) giúp hiểu sâu bản chất toán học của các thuật toán (K-Means++, Lance–Williams, lan truyền mật độ DBSCAN) và chứng minh năng lực lập trình thuật toán trước hội đồng.
- **Câu hỏi 2:** Công thức Lance–Williams hoạt động như thế nào trong phân cấp liên kết Ward?
  *Trả lời:* Khi gộp hai cụm $A$ và $B$ thành cụm $A \cup B$, khoảng cách giữa cụm mới này tới một cụm thứ ba $C$ được tính theo hệ thức:
  $$D(A \cup B, C) = \frac{n_A + n_C}{n_A + n_B + n_C} D(A, C) + \frac{n_B + n_C}{n_A + n_B + n_C} D(B, C) - \frac{n_C}{n_A + n_B + n_C} D(A, B)$$
  Công thức này giúp tính khoảng cách mà không cần phải duyệt lại toàn bộ các điểm dữ liệu thô, giảm chi phí tính toán đáng kể.
- **Câu hỏi 3:** Tại sao thuật toán DBSCAN lại cho kết quả kém trên bộ dữ liệu World Happiness Report?
  *Trả lời:* Dữ liệu báo cáo hạnh phúc có mật độ phân bố tương đối đều trên không gian đa chiều, không có các "thung lũng mật độ thấp" rõ rệt. Khi quét các giá trị $\epsilon$ khác nhau, DBSCAN dễ rơi vào tình trạng gom toàn bộ vào 1 cụm duy nhất hoặc coi phần lớn các điểm là nhiễu (noise $-1$).

#### 2. Chuẩn bị Rehearsal đổi vai (Thuyết trình phần Demo của Trung):
- Nắm vững cấu trúc 4 tab của ứng dụng Streamlit: Tab 1 (Radar chart), Tab 2 (Bản đồ ISO-3), Tab 3 (Tra cứu quốc gia & Dịch chuyển cụm), Tab 4 (What-if analysis gán quốc gia mới).
- Trình bày được cách thức app nạp trọng tâm cụm từ file JSON và gán nhãn cho một vector 6 đặc trưng mới dựa trên khoảng cách Euclidean tối thiểu.
