# Bộ 20 câu hỏi – đáp vấn đáp bảo vệ đồ án

- **Học phần:** Khai thác dữ liệu — **Đề tài 16:** Phân nhóm quốc gia theo các yếu tố hạnh phúc (World Happiness Report)
- **Nhóm 12:** Hà Mạnh Trường (2045240326) — Huỳnh Tâm Trí (2045240315) — Ngô Quang Trung (2045240325)
- **Người tổng hợp:** Ngô Quang Trung — Mốc M1 (Ngày 7), bản nháp; cả nhóm rà soát và cập nhật sau buổi tổng duyệt Ngày 28.

> **Quy ước số liệu:** Mọi con số trong tài liệu này lấy từ `reports/tables/*.csv`, `data/processed/country_cluster_shift.csv` và mã nguồn trong `src/`; khớp với kết quả chạy trong `notebooks/03`, `notebooks/04`. Khi trả lời trước hội đồng, chỉ nêu số liệu truy được về các tệp này.

---

## PHẦN 1 — BỐI CẢNH, MỤC TIÊU & HIỂU DỮ LIỆU (Câu 1 – 4)

### Câu 1. World Happiness Report là gì, dữ liệu nhóm dùng có nguồn gốc thế nào?

WHR là báo cáo thường niên về mức sống hạnh phúc của các quốc gia, công bố từ năm 2012 dưới sự chủ trì của Mạng lưới Giải pháp Phát triển Bền vững Liên Hợp Quốc; các bản 2015–2019 là phạm vi nhóm khai thác. Điểm số và xếp hạng được xây dựng từ khảo sát Gallup World Poll: mỗi quốc gia lấy mẫu đại diện khoảng 1.000 người trưởng thành, dùng trọng số Gallup, chấm trên thang Cantril Ladder từ 0 đến 10. Nhóm dùng bản tổng hợp 5 tệp CSV (2015–2019) đăng trên Kaggle, tổng 782 dòng thô, sau làm sạch còn 781 dòng.

Đây là bài toán gom cụm vì dữ liệu không có nhãn mục tiêu cho bài toán phân lớp; `happiness_score` tồn tại nhưng bị quy tắc vàng cấm dùng làm đặc trưng, nên chỉ còn cách phân nhóm dựa trên 6 yếu tố cơ sở rồi hậu kiểm bằng điểm hạnh phúc.

### Câu 2. Sáu yếu tố cơ sở có ý nghĩa gì và vì sao chọn đúng 6 biến này?

Sáu yếu tố là: `gdp_per_capita` (log GDP bình quân đầu người theo PPP), `social_support` (có người thân/bạn bè để dựa vào khi khó khăn — cột `Family` các năm 2015–2017), `healthy_life_expectancy` (số năm sống khỏe mạnh kỳ vọng theo WHO), `freedom` (tự do lựa chọn cuộc sống), `generosity` (mức quyên góp từ thiện đã trừ phần dự báo bởi GDP) và `corruption_perception` (niềm tin vào sự liêm chính của chính phủ, doanh nghiệp — điểm càng cao thì tham nhũng càng ít).

Cả 6 biến là thang đo liên tục, phủ 6 trụ cột khác nhau của chất lượng sống: kinh tế, quan hệ xã hội, sức khỏe, tự do, vị tha và thể chế. Chỉ dùng GDP sẽ không phân biệt được quốc gia tăng trưởng kinh tế nhưng thể chế yếu với quốc gia phát triển toàn diện. Ngoài ra, chính WHR cũng xác nhận 6 yếu tố này giải thích phần lớn chênh lệch điểm sống giữa các quốc gia, nên dùng chúng làm đặc trưng gom cụm là hợp với bản chất dữ liệu.

### Câu 3. Ranh giới bất biến (quy tắc vàng) của đề tài là gì và nhóm kiểm soát bằng cách nào?

Quy tắc vàng: **tuyệt đối không đưa `happiness_score` và `happiness_rank` vào ma trận đặc trưng $X$**; gom cụm chỉ bằng 6 yếu tố cơ sở, điểm hạnh phúc chỉ dùng ở bước 9 để hậu kiểm.

