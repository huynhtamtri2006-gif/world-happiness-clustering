# BẢN PHÂN TÍCH NHIỆM VỤ CÁ NHÂN — HÀ MẠNH TRƯỜNG
## Đề tài 16: Phân nhóm quốc gia theo các yếu tố hạnh phúc (World Happiness Report)

---

### 👤 THÔNG TIN THÀNH VIÊN
- **Họ và tên:** Hà Mạnh Trường
- **Mã số sinh viên:** 2045240326
- **Vai trò trong nhóm:** Nhóm trưởng
- **Tỷ lệ đóng góp cam kết:** **34%**
- **Trách nhiệm chính:** Quản lý dự án, Kỹ thuật dữ liệu 5 năm (Data Engineering), Kiểm soát tính tái lập (Reproducibility), Ghép và tự động hóa báo cáo Word.
- **Trách nhiệm hỗ trợ:** Rà soát logic gom cụm của Trí, đối chiếu số liệu giữa 5 năm, hỗ trợ nạp dữ liệu cho Demo của Trung.

---

### 🎯 MỤC TIÊU & PHẠM VI PHỤ TRÁCH THEO ĐỀ CƯƠNG
Phụ trách chính **Giai đoạn 1, 2, 4** và chủ trì việc ghép báo cáo:
1. **Mục 1 — Xác định bài toán:** Bối cảnh World Happiness Report, 4 câu hỏi khai thác dữ liệu, ranh giới bất biến (không đưa điểm/thứ hạng hạnh phúc vào gom cụm).
2. **Mục 2 — Tìm hiểu dữ liệu:** Phân tích cấu trúc 5 năm (2015–2019) với schema không đồng nhất, ý nghĩa 6 biến cơ sở.
3. **Mục 4 — Tiền xử lý dữ liệu:** Chuẩn hóa tên cột, xử lý thiếu dữ liệu (loại UAE 2018), đồng bộ tên quốc gia qua 5 năm, loại bỏ các cột sai số đo lường (`Standard Error`, `Whisker`).
4. **Tự động hóa báo cáo Word:** Xây dựng công cụ tạo file `.docx` tự động chuẩn Open Packaging Conventions / OOXML.

---

### 📅 KẾ HOẠCH CHI TIẾT THEO 5 MỐC THỜI GIAN (28 NGÀY)

#### 🔹 Mốc M0: Chốt kiến trúc & Thiết kế hệ thống (Ngày 1 – Ngày 2)
- [x] **Ngày 1 (Họp nhóm):** Chủ trì chốt baseline kỹ thuật: 5 năm chạy độc lập, $k^*$ tối ưu là kết quả chính, $k=3$ là đối chứng xuyên năm; ghi nhận quyết định kiến trúc [`docs/adr/0002-gom-cum-theo-nam-va-ghep-cum-lien-nam.md`](../../docs/adr/0002-gom-cum-theo-nam-va-ghep-cum-lien-nam.md); chuẩn hóa [`CONTEXT.md`](../../CONTEXT.md).
- [x] **Ngày 2:** Hoàn thiện kế hoạch thực thi 28 ngày [`ke_hoach_nhom.md`](./ke_hoach_nhom.md) và bảng phân công [`phan_cong_cong_viec.md`](./phan_cong_cong_viec.md).

#### 🔹 Mốc M1: Xây dựng nền dữ liệu 5 năm & Kiểm soát chất lượng (Ngày 3 – Ngày 7)
- [x] **Ngày 3:** Phát triển module [`src/data/data_loader.py`](../../src/data/data_loader.py):
  - Xây dựng từ điển `COLUMN_MAPPING` đồng nhất tên cột qua 5 năm.
  - Viết hàm `build_interim_dataset(years=[2015..2019])`.
  - Cài đặt cơ chế chuẩn hóa tên quốc gia `harmonize_country_names`, từ điển sửa lỗi `COUNTRY_NAME_FIXES` và bộ chuyển đổi `country_to_iso3`.
  - Định nghĩa hàm nạp `load_interim` và `load_processed`.
- [x] **Ngày 4:** Sửa đổi và hoàn thiện [`notebooks/01_data_understanding_and_cleaning.ipynb`](../../notebooks/01_data_understanding_and_cleaning.ipynb):
  - Viết mã nguồn nạp 5 file raw CSV (2015–2019).
  - Loại bỏ các cột sai số (`Standard Error`, `Whisker.high`, `Whisker.low`) kèm lập luận khoa học trong markdown.
  - Xử lý bản ghi khuyết thiếu của UAE năm 2018 (loại bỏ an toàn khỏi thực nghiệm).
  - Xuất file dữ liệu trung gian thống nhất [`data/interim/happiness_merged.csv`](../../data/interim/happiness_merged.csv) (781 dòng dữ liệu sạch).
