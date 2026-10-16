# BẢN PHÂN TÍCH NHIỆM VỤ CÁ NHÂN — NGÔ QUANG TRUNG
## Đề tài 16: Phân nhóm quốc gia theo các yếu tố hạnh phúc (World Happiness Report)

---

### 👤 THÔNG TIN THÀNH VIÊN
- **Họ và tên:** Ngô Quang Trung
- **Mã số sinh viên:** 2045240325
- **Vai trò trong nhóm:** Thành viên
- **Tỷ lệ đóng góp cam kết:** **33%**
- **Trách nhiệm chính:** Phân tích Khám phá dữ liệu (EDA), Diễn giải tri thức kinh tế - xã hội, Thuật toán ghép cụm liên năm & Bảng dịch chuyển cụm 156 quốc gia qua 5 năm, Ứng dụng Demo Streamlit 4 tab, Thiết kế Slide thuyết trình, Viết Mục 8–11 báo cáo.
- **Trách nhiệm hỗ trợ:** Rà soát notebook 01 của Trường, kiểm tra chất lượng dữ liệu theo năm, kiểm tra bảng mã ISO-3 vẽ bản đồ, điều hành buổi tổng duyệt rehearsal.

---

### 🎯 MỤC TIÊU & PHẠM VI PHỤ TRÁCH THEO ĐỀ CƯƠNG
Phụ trách chính **Giai đoạn 3, 5, 9, 10, 11** của quy trình khai phá dữ liệu:
1. **Mục 3 — Đánh giá chất lượng dữ liệu:** Kiểm tra phân bố dữ liệu theo năm, phát hiện ngoại lai, nghiên cứu phương pháp luận Cantril Ladder và thang đo Dystopia.
2. **Mục 5 — Phân tích khám phá dữ liệu (EDA):** Phân tích hình thái phân phối (skewness), tính đa cộng tuyến và tương quan giữa các đặc trưng; đề xuất phương pháp chuẩn hóa.
3. **Mục 9 — Diễn giải kết quả gom cụm & Khám phá tri thức:** Xây dựng chân dung cụm (*Cluster Profile*), đặt tên có ý nghĩa kinh tế - xã hội, đối chiếu hậu kiểm với điểm hạnh phúc thực tế (`happiness_score`), thực hiện ghép cụm liên năm và theo dõi xu hướng dịch chuyển của 156 quốc gia.
4. **Mục 10 — Ứng dụng Demo tương tác:** Phát triển hoàn chỉnh công cụ demo Streamlit 4 tab cho người dùng trải nghiệm.
5. **Mục 11 — Kết luận và Hạn chế:** Đánh giá ưu nhược điểm của các giải thuật, nêu rõ các hạn chế khách quan của bộ dữ liệu và định hướng mở rộng.

---

### 📅 KẾ HOẠCH CHI TIẾT THEO 5 MỐC THỜI GIAN (28 NGÀY)

#### 🔹 Mốc M0: Thiết kế giao diện & Danh mục trực quan hóa (Ngày 1 – Ngày 2)
- [x] **Ngày 1 (Họp nhóm):** 
  - Lên danh mục cố định 12 hình vẽ trực quan hóa chất lượng cao (300 DPI) cho báo cáo Word.
  - Phác thảo cấu trúc và layout 4 tab của ứng dụng Demo Streamlit.
- [x] **Ngày 2:** Liệt kê các câu hỏi kỹ thuật và nghiệp vụ cần trả lời ở phần thảo luận và kết luận; đóng góp vào kế hoạch thực thi 28 ngày.

#### 🔹 Mốc M1: Đánh giá chất lượng dữ liệu & Nghiên cứu bối cảnh (Ngày 3 – Ngày 7)
- [x] **Ngày 3:** Lập bảng đánh giá chất lượng dữ liệu 5 năm (tỷ lệ missing, trùng lặp, cỡ mẫu từng năm: 158/157/155/156/156).
- [x] **Ngày 4:** Nghiên cứu và tổng hợp tài liệu phương pháp luận: Thang đo Cantril Ladder (0 đến 10), khái niệm quốc gia giả định Dystopia và 6 yếu tố giải thích.
- [x] **Ngày 5:** Kiểm tra và chuẩn hóa bảng mã quốc gia 3 ký tự (ISO-3) để đảm bảo vẽ bản đồ thế giới Choropleth không bị khuyết màu.
- [x] **Ngày 6:** Ghi nhận lý do loại trừ dữ liệu UAE 2018 và xác nhận cỡ mẫu từng năm vào tài liệu.
- [x] **Ngày 7:** Soạn thảo bản nháp bộ 20 câu hỏi vấn đáp cho 3 thành viên; tham gia buổi Walkthrough của Trường.