Lý do: trong dữ liệu, `happiness_score` bằng tổng 6 yếu tố cộng `dystopia_residual` (nhóm đã kiểm chứng trên 2015–2017, sai lệch lớn nhất chỉ 0,00051 do làm tròn). Nếu đưa điểm hạnh phúc vào $X$, cụm bị chi phối bởi chính biến cần giải thích, bước hậu kiểm trở thành vòng tròn và mất giá trị khoa học. Nhóm kiểm soát ở ba tầng: danh sách `CORE_FEATURES` trong `src/data/data_loader.py` chỉ có 6 cột; script `scripts/verify_scratch_implementations.py` assert bất biến $X$; và kết quả đối chiếu cho thấy dù không dùng điểm hạnh phúc, các cụm vẫn phân hóa rất mạnh về điểm hạnh phúc thực tế (chênh lệch trung bình giữa cụm cao nhất và thấp nhất của cấu hình K-Means/Z-score là 2,46–2,72 điểm trên thang 0–10 tùy năm).

### Câu 4. Vì sao không gộp cả 5 năm thành một bảng rồi gom cụm một lần?

Nhóm đã cân nhắc và chốt phương án ngược lại (ghi tại `docs/adr/0002`), vì gộp 5 năm có ba hệ quả xấu:

1. Mỗi quốc gia lặp lại 5 lần nên cụm bị chi phối bởi những năm nhiều dữ liệu; quốc gia thiếu một năm bị kéo lệch.
2. Chỉ còn một mô hình duy nhất, mất khả năng theo dõi quốc gia dịch chuyển giữa các nhóm — trong khi đây là một câu hỏi khai thác chính của đề tài.
3. Ngầm giả định cấu trúc phân nhóm không thay đổi trong 5 năm, trong khi bản chất dữ liệu là chuỗi khảo sát theo năm.

Nhóm chạy **5 thí nghiệm độc lập**, mỗi năm một lần gom cụm, rồi ghép cụm liên năm bằng thuật toán tham lam và giữ cấu hình $k=3$ làm chuẩn đối chứng xuyên năm. Mọi so sánh theo thời gian đều ghi rõ cỡ mẫu từng năm: 158/157/155/156/156 (năm 2018 còn 155 sau khi loại UAE).

---

## PHẦN 2 — TIỀN XỬ LÝ & CHUẨN HÓA (Câu 5 – 8)

### Câu 5. Năm tệp dữ liệu lệch schema thế nào và nhóm xử lý ra sao?

Ba dạng lệch chính:

- **Tên cột đổi qua từng năm:** `Happiness Rank` (2015–2016) → `Happiness.Rank` (2017) → `Overall rank` (2018–2019); `Country` → `Country or region`; `Economy (GDP per Capita)` → `Economy..GDP.per.Capita.` → `GDP per capita`; `Family` → `Social support`; `Trust (Government Corruption)` → `Perceptions of corruption`.
- **Cột xuất hiện rồi biến mất:** `Region` chỉ có 2015–2016; các cột sai số khảo sát chỉ có ở 2015–2017.
- **Tên quốc gia ghi khác nhau:** `Macedonia`/`North Macedonia`, `Swaziland`/`Eswatini`, `Taiwan Province of China`, `Hong Kong S.A.R., China`, `Trinidad & Tobago`, `Somaliland region`.

Cách xử lý: hàm `standardize_columns` dùng từ điển `COLUMN_MAPPING` đưa toàn bộ về 13 cột snake_case chuẩn; hàm `harmonize_country_names` với `COUNTRY_NAME_FIXES` đồng bộ tên quốc gia để bảng dịch chuyển không bị tách dòng; cột `region` thiếu được bù từ dữ liệu 2015–2016 và có bảng dự phòng `REGION_FALLBACKS`, nhưng chỉ dùng tham khảo chứ không đưa vào gom cụm. Kết quả cuối: `data/interim/happiness_merged.csv` 781 dòng, 13 cột.

### Câu 6. Vì sao loại bỏ `Standard Error`, `Lower/Upper Confidence Interval`, `Whisker.high/low`?

Các cột này là **sai số chọn mẫu và khoảng tin cậy 95%** của cuộc khảo sát Gallup, không phải thuộc tính kinh tế – xã hội của quốc gia. Chúng phụ thuộc cỡ mẫu và độ biến động câu trả lời, không phản ánh mức sống. Nếu giữ lại:

- Khoảng cách Euclidean bị nhiễu bởi các đại lượng thống kê thuần túy, làm cụm lệch theo độ chính xác khảo sát thay vì theo chất lượng sống.
- Ma trận đặc trưng tăng từ 6 lên 8–10 chiều một cách vô nghĩa, làm loãng tín hiệu của 6 trụ cột chính.