- [x] **Ngày 5:** Quản trị môi trường và kho lưu trữ:
  - Cập nhật [`.gitignore`](../../.gitignore) bỏ chặn `README.md`.
  - Chốt phiên bản cố định trong [`requirements.txt`](../../requirements.txt).
- [x] **Ngày 6:** Viết [`README.md`](../../README.md) hoàn chỉnh: bảng phân công đóng góp 34/33/33, hướng dẫn thiết lập môi trường và lệnh chạy lại từ đầu; cập nhật [`notebooks/README.md`](../../notebooks/README.md).
- [x] **Ngày 7:** Tổ chức buổi **Walkthrough 20 phút** trình bày quy trình tiền xử lý dữ liệu và cấu trúc bảng interim cho Trí và Trung; kiểm tra notebook 01 chạy sạch từ đầu (0 cell lỗi).

#### 🔹 Mốc M2: Kiểm soát chất lượng & Tối ưu hiệu năng (Ngày 8 – Ngày 14)
- [x] **Ngày 8 (Họp nhóm):** Đánh giá nghiệm thu tiến độ M1; chốt chữ ký API với Trí trước khi triển khai thuật toán from-scratch.
- [x] **Ngày 9:** Rà soát đường dẫn tương đối trong các tệp mã nguồn và notebook để tránh lỗi môi trường.
- [x] **Ngày 10:** Hỗ trợ Trí tối ưu hóa thuật toán phân cấp Ward (mục tiêu chạy < 30 giây trên 156 mẫu).
- [x] **Ngày 11:** Viết script kiểm tra nhanh môi trường cài đặt cho demo máy chấm.
- [x] **Ngày 12:** Soát lỗi chính tả docstring tiếng Việt và công thức toán học trong [`src/models/clustering.py`](../../src/models/clustering.py).
- [x] **Ngày 13:** Chạy thử nghiệm script kiểm thử đối chứng lần 1, lưu log kết quả.
- [x] **Ngày 14:** Tham gia buổi Walkthrough module thuật toán do Trí trình bày.

#### 🔹 Mốc M3: Thẩm định tính nhất quán số liệu thực nghiệm (Ngày 15 – Ngày 21)
- [x] **Ngày 15 (Họp nhóm):** Chốt định dạng bảng biểu và cách trình bày kết quả $k^*$ chính và $k=3$ đối chứng; nghiệm thu bảng `reports/tables/contrast_k3_by_year.csv` (10 dòng đầy đủ cho K-Means và Ward).
- [x] **Ngày 16:** Kiểm tra tính hợp lý của số cụm $k^*$ giữa các năm (100% các năm $k^* \in [2, 5]$; đồng thuận $k^*=3$ toàn cục với Silhouette cực đại 0.293–0.344).
- [x] **Ngày 17:** Đối chiếu các con số trong notebook 03 với các file CSV xuất ra trong `reports/tables/` (`k_sensitivity_by_year.csv` 40 dòng, `model_comparison_metrics_by_year.csv` 25 dòng, `dbscan_sweep.csv` 60 dòng, `stability_ari.csv` 25 dòng).
- [x] **Ngày 18:** Rà soát khóa chính và tên cột giữa các bảng số liệu để bảo đảm liên kết dữ liệu không bị lỗi; xác nhận khớp 100% với 781 dòng interim.
- [x] **Ngày 19:** Kiểm tra bảng dịch chuyển cụm 156 quốc gia qua 5 năm (`data/processed/country_cluster_shift.csv`), xác nhận đủ 156 dòng, 0 trùng lặp, UAE 2018 khuyết thiếu hợp lệ.
- [x] **Ngày 20:** Kiểm tra toàn bộ 13 hình ảnh xuất ra bảo đảm đúng độ phân giải $\ge 300$ DPI phục vụ in ấn Báo cáo Word.
- [x] **Ngày 21:** Tham gia buổi Walkthrough module Diễn giải tri thức do Trung trình bày; rà soát chéo toàn bộ kết quả M3; xây dựng script kiểm toán độc lập [`scripts/audit_m3_data_consistency.py`](../../scripts/audit_m3_data_consistency.py) và lưu log tại [`logs/audit_m3_consistency.log`](../../logs/audit_m3_consistency.log).

#### 🔹 Mốc M4: Tự động hóa Báo cáo Word & Soạn thảo Mục 1–4 (Ngày 22 – Ngày 26)
- [ ] **Ngày 22 (Họp nhóm):** Chốt tiến độ M3 và phạm vi báo cáo Word.
- [ ] **Ngày 23:** Viết công cụ [`reports/final_report/build_report.py`](./build_report.py) (backend OOXML thuần Python):
  - Tạo trang bìa chuẩn đề tài môn học.
  - Tạo mục lục tự động (TOC field).
  - Tự động đọc và vẽ bảng từ `reports/tables/*.csv`.
  - Tự động nhúng và đánh số hình từ `reports/figures/*.png`.