#### 🔹 Mốc M2: Xây dựng biểu đồ trực quan & Phân tích EDA (Ngày 8 – Ngày 14)
- [x] **Ngày 8 (Họp nhóm):** Hoàn thiện các hàm vẽ biểu đồ trong [`src/visualization/plots.py`](../../src/visualization/plots.py):
  - `plot_feature_distributions` (Histogram + đường cong KDE).
  - `plot_correlation_heatmap` (Ma trận tương quan Pearson).
  - `plot_outliers_boxplot` (Biểu đồ hộp phát hiện ngoại lai).
  - `plot_clusters_2d` (Không gian PCA 2D).
  - `plot_cluster_radar` (Radar chart đa giác 6 yếu tố).
  - `plot_dendrogram` (Cây phân cấp).
  - `plot_happiness_score_by_cluster` (Boxplot hậu kiểm điểm hạnh phúc).
- [x] **Ngày 9:** Thực hiện [`notebooks/02_exploratory_data_analysis.ipynb`](../../notebooks/02_exploratory_data_analysis.ipynb):
  - Tính toán độ lệch skewness và nhận xét phân bố từng đặc trưng.
  - Phân tích tương quan: Chỉ ra mối quan hệ rất mạnh giữa GDP, Tuổi thọ và Hỗ trợ xã hội ($r > 0.7$).
- [x] **Ngày 10:** Phát hiện các quốc gia có giá trị ngoại lai dị biệt (ví dụ: điểm tham nhũng cao đột biến ở một số nước phát triển, điểm hỗ trợ xã hội rất thấp ở một số nước châu Phi).
- [x] **Ngày 11:** Phân tích thực nghiệm so sánh Z-score và Min-Max, đưa ra luận điểm thuyết phục vì sao chọn Z-score làm cấu hình chính của đề tài.
- [x] **Ngày 12:** Xuất các hình ảnh phân tích EDA độ phân giải cao vào [`reports/figures/`](../../reports/figures):
  - `feature_distributions.png`
  - `correlation_heatmap.png`
  - `boxplots_outliers.png`
- [x] **Ngày 13:** Kiểm tra thời gian chạy của các hàm vẽ biểu đồ; đảm bảo hình vẽ hiển thị nhãn tiếng Việt rõ ràng, có thước đo độ phân giải.
- [x] **Ngày 14:** Tham gia buổi Walkthrough module thuật toán của Trí.

#### 🔹 Mốc M3: Diễn giải tri thức, Ghép cụm liên năm & Bảng dịch chuyển (Ngày 15 – Ngày 21)
- [x] **Ngày 15 (Họp nhóm):** Khởi tạo khung phân tích cho [`notebooks/04_cluster_profiling_and_evaluation.ipynb`](../../notebooks/04_cluster_profiling_and_evaluation.ipynb).
- [x] **Ngày 16:** 
  - Thực hiện giảm chiều dữ liệu bằng SimplePCA xuống 2D trên cả 5 năm.
  - Vẽ lưới biểu đồ phân bố cụm 5 năm: `reports/figures/pca_clusters_grid.png`.
- [x] **Ngày 17:** 
  - **Xây dựng chân dung cụm (*Cluster Profiling*):** Tính giá trị trung bình 6 yếu tố cho từng nhóm, vẽ biểu đồ Radar Chart cho các năm.
  - Đặt tên có ý nghĩa kinh tế - xã hội cho các cụm (ví dụ: *Cụm 1 — Phát triển toàn diện*, *Cụm 2 — Đang phát triển phụ thuộc kinh tế*, *Cụm 3 — Dễ bị tổn thương & Khó khăn*).