Sau xử lý, bảng interim chỉ giữ đúng 13 cột trong `INTERIM_COLUMNS`; script audit M1 sẽ quét lại và xác nhận không còn cột nào chứa từ khóa `standard error`, `whisker` hay `confidence`.

### Câu 7. Vì sao loại dòng United Arab Emirates (UAE) năm 2018?

Tệp `data/raw/2018.csv` có đúng **một giá trị khuyết duy nhất** của cả 5 năm: `Perceptions of corruption` của UAE (các chỉ số khác của UAE năm đó vẫn đủ). Nhóm xử lý bằng cách loại đúng 1 dòng, không điền giá trị thiếu, vì:

- Điền bằng trung bình sẽ tự tay tạo ra một giá trị giả cho 1 quốc gia, làm sai lệch kết quả gom cụm và không thể giải trình trước hội đồng.
- Không thể bỏ cả cột `corruption_perception` chỉ vì 1 dòng, vì cột này là một trong 6 trụ cột và ảnh hưởng đến 155 quốc gia còn lại của năm 2018.

Kết quả: 782 dòng thô → 781 dòng sạch; trong bảng dịch chuyển 156 quốc gia, UAE vẫn xuất hiện với `cluster_2018 = NaN` — đây là khuyết thiếu có chủ đích, được ghi chú rõ, không phải lỗi dữ liệu.

### Câu 8. So sánh Z-score và Min-Max, vì sao nhóm chọn Z-score làm cấu hình chính?

Công thức: Z-score cho $z = (x - \mu)/\sigma$; Min-Max cho $x' = (x - \min)/(\max - \min)$.

- Min-Max ép mọi biến về $[0; 1]$ nhưng **rất nhạy với ngoại lai**: một quốc gia có GDP hoặc tuổi thọ đột biến sẽ nén toàn bộ các quốc gia còn lại vào một khoảng nhỏ, làm mất độ phân giải giữa các nước trung bình.
- Z-score đưa các biến về cùng đơn vị độ lệch chuẩn, giữ nguyên hình dáng phân phối và mức độ phân tán tương đối, nên mỗi trụ cột đóng góp công bằng vào khoảng cách Euclidean.

Nhóm vẫn chạy đủ cả ba phương án để so sánh (`reports/tables/model_comparison_metrics_by_year.csv`): với K-Means ở $k=3$, Silhouette của Z-score là 0,293–0,344; Min-Max 0,308–0,347; dữ liệu thô 0,314–0,340. Chênh lệch giữa ba phương án rất nhỏ (dưới 0,05), nên quyết định không chỉ dựa vào Silhouette mà dựa vào bản chất phép biến đổi: dữ liệu thô để GDP lệch mạnh chi phối không gian khoảng cách, Min-Max bị ngoại lai kéo; Z-score là lựa chọn có cơ sở diễn giải rõ ràng nhất và giữ được đóng góp cân bằng của cả 6 trụ cột. Độ ổn định của Z-score qua 10 seed cũng đạt ARI trung bình 0,979–1,000.

---

## PHẦN 3 — THUẬT TOÁN FROM-SCRATCH & ĐO LƯỜNG (Câu 9 – 12)

### Câu 9. K-Means++ khởi tạo tâm cụm thế nào và Inertia đo cái gì?

K-Means nhóm tự cài đặt trong `src/models/clustering.py`, không gọi black-box của thư viện. Khởi tạo K-Means++ gồm các bước:

1. Chọn ngẫu nhiên tâm cụm đầu tiên từ dữ liệu.
2. Với mỗi điểm, tính khoảng cách bình phương đến tâm gần nhất; chọn tâm tiếp theo với xác suất tỉ lệ thuận với khoảng cách bình phương đó — điểm càng xa tâm cũ càng dễ được chọn.
3. Lặp đến khi đủ $k$ tâm, sau đó chạy vòng lặp gán điểm – cập nhật tâm cho đến khi hội tụ.

Cách khởi tạo này giảm khả năng rơi vào cực tiểu địa phương so với khởi tạo hoàn toàn ngẫu nhiên; nhóm chạy `n_init=10` lần với các seed khác nhau và giữ lần có chất lượng tốt nhất.