- [ ] **Ngày 24:** Soạn thảo bản gốc markdown [`reports/final_report/bao_cao.md`](./bao_cao.md) cho Mục 1, 2, 3, 4.
- [ ] **Ngày 25:** Chạy `build_report.py`, ghép nối các phần nội dung của Trí và Trung, kiểm tra độ dài ~50 trang.
- [ ] **Ngày 26:** Rà soát toàn bộ số liệu báo cáo; ký xác nhận hoàn thành biên tập Mục 1–4.

#### 🔹 Mốc M5: Tổng duyệt, Rehearsal & Đóng gói nộp bài (Ngày 27 – Ngày 28)
- [ ] **Ngày 27:** Chạy kiểm thử toàn diện toàn bộ pipeline từ đầu trên máy sạch; kiểm tra 10 tiêu chí nộp bài của đề cương; tham gia tổng duyệt vấn đáp phần tiền xử lý.
- [ ] **Ngày 28:** 
  - **Rehearsal đổi vai:** Thuyết trình thử phần **Phương pháp gom cụm & Tham số** (thay cho Trí).
  - Quản trị Git: merge nhánh `main`, tạo tag `v1.0`, đẩy toàn bộ mã nguồn lên GitHub.
  - Nộp file báo cáo Word `.docx`, slide trình chiếu và liên kết repository.

---

### 📦 SẢN PHẨM BÀN GIAO CỤ THỂ (DELIVERABLES)
1. **Module nạp dữ liệu:** [`src/data/data_loader.py`](../../src/data/data_loader.py) (đầy đủ các hàm nạp, làm sạch, chuẩn hóa tên quốc gia 5 năm).
2. **Notebook tiền xử lý:** [`notebooks/01_data_understanding_and_cleaning.ipynb`](../../notebooks/01_data_understanding_and_cleaning.ipynb) (chạy sạch, markdown phân tích chi tiết).
3. **Bộ dữ liệu trung gian:** [`data/interim/happiness_merged.csv`](../../data/interim/happiness_merged.csv) (781 dòng sạch, 0 khuyết thiếu ở 6 đặc trưng, schema thống nhất).
4. **Tài liệu quản trị:** [`README.md`](../../README.md), [`requirements.txt`](../../requirements.txt), [`.gitignore`](../../.gitignore).
5. **Công cụ tạo báo cáo:** [`reports/final_report/build_report.py`](./build_report.py).
6. **Văn bản báo cáo Word:** Phụ trách trọn vẹn Mục 1, 2, 3, 4 trong [`Bao_cao_De_tai_16_Nhom_12.docx`](./Bao_cao_De_tai_16_Nhom_12.docx).

---

### 🎓 CHUẨN BỊ BẢO VỆ & VẤN ĐÁP CÁ NHÂN

#### 1. Câu hỏi trọng tâm phần phụ trách chính:
- **Câu hỏi 1:** Tại sao nhóm lại quyết định loại bỏ các cột như `Standard Error`, `Whisker.high`, `Whisker.low` trong quá trình tiền xử lý?
  *Trả lời:* Các cột này chỉ biểu thị sai số ước lượng thống kê của cuộc khảo sát mẫu, không phản ánh đặc tính kinh tế - xã hội của quốc gia, nếu đưa vào sẽ gây nhiễu thuật toán khoảng cách.
- **Câu hỏi 2:** Nhóm đã xử lý sự không đồng nhất về cấu trúc cột giữa các năm 2015–2019 như thế nào?
  *Trả lời:* Xây dựng từ điển `COLUMN_MAPPING` để đồng nhất tên cột (ví dụ: `Economy (GDP per Capita)` ở 2015 đổi thành `gdp_per_capita`), đồng thời chuẩn hóa tên quốc gia (`COUNTRY_NAME_FIXES`) để không bị tách dòng dữ liệu.
- **Câu hỏi 3:** Tại sao lại loại bản ghi của United Arab Emirates (UAE) trong năm 2018?
  *Trả lời:* Năm 2018, UAE bị khuyết hoàn toàn chỉ số `Perceptions of corruption`. Việc loại bỏ 1 mẫu này bảo đảm ma trận đầu vào hoàn toàn không bị giá trị NaN làm sai lệch thuật toán gom cụm.

#### 2. Chuẩn bị Rehearsal đổi vai (Thuyết trình phần Thuật toán của Trí):
- Nắm vững công thức toán của giải thuật K-Means: hàm mục tiêu Inertia (WCSS), cơ chế chọn tâm ban đầu K-Means++.
- Nắm vững nguyên lý liên kết Ward trong phân cấp tích tụ: tối thiểu hóa gia tăng phương sai nội cụm $\Delta WSS$ sau mỗi bước gộp.
- Giải thích được ý nghĩa toán học của hệ số Silhouette $s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$.