- [x] **Ngày 18:** 
  - **Hậu kiểm độc lập (*Post-clustering Validation*):** Đối chiếu nhãn cụm với điểm hạnh phúc thực tế (`happiness_score`).
  - Vẽ biểu đồ boxplot phân bố điểm hạnh phúc giữa các cụm (`validation_happiness_score_by_cluster.png`), chứng minh các cụm có sự phân hóa điểm sống thực tế sâu sắc.
- [x] **Ngày 19:** 
  - **Thuật toán ghép cụm liên năm (`match_clusters_greedy`):** Ghép cặp cụm giữa năm $t$ và năm $t-1$ theo khoảng cách tâm cụm nhỏ nhất; nếu khoảng cách bằng nhau thì xét điểm hạnh phúc trung bình.
  - Xuất bảng ghép cụm liên năm: `reports/tables/cross_year_matching.csv`.
- [x] **Ngày 20:** 
  - **Xây dựng bảng dịch chuyển cụm của 156 quốc gia qua 5 năm:** Theo dõi quốc gia nào tăng nhóm, quốc gia nào tụt nhóm hoặc giữ nguyên ổn định ➔ xuất file [`data/processed/country_cluster_shift.csv`](../../data/processed).
  - Vẽ biểu đồ xu hướng số lượng quốc gia theo từng cụm qua thời gian: `reports/figures/cluster_count_trend.png` và xuất `cluster_trends.csv`.
- [x] **Ngày 21:** Tổ chức buổi **Walkthrough 20 phút** trình bày kết quả Diễn giải tri thức và bảng dịch chuyển cho Trường và Trí; hoàn thành Mục 8, 9, 10, 11 của báo cáo.

#### 🔹 Mốc M4: Hoàn thiện Ứng dụng Demo Streamlit & Thiết kế Slide (Ngày 22 – Ngày 26)
- [ ] **Ngày 22 (Họp nhóm):** Thiết kế nâng cấp ứng dụng tương tác [`app/app.py`](../../app/app.py).
- [ ] **Ngày 23:** Hoàn thiện 4 tab tương tác của ứng dụng Demo Streamlit:
  - **Tab 1 — Tổng quan cụm & Radar Chart:** Cho phép tùy chọn năm (2015–2019), thuật toán (K-Means, Ward), hiển thị Radar chart động và bảng chỉ số đánh giá.
  - **Tab 2 — Bản đồ thế giới (Choropleth Map):** Trực quan hóa màu sắc các cụm lên bản đồ tương tác thế giới sử dụng mã ISO-3.
  - **Tab 3 — Tra cứu quốc gia & Dịch chuyển cụm:** Ô tìm kiếm tên quốc gia (Việt Nam, Na Uy, v.v.) hiển thị biểu đồ diễn biến 6 chỉ số và lịch sử chuyển nhóm qua 5 năm.
  - **Tab 4 — Thử nghiệm gán nhãn cho quốc gia mới (*What-if Analysis*):** Cho phép người dùng kéo thanh trượt 6 đặc trưng giả định để hệ thống tính khoảng cách Euclidean và gán cụm tức thì.
- [ ] **Ngày 24:** Tối ưu hóa hiệu năng ứng dụng bằng `@st.cache_data`, kiểm tra ứng dụng chạy mượt mà offline.
- [ ] **Ngày 25:** Thiết kế bộ slide thuyết trình chuẩn đề tài (12–15 slide cô đọng, trình bày trong 8–10 phút).
- [ ] **Ngày 26:** Ký xác nhận hoàn thành biên tập Mục 8–11 trong checklist báo cáo.

#### 🔹 Mốc M5: Tổng duyệt, Rehearsal & Vấn đáp (Ngày 27 – Ngày 28)
- [ ] **Ngày 27:** Điều hành buổi diễn tập tổng duyệt của cả nhóm, bấm giờ thuyết trình và đặt các câu hỏi phản biện giả lập.
- [ ] **Ngày 28:**
  - **Rehearsal đổi vai:** Thuyết trình thử phần **Thu thập và Tiền xử lý dữ liệu** (thay cho Trường).
  - Trình bày phần Diễn giải tri thức, Demo tương tác và Kết luận trước hội đồng chấm đồ án.

