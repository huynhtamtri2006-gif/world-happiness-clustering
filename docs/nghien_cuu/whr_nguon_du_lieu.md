# Nghiên cứu nguồn dữ liệu World Happiness Report (2015 – 2019)

- **Học phần:** Khai thác dữ liệu (Data Mining)
- **Đề tài 16:** Phân nhóm quốc gia theo các yếu tố tạo nên mức độ hạnh phúc (World Happiness Report)
- **Nhóm thực hiện:** Nhóm 12 — Hà Mạnh Trường, Huỳnh Tâm Trí, Ngô Quang Trung
- **Người tổng hợp:** Ngô Quang Trung (MSSV: 2045240325)
- **Mốc thực hiện:** M1 — Ngày 4 (thu thập nguồn tài liệu phương pháp luận)

---

## 1. Bối cảnh báo cáo và nguồn dữ liệu

World Happiness Report (WHR) là báo cáo thường niên về mức độ hạnh phúc của các quốc gia, công bố lần đầu năm 2012 nhân hội nghị của Liên Hợp Quốc về hạnh phúc và được duy trì bởi Mạng lưới Giải pháp Phát triển Bền vững (SDSN). Bản 2017 công bố ngày 20/3/2017 — đúng Ngày Quốc tế Hạnh phúc — xếp hạng 155 quốc gia. Mục tiêu lâu dài của báo cáo là đưa chỉ số hạnh phúc vào việc hoạch định chính sách công, thay vì chỉ đo tăng trưởng bằng GDP.

Toàn bộ điểm số và xếp hạng trong WHR lấy từ dữ liệu khảo sát của **Gallup World Poll** — khảo sát mẫu đại diện quốc gia, mỗi nước khoảng 1.000 người trưởng thành, dùng trọng số Gallup để hiệu chỉnh theo cơ cấu dân số. Vì vậy, điểm số trong WHR là **ý kiến tự đánh giá của người dân**, không phải chỉ tiêu kinh tế thuần túy.

Bộ dữ liệu nhóm sử dụng là bản tổng hợp trên Kaggle (*World Happiness Report*, tác giả `synful`), gồm 5 tệp CSV cho 5 năm liên tiếp 2015–2019. Mỗi tệp có cấu trúc cột khác nhau (xem Mục 5) nhưng cùng chứa 3 nhóm thông tin:

1. Định danh quốc gia và xếp hạng (`Country`, `Region`, `Overall rank` / `Happiness.Rank`…).
2. Điểm hạnh phúc tổng hợp (`Happiness Score` / `Score`).
3. Sáu yếu tố cơ sở giải thích và cột `Dystopia Residual`.

**Hiện trạng bộ dữ liệu thô trong repo (kiểm tra ngày 3):**

| Năm | Số dòng (quốc gia) | Số cột | Cột sai số tồn tại | Ghi chú chất lượng |
|:---:|:---:|:---:|:---|:---|
| 2015 | 158 | 12 | `Standard Error` | Đủ 6 yếu tố, không khuyết |
| 2016 | 157 | 13 | `Lower/Upper Confidence Interval` | Đủ 6 yếu tố, không khuyết |
| 2017 | 155 | 12 | `Whisker.high`, `Whisker.low` | Đủ 6 yếu tố, không khuyết |
| 2018 | 156 | 9 | Không | UAE khuyết `Perceptions of corruption` (1 giá trị NaN duy nhất của cả 5 năm) |
| 2019 | 156 | 9 | Không | Đủ 6 yếu tố, không khuyết |

Tổng cộng 782 dòng thô; sau khi loại 1 dòng UAE 2018 còn **781 dòng sạch** trong `data/interim/happiness_merged.csv`.

---

## 2. Thang đo Cantril Ladder

### 2.1. Câu hỏi khảo sát

Gallup World Poll đo "đánh giá cuộc sống" (*life evaluation*) bằng câu hỏi Cantril Ladder:

