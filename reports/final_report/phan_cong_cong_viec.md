# Bảng phân công công việc — Nhóm 12 — Đề tài 16

Bảng dưới đây là phần dùng cho báo cáo: nêu phần việc chính, phần việc hỗ trợ và tỷ lệ đóng góp của từng
thành viên. Tỷ lệ đóng góp cộng lại bằng 100%.

| Thành viên | Công việc chính | Công việc hỗ trợ | Tỷ lệ đóng góp (%) |
|:--|:--|:--|:--:|
| Hà Mạnh Trường (2045240326, nhóm trưởng) | Thu thập và tiền xử lý dữ liệu 5 năm; dựng bảng dữ liệu trung gian; kiểm soát khả năng chạy lại của mã nguồn; điều phối tiến độ và ghép báo cáo; viết Chương 1, Chương 2 | Rà soát phần thuật toán gom cụm; đối chiếu số liệu giữa các năm; hỗ trợ nạp dữ liệu cho demo | 34 |
| Huỳnh Tâm Trí (2045240315) | Tự cài đặt thuật toán gom cụm (K-Means, phân cấp Ward, DBSCAN), giảm chiều PCA và các độ đo đánh giá; chạy thực nghiệm 5 cấu hình × 5 năm; khảo sát tham số; viết Chương 3 và phần thực nghiệm Chương 4 | Rà soát bộ nạp dữ liệu; kiểm chứng các độ đo bằng thư viện; rà soát phần nối dữ liệu của demo | 33 |
| Ngô Quang Trung (2045240325) | Phân tích khám phá dữ liệu; diễn giải kết quả gom cụm; ghép cụm giữa các năm và lập bảng dịch chuyển cụm; xây dựng demo Streamlit; làm slide; viết phần diễn giải Chương 4 và Chương 5 | Rà soát notebook 01; kiểm tra chất lượng dữ liệu theo năm; kiểm tra bản đồ; điều hành buổi tổng duyệt | 33 |

---

## Phần nội bộ của nhóm (không đưa vào báo cáo)

### Phân chia theo giai đoạn phân tích

| Giai đoạn | Nội dung | Chính | Hỗ trợ | Nơi thể hiện |
|:--|:--|:--|:--|:--|
| 1 | Xác định bài toán và câu hỏi khai thác | Trường | cả nhóm | `notebooks/01` mục 1, `README.md` |
| 2 | Tìm hiểu dữ liệu (5 năm, schema lệch) | Trường | Trung | `notebooks/01` mục 2, `src/data/data_loader.py` |
| 3 | Đánh giá chất lượng dữ liệu theo từng năm | Trung | Trường | `notebooks/01` mục 3 |
| 4 | Tiền xử lý, chuẩn hóa tên cột và tên quốc gia, dựng bảng trung gian | Trường | Trí | `notebooks/01`, `data/interim/` |
| 5 | Phân tích khám phá dữ liệu | Trung | Trí | `notebooks/02`, `reports/figures/` |
| 6 | Biến đổi dữ liệu cho thuật toán (Z-score, Min-Max, không chuẩn hóa) | Trí | Trường | `src/features/feature_engineering.py`, `notebooks/03` |
| 7 | Chạy thuật toán và chọn tham số (số cụm tối ưu mỗi năm, cấu hình ba cụm đối chứng, quét DBSCAN) | Trí | Trung | `notebooks/03`, `reports/tables/k_sensitivity_by_year.csv` |
| 8 | So sánh các cấu hình gom cụm và đo độ ổn định | Trí | Trường | `notebooks/03`, `reports/tables/model_comparison_metrics_by_year.csv` |
| 9 | Diễn giải kết quả: chân dung cụm, ghép cụm liên năm, bảng dịch chuyển cụm, hậu kiểm điểm hạnh phúc | Trung | Trí | `notebooks/04`, `data/processed/country_cluster_shift.csv` |
| 10 | Sản phẩm demo (chọn năm, thuật toán, cách chuẩn hóa, số cụm) | Trung | Trường | `app/app.py` |
| 11 | Kết luận và hướng phát triển | Trung | cả nhóm | `notebooks/04` mục 3, Chương 5 của báo cáo |

### Yêu cầu chung của nhóm & Phân chia Video Thuyết trình ($\le$ 12 phút)

- **Kịch bản phân chia thời lượng video báo cáo ($\le$ 12 phút, cả 3 thành viên tham gia):**
  - **Phần 1 — Hà Mạnh Trường (00:00 – 04:00, ~4 phút):** Giới thiệu bài toán phân nhóm quốc gia WHR, cấu trúc dữ liệu 5 năm và giải thích các quyết định tiền xử lý quan trọng (loại UAE 2018, chuẩn hóa 6 thuộc tính không chứa Happiness Score).
  - **Phần 2 — Huỳnh Tâm Trí (04:00 – 08:00, ~4 phút):** Trình bày phương pháp gom cụm from-scratch (K-Means, Ward, DBSCAN), quy trình tối ưu tham số ($k^*$, $eps$) và so sánh định lượng các cấu hình qua hệ số Silhouette, Davies-Bouldin.
  - **Phần 3 — Ngô Quang Trung (08:00 – 12:00, ~4 phút):** Diễn giải chân dung cụm tiêu biểu, dịch chuyển cụm liên năm 156 quốc gia, minh họa chạy demo ứng dụng Streamlit trực tiếp và tổng kết hạn chế của đề tài.
- Mỗi thành viên nắm toàn bộ quy trình phân tích, không chỉ phần việc cá nhân: sau mỗi phần việc hoàn thành, người thực hiện trình bày lại 20 phút cho hai thành viên còn lại và ghi biên bản vào `ke_hoach_nhom.md`.
- Trước buổi báo cáo, cả nhóm tổng duyệt và đổi vai: Trường trình bày phần phương pháp, Trí trình bày phần demo, Trung trình bày phần tiền xử lý dữ liệu.
- Mỗi thành viên phải chạy được cả bốn notebook, giải thích được công thức Silhouette, chân dung một cụm của một năm bất kỳ và một đoạn mã bất kỳ trong `src/models/clustering.py`.

### Checklist ký xác nhận nội dung báo cáo & Truy vết số liệu

Mọi con số trong Báo cáo Word phải truy được về `reports/tables/*.csv` hoặc `reports/figures/*`. Báo cáo phải tuân thủ nghiêm ngặt chuẩn **Anti-AI Writing Style** (không dùng văn phong sáo rỗng, đối xứng nhân tạo). Trước khi nộp, mỗi thành viên đọc lại phần mình phụ trách và ký xác nhận.

| Mục báo cáo | Người biên tập | Đã đọc | Đã đối chiếu số với CSV | Không văn phong AI | Ngày ký |
|:--|:--|:--:|:--:|:--:|:--|
| Chương 1 & 2 (Tổng quan bài toán, dữ liệu, tiền xử lý) | Trường | ☐ | ☐ | ☐ | |
| Chương 3 & phần thực nghiệm Chương 4 (Phương pháp from-scratch, tham số, kết quả) | Trí | ☐ | ☐ | ☐ | |
| Phần diễn giải Chương 4 & Chương 5 (Diễn giải tri thức, kết luận, hạn chế) | Trung | ☐ | ☐ | ☐ | |
| Slide thuyết trình & Video $\le$ 12 phút | cả nhóm | ☐ | ☐ | ☐ | |