---

### 📦 SẢN PHẨM BÀN GIAO CỤ THỂ (DELIVERABLES)
1. **Module trực quan hóa:** [`src/visualization/plots.py`](../../src/visualization/plots.py) (đầy đủ các hàm vẽ 300 DPI).
2. **Notebooks phân tích:**
   - [`notebooks/02_exploratory_data_analysis.ipynb`](../../notebooks/02_exploratory_data_analysis.ipynb)
   - [`notebooks/04_cluster_profiling_and_evaluation.ipynb`](../../notebooks/04_cluster_profiling_and_evaluation.ipynb)
3. **Ứng dụng Demo tương tác:** [`app/app.py`](../../app/app.py) (4 tab tương tác hoàn chỉnh).
4. **Dữ liệu phân tích dịch chuyển:** [`data/processed/country_cluster_shift.csv`](../../data/processed) (bảng 156 quốc gia × 5 năm) và `cluster_trends.csv`.
5. **Bộ hình ảnh báo cáo:** 12 tệp hình ảnh đạt chuẩn 300 DPI trong thư mục [`reports/figures/`](../../reports/figures).
6. **Slide thuyết trình & Báo cáo:** Bài thuyết trình PowerPoint và nội dung Mục 8, 9, 10, 11 trong báo cáo tổng kết.

---

### 🎓 CHUẨN BỊ BẢO VỆ & VẤN ĐÁP CÁ NHÂN

#### 1. Câu hỏi trọng tâm phần phụ trách chính:
- **Câu hỏi 1:** Bức chân dung (*Profile*) của các cụm được định nghĩa như thế nào và có ý nghĩa gì?
  *Trả lời:* Dựa trên giá trị trung bình của 6 yếu tố sau khi gom cụm:
  - *Cụm Phát triển toàn diện:* Vượt trội về kinh tế (GDP), Tuổi thọ cao, Hỗ trợ xã hội mạnh và Nhận thức tham nhũng rất cao (tham nhũng thấp). Điểm hạnh phúc trung bình thực tế > 7.0.
  - *Cụm Đang phát triển:* Kinh tế và tuổi thọ ở mức khá/trung bình, tự do cá nhân khá, nhưng niềm tin vào sự liêm chính còn hạn chế. Điểm hạnh phúc trung bình ~ 5.2 - 5.8.
  - *Cụm Dễ tổn thương:* Kinh tế thấp, tuổi thọ ngắn, hỗ trợ xã hội yếu kém. Điểm hạnh phúc trung bình < 4.5.
- **Câu hỏi 2:** Thuật toán ghép cụm liên năm hoạt động ra sao khi các năm được chạy gom cụm độc lập?
  *Trả lời:* Nhóm sử dụng thuật toán ghép tham lam (*Greedy Matching*): Đo khoảng cách Euclidean giữa các vector trọng tâm cụm của năm sau và năm trước (đã chuẩn hóa). Cặp cụm có khoảng cách nhỏ nhất được ghép với nhau. Nếu có trường hợp khoảng cách hòa thì dùng điểm hạnh phúc trung bình làm tiêu chí phân định.
- **Câu hỏi 3:** Tại sao lại cần bước hậu kiểm (*Post-clustering Validation*) với điểm hạnh phúc?
  *Trả lời:* Vì theo Quy tắc vàng, biến `happiness_score` không tham gia vào quá trình gom cụm. Việc hậu kiểm bằng biểu đồ boxplot và kiểm định thống kê giúp chứng minh khách quan rằng các cụm được hình thành từ 6 yếu tố cơ sở hoàn toàn phản ánh đúng mức độ hạnh phúc thực tế của người dân.

#### 2. Chuẩn bị Rehearsal đổi vai (Thuyết trình phần Tiền xử lý của Trường):
- Nắm vững cấu trúc 5 tệp dữ liệu thô (2015–2019) và các trường hợp lệch tên cột.
- Giải thích được tại sao nhóm lựa chọn loại bỏ dòng dữ liệu UAE năm 2018 (do thiếu hoàn toàn chỉ số tham nhũng).
- Trình bày được quy trình xuất bảng trung gian `happiness_merged.csv` với 783 dòng dữ liệu sạch.