> "Hãy tưởng tượng một chiếc thang với các bậc được đánh số từ 0 ở dưới cùng đến 10 ở trên cùng. Bậc trên cùng (10) tượng trưng cho cuộc sống tốt đẹp nhất có thể đối với bạn, bậc dưới cùng (0) tượng trưng cho cuộc sống tồi tệ nhất có thể. Bạn cảm thấy mình đang đứng ở bậc nào vào lúc này?"

### 2.2. Cách tính điểm quốc gia

- Mỗi cá nhân trả lời một số nguyên/thập phân trong khoảng $[0; 10]$.
- Điểm của quốc gia là **trung bình có trọng số** của các câu trả lời, nhân với trọng số Gallup để bảo đảm tính đại diện dân số.
- Điểm này được gọi là `Happiness Score` (2015–2017) hoặc `Score` (2018–2019) trong bộ dữ liệu, và là cơ sở để xếp hạng (`Happiness Rank` / `Overall rank`).
- Để giảm ảnh hưởng của biến động mẫu theo từng năm, WHR thường lấy trung bình trượt 3 năm gần nhất (ví dụ bản 2017 dùng dữ liệu 2013–2016).

### 2.3. Ý nghĩa và giới hạn của thang đo

Vì là thang tự đánh giá cảm nhận, điểm Cantril Ladder chịu ảnh hưởng của yếu tố văn hóa, ngôn ngữ và kỳ vọng sống của từng dân tộc. Hai người có hoàn cảnh vật chất như nhau ở hai quốc gia khác nhau có thể chấm điểm khác nhau. Đây là lý do nhóm không coi `happiness_score` là một thuộc tính khách quan để gom cụm, mà chỉ dùng nó làm **chuẩn hậu kiểm độc lập** sau khi đã phân nhóm bằng 6 yếu tố cơ sở (xem Mục 5).

---

## 3. Quốc gia giả định Dystopia và Dystopia Residual

### 3.1. Khái niệm Dystopia

Dystopia là một **quốc gia giả định** do nhóm tác giả WHR tạo ra, đại diện cho trường hợp xấu nhất có thể: người dân có thu nhập thấp nhất, tuổi thọ ngắn nhất, hỗ trợ xã hội ít nhất, tự do ít nhất, hào phóng ít nhất và tham nhũng bị nhìn nhận cao nhất. Nói cách khác, Dystopia được dựng từ **giá trị thấp nhất thế giới quan sát được của mỗi yếu tố trong 6 yếu tố cơ sở**, nên mọi quốc gia thực tế đều "tốt hơn" Dystopia ở từng trục.

Mục đích của Dystopia là làm **mốc chuẩn so sánh** để mọi đóng góp của 6 yếu tố đều mang giá trị dương trong các biểu đồ phân rã (*bar chart*) mà WHR công bố. Theo tài liệu của báo cáo, mức sống trung bình của Dystopia được ước lượng khoảng **1,85 trên thang 0–10**.

### 3.2. Dystopia Residual

Trong bộ dữ liệu, cột `Dystopia Residual` (2015–2017) là phần dư chưa được 6 yếu tố giải thích cộng với chuẩn Dystopia:

$$\text{happiness\_score} \approx \left(\sum_{i=1}^{6} \text{factor}_i\right) + \text{dystopia\_residual}$$

Nhóm đã kiểm chứng đẳng thức này trên 3 tệp 2015–2017 bằng `src/data/data_loader.py`: sai lệch tuyệt đối lớn nhất giữa vế trái và vế phải chỉ là **0,00051** (do bộ dữ liệu đã làm tròn 5 chữ số thập phân). Cột `dystopia_residual` thực tế nằm trong khoảng:

| Năm | Min | Max | Ghi chú |
|:---:|:---:|:---:|:---|
| 2015 | 0,3286 | 3,6021 | Có sẵn trong tệp gốc |
| 2016 | 0,8179 | 3,8377 | Có sẵn trong tệp gốc |
| 2017 | 0,3779 | 3,1175 | Có sẵn trong tệp gốc |
| 2018–2019 | — | — | Tệp gốc không có cột này; nhóm tự tính bằng `happiness_score − tổng 6 yếu tố` trong `build_interim_dataset` |

Ý nghĩa thực tiễn: phần dư phản ánh những khía cạnh ngoài 6 yếu tố (văn hóa, thể chế, biến cố lịch sử, tâm lý cộng đồng…) ảnh hưởng đến điểm sống tự đánh giá. Phần dư trung bình xấp xỉ 0 nhưng một số quốc gia có phần dư trên 1 điểm — tức có những điều kiện sống tốt hơn hoặc xấu hơn mức mà 6 chỉ số kinh tế – xã hội có thể dự báo.

### 3.3. Cảnh báo khi dùng cho gom cụm

Vì `happiness_score` bằng tổng 6 yếu tố cộng phần dư (sai lệch không đáng kể), nếu đưa điểm hạnh phúc vào ma trận đặc trưng thì bài toán gom cụm sẽ "tự dự đoán chính nó" — các cụm chỉ đơn thuần tái tạo thứ hạng hạnh phúc, không còn giá trị khám phá. Do đó `dystopia_residual` cũng chỉ dùng để mô tả, không đưa vào ma trận đặc trưng.

---

## 4. Sáu yếu tố cơ sở giải thích

Sáu cột nằm sau cột điểm số trong tệp WHR là mức đóng góp ước lượng của từng yếu tố, tính bằng hồi quy trên mẫu quốc gia và so với chuẩn Dystopia, nên **luôn dương**. Bảng dưới đối chiếu cột gốc trong dữ liệu thô với tên chuẩn hóa trong repo:

| # | Tên chuẩn trong repo | Cột gốc các năm | Nội dung đo lường | Nguồn số liệu |
|:--:|:--|:--|:--|:--|
| 1 | `gdp_per_capita` | `Economy (GDP per Capita)` / `Economy..GDP.per.Capita.` / `GDP per capita` | Sản phẩm quốc nội bình quân đầu người theo sức mua tương đương, lấy log để giảm lệch | Ngân hàng Thế giới (WDI) |
| 2 | `social_support` *(cột `Family` 2015–2017)* | `Family` / `Social support` | Tỷ lệ người trả lời có người thân/bạn bè để dựa vào khi gặp khó khăn | Gallup World Poll |
| 3 | `healthy_life_expectancy` | `Health (Life Expectancy)` / `Health..Life.Expectancy.` / `Healthy life expectancy` | Số năm sống khỏe mạnh kỳ vọng từ lúc sinh | Tổ chức Y tế Thế giới (WHO) |
| 4 | `freedom` | `Freedom` / `Freedom to make life choices` | Mức hài lòng với quyền tự do lựa chọn việc làm, cuộc sống của bản thân | Gallup World Poll |
| 5 | `generosity` | `Generosity` | Mức độ quyên góp từ thiện trong tháng gần nhất, sau khi trừ phần dự báo được bởi GDP | Gallup World Poll |
| 6 | `corruption_perception` | `Trust (Government Corruption)` / `Trust..Government.Corruption.` / `Perceptions of corruption` | Niềm tin vào sự liêm chính của chính phủ và doanh nghiệp | Gallup World Poll |

**Hướng diễn giải cần nhớ:** riêng `corruption_perception` được mã hóa sao cho **giá trị cao = ít tham nhũng = tốt**. Kiểm tra nhanh dữ liệu 2019 cho thấy Phần Lan 0,393 và Đan Mạch 0,410 ở nhóm cao, trong khi Nga 0,031 và Afghanistan 0,025 ở nhóm thấp — đúng với thực tế thể chế. Khi viết nhận xét, tuyệt đối không diễn giải ngược thành "điểm tham nhũng cao".