**Inertia (WCSS)** là tổng bình phương khoảng cách từ mỗi điểm đến tâm cụm của nó:

$$\text{Inertia} = \sum_{i=1}^{n} \lVert x_i - \mu_{c(i)} \rVert^2$$

Inertia càng nhỏ thì các điểm càng gần tâm cụm, nhưng giảm mãi khi tăng $k$ nên không dùng đơn lẻ để chọn $k$; nhóm dùng nó để vẽ biểu đồ khuỷu tay (Elbow) song song với Silhouette.

### Câu 10. Ward linkage hoạt động thế nào và công thức Lance–Williams liên quan gì?

Phân cấp Ward là phương pháp gộp cụm (agglomerative): bắt đầu mỗi điểm là một cụm, mỗi bước gộp hai cụm sao cho **tổng phương sai nội cụm tăng ít nhất**. Tiêu chí gộp giữa hai cụm $A$ và $B$ có thể viết qua khoảng cách tâm cụm:

$$\Delta(A, B) = \frac{n_A n_B}{n_A + n_B} \lVert \mu_A - \mu_B \rVert^2$$

Công thức Lance–Williams là cách cập nhật khoảng cách giữa cụm mới $A \cup B$ và cụm còn lại $C$ mà không cần tính lại toàn bộ từ đầu:

$$d(A \cup B, C) = \frac{n_A + n_C}{n_A + n_B + n_C}\, d(A, C) + \frac{n_B + n_C}{n_A + n_B + n_C}\, d(B, C) - \frac{n_C}{n_A + n_B + n_C}\, d(A, B)$$

Nhóm tự cài đặt Ward thật kèm bộ nhớ đệm tâm cụm để tránh tính lại từ đầu, chạy 156 điểm trong khoảng 0,8–1,4 giây mỗi năm (cột `runtime_seconds` trong `model_comparison_metrics_by_year.csv`). Ward là thuật toán tất định: chạy lại nhiều lần cho cùng kết quả, nên trong bảng độ ổn định nhóm ghi ARI = 1,0 kèm giải thích thay vì chạy 10 seed hình thức.

### Câu 11. DBSCAN hoạt động thế nào và kết quả quét tham số của nhóm ra sao?

DBSCAN gom cụm theo mật độ với hai tham số: bán kính `eps` và số điểm tối thiểu `min_samples`. Mỗi điểm được phân loại:

- **Điểm lõi:** có ít nhất `min_samples` điểm (kể cả nó) nằm trong bán kính `eps`.
- **Điểm biên:** không phải lõi nhưng nằm trong bán kính của một điểm lõi — được gán vào cụm của điểm lõi đó.
- **Nhiễu (nhãn −1):** không thỏa cả hai điều kiện trên.

Nhóm tự cài đặt `SimpleDBSCAN` (duyệt vùng lân cận, lan truyền nhãn) và quét toàn bộ lưới `eps ∈ {0.6, 0.8, 1.0, 1.2}` × `min_samples ∈ {3, 4, 5}` cho từng năm (60 dòng trong `reports/tables/dbscan_sweep.csv`). Kết quả điển hình với cấu hình tốt nhất (`eps=1.2`, `min_samples=4`): năm 2015 được 2 cụm + 34 điểm nhiễu (Silhouette 0,298); các năm 2016, 2017 chỉ còn 1 cụm + hơn 30 nhiễu nên Silhouette bằng 0; năm 2019 Silhouette âm (−0,081). Nguyên nhân là 6 chiều đặc trưng đã chuẩn hóa có mật độ khá đồng đều, không tồn tại "vùng dày – vùng thưa" rõ rệt để DBSCAN khai thác. Nhóm giữ DBSCAN như phương án đối chứng để chứng minh dữ liệu quốc gia phù hợp hơn với phương pháp dựa trên khoảng cách (K-Means, Ward).

### Câu 12. Silhouette đo gì và ARI 10 seed nói lên điều gì?

**Silhouette** của điểm $i$: gọi $a(i)$ là khoảng cách trung bình đến các điểm cùng cụm (độ kết dính), $b(i)$ là khoảng cách trung bình nhỏ nhất đến một cụm khác (độ phân tách), thì

$$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))} \in [-1; 1]$$

Điểm số gần 1 nghĩa là điểm nằm gọn trong cụm của mình và xa cụm khác; gần 0 là nằm sát ranh giới; âm là bị gán sai cụm. Hệ số Silhouette của cả tập là trung bình của $s(i)$ — nhóm tự cài đặt từng bước tính $a$, $b$, $s$ bằng vòng lặp trong `calculate_silhouette_score_simple`.

**ARI (Adjusted Rand Index)** đo mức trùng khớp nhãn cụm giữa hai lần chạy, đã hiệu chỉnh loại bỏ yếu tố ngẫu nhiên: hai kết quả giống hệt nhau cho ARI = 1; gán nhãn ngẫu nhiên cho ARI xấp xỉ 0. Nhóm chạy K-Means 10 lần với 10 seed khác nhau cho mỗi năm, tính ARI cho từng cặp trong 45 cặp (`reports/tables/stability_ari.csv`). Kết quả cấu hình chính K-Means/Z-score: ARI trung bình 0,979–1,000; cặp thấp nhất trong toàn bộ 5 năm là 0,9446. Nghĩa là kết quả gom cụm gần như không phụ thuộc seed — cụm được hình thành bởi cấu trúc thật của dữ liệu, không phải may mắn của một lần khởi tạo.

---

## PHẦN 4 — DIỄN GIẢI TRI THỨC, GHÉP CỤM LIÊN NĂM & DEMO (Câu 13 – 16)

### Câu 13. Chân dung cụm (Cluster Profile) được xây dựng và đặt tên thế nào?

Với mỗi cụm, nhóm tính **giá trị trung bình 6 yếu tố** trên các quốc gia thành viên (vẽ thành Radar Chart) rồi mô tả bằng ngôn ngữ kinh tế – xã hội. Kết quả thực nghiệm của cấu hình K-Means/Z-score, $k^* = 3$ đồng thuận cả 5 năm:

| Cụm | Đặc điểm 6 yếu tố | Số quốc gia mỗi năm | Điểm hạnh phúc trung bình thực tế (hậu kiểm) |
|:--|:--|:--:|:--:|
| **Cụm 1 — Hạnh phúc cao (Phát triển toàn diện)** | Vượt trội đồng thời ở GDP, tuổi thọ, hỗ trợ xã hội; nhận thức tham nhũng cao nhất | 29 / 27 / 29 / 24 / 28 | 6,73 – 6,85 |
| **Cụm 2 — Hạnh phúc trung bình (Đang phát triển)** | Các chỉ số ở mức trung bình khá, đông quốc gia nhất | 79 / 84 / 80 / 85 / 82 | 5,57 – 5,61 |
| **Cụm 3 — Hạnh phúc thấp (Khó khăn & Thách thức)** | Điểm rất thấp ở hầu hết trụ cột kinh tế – y tế – tự do | 50 / 46 / 46 / 46 / 46 | 4,10 – 4,26 |

Điểm cần nhấn mạnh khi bảo vệ: tên cụm đặt theo **chân dung 6 yếu tố**, nhưng thứ tự điểm hạnh phúc ở cột cuối là kết quả hậu kiểm độc lập — thứ tự này trùng khớp tuyệt đối giữa 5 năm, chứng minh cấu trúc phân nhóm có ý nghĩa thực tế chứ không phải phân chia cơ học. Các nhận xét kiểu "Cụm 1 hạnh phúc nhất" chỉ được phát biểu sau bước hậu kiểm này.

### Câu 14. Thuật toán ghép cụm liên năm `match_clusters_greedy` hoạt động thế nào?

Vì mỗi năm gom cụm độc lập nên số hiệu cụm (0, 1, 2) không mang ý nghĩa so sánh giữa các năm — cụm 1 năm sau có thể là cụm 2 năm trước. Hàm `match_clusters_greedy(centroids_a, centroids_b, scores_a, scores_b)` giải quyết vấn đề bằng ghép tham lam:

1. Tính khoảng cách Euclidean giữa **mọi cặp tâm cụm** của hai năm liền kề (6 chiều, trên dữ liệu đã chuẩn hóa Z-score).
2. Sắp xếp các cặp theo khoảng cách tăng dần; nếu hai cặp có khoảng cách chênh nhau dưới $10^{-6}$ thì xét thêm độ chênh lệch điểm hạnh phúc trung bình làm tiêu chí phụ (tie-break).
3. Lần lượt ghép từng cặp chưa dùng: cụm năm sau nhận số hiệu của cụm năm trước gần nhất.