**Vì sao 6 yếu tố này phù hợp để gom cụm:** cả 6 đều là thang đo liên tục, phản ánh 6 trụ cột khác nhau của chất lượng sống (kinh tế, quan hệ xã hội, sức khỏe, tự do cá nhân, vị tha, thể chế). Kết hợp chúng cho phép phân biệt "phát triển toàn diện" với "tăng trưởng kinh tế nhưng thể chế yếu" — điều mà chỉ dùng GDP không làm được.

Các cột cần loại bỏ:
- `Standard Error` (2015), `Lower/Upper Confidence Interval` (2016), `Whisker.high` / `Whisker.low` (2017): đây là sai số chọn mẫu và khoảng tin cậy của khảo sát, không mang thông tin nội hàm kinh tế – xã hội; giữ lại sẽ làm nhiễu khoảng cách Euclidean.
- `happiness_rank`, `happiness_score`, `dystopia_residual`: không đưa vào ma trận đặc trưng theo quy tắc vàng.

---

## 5. Quy tắc vàng của Đề tài 16

> **Không** đưa `happiness_score` (Điểm hạnh phúc) và `happiness_rank` (Thứ hạng) vào ma trận đặc trưng $X$. Việc gom cụm chỉ dựa trên 6 yếu tố cơ sở; điểm hạnh phúc dùng độc lập ở bước hậu kiểm (Bước 9 — Diễn giải tri thức).

Cơ sở của quy tắc gồm hai lý do:

1. **Lý do toán học:** như đã chứng minh ở Mục 3.2, điểm hạnh phúc là tổng của 6 yếu tố cộng phần dư. Đưa nó vào $X$ khiến cụm bị chi phối bởi chính biến cần giải thích, tạo kết quả "vòng tròn".
2. **Lý do phương pháp luận:** mục tiêu của đề tài là kiểm tra xem **hoàn cảnh kinh tế – xã hội khách quan** có tự hình thành các nhóm quốc gia hay không, rồi mới đối chiếu với mức hạnh phúc thực tế. Nếu dùng điểm hạnh phúc để gom cụm, bước đối chiếu mất tính độc lập và không còn chứng minh được điều gì.

**Cơ chế kiểm soát đã triển khai trong repo:**

| Chốt kiểm soát | Vị trí | Nội dung |
|:--|:--|:--|
| Danh sách đặc trưng cố định | `src/data/data_loader.py` (`CORE_FEATURES`) | Đúng 6 cột, không chứa `happiness_score`/`happiness_rank` |
| Bảng interim 13 cột | `data/interim/happiness_merged.csv` (`INTERIM_COLUMNS`) | Điểm hạnh phúc nằm cùng bảng nhưng tách khỏi ma trận $X$ khi chạy thuật toán |
| Script đối chứng | `scripts/verify_scratch_implementations.py` | Assert bất biến $X$ không chứa 2 cột bị cấm |
| Hậu kiểm bằng số | `notebooks/04_cluster_profiling_and_evaluation.ipynb` | Boxplot `happiness_score` theo cụm; các cụm tách biệt rõ về điểm hạnh phúc dù không dùng biến này để gom |

---

## 6. Nguồn tham khảo

1. Helliwell, J. F., Layard, R., Sachs, J. D. (chủ biên), *World Happiness Report* các bản 2015–2019, Mạng lưới Giải pháp Phát triển Bền vững Liên Hợp Quốc.
2. Data Card bộ dữ liệu *World Happiness Report* trên Kaggle (tài khoản `synful`) và mô tả kèm trong repo: [`data/Aboutdataset.md`](../../data/Aboutdataset.md).
3. Gallup World Poll — tài liệu phương pháp khảo sát và thang đo Cantril Ladder.
4. Tài liệu hướng dẫn đề tài nhóm Khai thác dữ liệu — Mục 1.2 (pipeline 11 bước) và Đề tài 16.