Kết quả trong `reports/tables/cross_year_matching.csv`: 12 cặp ghép ứng với 4 mốc chuyển tiếp (2015→2016, 2016→2017, 2017→2018, 2018→2019) × 3 cặp cụm mỗi mốc; khoảng cách tâm cụm của các cặp được ghép từ 0,057 đến 0,420; chênh lệch điểm hạnh phúc giữa hai cụm được ghép tối đa 0,092. Ngoài ra, cấu hình đối chứng $k=3$ cho ARI giữa $k^*$ và $k=3$ bằng 1,0 ở mọi năm, nghĩa là khi cả hai năm đều dùng 3 cụm thì phân hoạch không đổi — đây là căn cứ để bảng dịch chuyển dùng số hiệu cụm nhất quán.

### Câu 15. Xu hướng dịch chuyển cụm của 156 quốc gia qua 5 năm cho thấy gì?

Bảng `data/processed/country_cluster_shift.csv` theo dõi nhãn cụm của 156 quốc gia qua 5 năm (2018 của UAE là NaN do khuyết dữ liệu). Phân bố trạng thái:

| Trạng thái | Số quốc gia | Tỷ lệ | Ví dụ |
|:--|:--:|:--:|:--|
| Ổn định tuyệt đối (không đổi cụm) | 142 | 91,0% | Việt Nam giữ nguyên cụm trung bình cả 5 năm; Na Uy giữ nguyên cụm cao |
| Biến động trung gian (có đổi rồi quay lại) | 8 | 5,1% | Bahrain, Iran, Israel, Saudi Arabia, Tajikistan, Thái Lan, Turkmenistan, Anh |
| Cải thiện nhóm (đi lên) | 4 | 2,6% | Botswana, Georgia, Indonesia, Myanmar |
| Suy giảm nhóm (đi xuống) | 2 | 1,3% | Kuwait, Uruguay |

Hàm ý: cấu trúc phân tầng hạnh phúc toàn cầu **rất bền vững** trong giai đoạn 2015–2019 — hơn 91% quốc gia không đổi nhóm. Số ít dịch chuyển chủ yếu do biến động ở các trụ cột riêng lẻ (tăng trưởng kinh tế, ổn định thể chế), không phải do thay đổi diện rộng. Cũng vì tính bền vững này, nhóm chọn $k=3$ làm cấu hình kể chuyện chính xuyên suốt báo cáo.

### Câu 16. Demo Streamlit 4 tab được kiến trúc như thế nào?

Ứng dụng `app/app.py` thiết kế 4 tab tương tác, cùng đọc dữ liệu từ `data/interim/` và `data/processed/`:

1. **Tab 1 — Tổng quan cụm & Radar Chart:** chọn năm (2015–2019), thuật toán (K-Means/Ward), hiển thị bảng kết quả gom cụm, Radar chart chân dung cụm và bảng chỉ số Silhouette/Davies-Bouldin theo cấu hình đã chọn.
2. **Tab 2 — Bản đồ thế giới (Choropleth Map):** tô màu quốc gia theo cụm bằng mã `iso_alpha` ISO-3, bảo đảm không bị khuyết màu trên bản đồ; cho phép đổi năm và cấu hình.
3. **Tab 3 — Tra cứu quốc gia & Dịch chuyển cụm:** nhập tên quốc gia (ví dụ Vietnam, Norway), hiển thị biểu đồ diễn biến 6 chỉ số qua 5 năm và lịch sử chuyển nhóm lấy từ `country_cluster_shift.csv`.
4. **Tab 4 — Thử nghiệm gán nhãn quốc gia mới (What-if):** người dùng kéo thanh trượt 6 đặc trưng giả định, hệ thống tính khoảng cách Euclidean từ vector vừa nhập đến tâm các cụm (đã lưu trong `models/*.json`) và gán cụm tức thì.

Lưu ý kỹ thuật: ứng dụng không huấn luyện lại mô hình khi người dùng tương tác mà đọc tâm cụm + tham số scaler từ artifact JSON; dùng `@st.cache_data` để không nạp lại dữ liệu mỗi lần kéo slider; chọn năm/thuật toán/scaler/$k$ khác nhau thì số liệu và metric thay đổi theo cấu hình thật, không hardcode.

---

## PHẦN 5 — HẠN CHẾ, HƯỚNG PHÁT TRIỂN & ĐỔI VAI REHEARSAL (Câu 17 – 20)

### Câu 17. Hạn chế khách quan của dữ liệu và phương pháp là gì?

**Về dữ liệu:**

- Bộ dữ liệu **thiếu các chỉ số văn hóa – thể chế chuyên sâu**: chỉ có 6 trụ cột của Gallup, không có phân biệt tôn giáo, ngôn ngữ, cấu trúc gia đình, chất lượng quản trị địa phương. Điều này giải thích vì sao `dystopia_residual` vẫn lớn ở một số quốc gia (0,33–3,84 tùy năm) — phần "chưa giải thích được" của mô hình.
- **Biến động ngoại lai theo năm:** cỡ mẫu mỗi năm khác nhau (158/157/155/156/156), một số quốc gia chỉ xuất hiện một phần giai đoạn, UAE khuyết 2018. Sai số khảo sát và trung bình trượt khiến điểm số một quốc gia có thể nhảy nhẹ giữa hai năm liền kề dù cuộc sống không đổi nhiều.
- **Thang đo chủ quan:** Cantril Ladder là tự đánh giá, chịu ảnh hưởng văn hóa "nói giảm" hoặc "khoe" của từng dân tộc — nhóm không thể kiểm soát sai lệch này bằng kỹ thuật.

**Về phương pháp:**

- Gom cụm không có nhãn chuẩn để đối chiếu (không có ground truth), nên mọi kết luận dựa trên các độ đo nội tại (Silhouette, Davies-Bouldin) và hậu kiểm bằng điểm hạnh phúc.
- Tên cụm mang tính diễn giải chủ quan của nhóm; nhóm đã thống nhất đặt tên theo chân dung 6 yếu tố và giữ nguyên cách đặt tên qua 5 năm để tránh mâu thuẫn.
- Nhãn cụm chỉ so sánh được giữa các năm nhờ ghép tham lam; khi $k^*$ lệch nhau giữa hai năm thì chỉ ghép được phần nhỏ hơn — nhóm xử lý bằng cấu hình đối chứng $k=3$.

### Câu 18. Hướng phát triển của đề tài là gì?

1. **Mở rộng chuỗi thời gian**: thêm dữ liệu 2020–2024 (có các bản WHR mới) để kiểm tra các cụm có giữ nguyên cấu trúc sau đại dịch COVID-19 hay không.
2. **Bổ sung đặc trưng ngoài 6 trụ cột**: ghép thêm dữ liệu Ngân hàng Thế giới (bất bình đẳng Gini, chi tiêu y tế, thất nghiệp), chỉ số chất lượng quản trị (WGI) để bước hậu kiểm giải thích được nhiều phần dư hơn.
3. **So sánh thêm thuật toán**: phân cụm mờ (Fuzzy C-Means) cho phép quốc gia mang nhiều mức độ thuộc cụm, phù hợp với bản chất "chuyển tiếp" của các nước đang phát triển.
4. **Phân tích độ nhạy theo trọng số**: khảo sát cụm thay đổi thế nào khi đặt trọng số ưu tiên cho từng trụ cột (ví dụ thể chế quan trọng hơn GDP).
5. **Đưa demo lên dashboard công khai** (Streamlit Community Cloud) và bổ sung chế độ xuất báo cáo PDF cho từng quốc gia.

### Câu 19. Kịch bản đổi vai rehearsal: Trung trình bày phần "Thu thập và Tiền xử lý dữ liệu" thay Trường — cần nắm những gì?

Nội dung bắt buộc phải trình bày được, theo đúng thứ tự pipeline:

1. **Nguồn gốc:** 5 tệp `data/raw/2015..2019.csv` (Kaggle), cỡ mẫu từng năm 158/157/155/156/156, tổng 782 dòng thô.
2. **Ba vấn đề chất lượng dữ liệu:** lệch tên cột qua các năm; cột sai số khảo sát (Standard Error, CI, Whisker) chỉ có ở 2015–2017; UAE 2018 khuyết `Perceptions of corruption`.
3. **Quy trình xử lý trong `src/data/data_loader.py`:** `standardize_columns` (đưa về 13 cột chuẩn) → `harmonize_country_names` (Macedonia/Eswatini/Taiwan…) → cộng thêm `country_to_iso3` cho bản đồ → loại dòng UAE 2018 → tính `dystopia_residual` cho 2018–2019 → xuất `data/interim/happiness_merged.csv` 781 dòng.
4. **Lý do từng quyết định:** loại cột sai số vì không mang thông tin nội hàm; loại UAE 2018 thay vì điền khuyết vì chỉ ảnh hưởng đúng 1 dòng dữ liệu và việc điền giá trị giả sẽ làm sai lệch kết quả gom cụm; giữ cột `region` chỉ để tham khảo, không dùng gom cụm vì chỉ có 2015–2016.
5. **Bằng chứng kiểm chứng:** chạy `python scripts/audit_m1_data_quality_and_iso3.py` — script kiểm lại cỡ mẫu, UAE 2018, 781 dòng, 100% mã ISO-3 hợp lệ và in log PASS ra `logs/audit_m1_quality.log`.

Khi bị hỏi ngoài phần mình phụ trách, cần nhớ tối thiểu: quy tắc vàng, các mốc $k^*=3$ cả 5 năm, Silhouette 0,293–0,344 và tỷ lệ ổn định 142/156 quốc gia.

### Câu 20. Một số câu hỏi hội đồng có thể hỏi và cách trả lời?

**H1. "Silhouette chỉ khoảng 0,29–0,34, sao dám kết luận các cụm rõ ràng?"**
Với dữ liệu kinh tế – xã hội nhiều chiều, Silhouette 0,3 là giá trị chấp nhận được vì các quốc gia có xu hướng nằm dọc một phổ liên tục chứ không tách rời hoàn toàn. Điều quan trọng là cả 5 năm đều cho kết quả nhất quán: $k^*=3$, Silhouette cực đại ở đúng $k$ này, độ ổn định ARI qua 10 seed đạt trên 0,979 và bước hậu kiểm cho thấy chênh lệch điểm hạnh phúc trung bình giữa cụm cao nhất và thấp nhất của cấu hình chính là 2,46–2,72 điểm — đủ để phân cụm có ý nghĩa thực tiễn.

**H2. "Vì sao chọn $k=3$ mà không phải $k=4$ hay $k=2$?"**
Vì cả Elbow lẫn Silhouette đều đạt cực trị tại $k=3$ trên cả 5 năm (bảng `k_sensitivity_by_year.csv` 40 dòng khảo sát $k \in [2;9]$), và $k=3$ cũng khớp với cấu trúc đặc tính của dữ liệu: một nhóm phát triển toàn diện, một nhóm trung bình đông đảo, một nhóm khó khăn. Nhóm vẫn giữ $k=3$ làm đối chứng xuyên năm sau khi xác nhận $k^*=3$ trùng khớp.

**H3. "Nếu loại UAE 2018 thì kết quả năm 2018 có bị lệch không?"**
UAE chỉ là 1/156 quốc gia (0,6%), hơn nữa kiểm tra cho thấy cấu trúc cụm 2018 vẫn đồng thuận $k^*=3$ và hậu kiểm điểm hạnh phúc vẫn phân hóa đúng thứ tự. Nhóm chọn phương án trung thực về dữ liệu thay vì điền khuyết giả tạo ảnh hưởng đến 155 quốc gia còn lại.

**H4. "Tại sao đường hạnh phúc của một số nước biến động mà kết luận vẫn là 91% ổn định?"**
Con số 142/156 quốc gia ổn định tuyệt đối (không đổi cụm cả 5 năm) đến từ `country_cluster_shift.csv`. Các trường hợp đổi nhóm đều có thể truy vết: 4 quốc gia cải thiện (Botswana, Georgia, Indonesia, Myanmar), 2 suy giảm (Kuwait, Uruguay), 8 biến động trung gian. Nhóm không suy diễn nhân quả cho từng quốc gia mà chỉ nêu hiện tượng và các trụ cột thay đổi tương ứng.

**H5. "Nếu đưa `happiness_score` vào gom cụm thì sao?"**
Về kỹ thuật sẽ cho cụm tách biệt "đẹp" hơn vì điểm hạnh phúc tổng hợp đúng lượng thông tin cần tìm, nhưng như vậy là tự dự đoán chính mình: `happiness_score` bằng tổng 6 yếu tố cộng phần dư (sai lệch 0,00051), nên cụm chỉ tái tạo lại một trục thay vì khám phá cấu trúc đa chiều. Đây là lý do đề cương yêu cầu hậu kiểm độc lập và nhóm tuân thủ nghiêm.
