# TRƯỜNG ĐẠI HỌC CÔNG THƯƠNG TP.HCM
## NGÀNH KHOA HỌC DỮ LIỆU

---

### BÁO CÁO ĐỒ ÁN MÔN HỌC KHAI THÁC DỮ LIỆU - NHÓM 12
### ĐỀ TÀI 16: PHÂN NHÓM QUỐC GIA THEO YẾU TỐ HẠNH PHÚC (WORLD HAPPINESS REPORT)

- **Giảng viên hướng dẫn:** Đinh Nguyễn Trọng Nghĩa
- **Sinh viên thực hiện:**
  1. Hà Mạnh Trường (MSSV: 2045240326 - Nhóm trưởng)
  2. Huỳnh Tâm Trí (MSSV: 2045240315 - Thành viên)
  3. Ngô Quang Trung (MSSV: 2045240325 - Thành viên)
- **Thời gian thực hiện:** TP. Hồ Chí Minh, 2026

---


## Tổng quan đề tài


Báo cáo sử dụng phương pháp gom cụm để khảo sát các nhóm quốc gia có đặc điểm tương tự theo sáu yếu tố liên quan đến mức độ hạnh phúc trong World Happiness Report giai đoạn 2015–2019. Mục tiêu là tìm cấu trúc nhóm trong dữ liệu, so sánh kết quả giữa các thuật toán và cách chuẩn hóa, sau đó dùng điểm hạnh phúc để hỗ trợ diễn giải các nhóm.


Nghiên cứu tập trung trả lời các câu hỏi: Có thể chia các quốc gia thành bao nhiêu nhóm dựa trên sáu yếu tố? Việc chuẩn hóa Z-score, Min-Max hay giữ dữ liệu Raw ảnh hưởng thế nào đến K-Means? Ward và DBSCAN cho kết quả ra sao khi so sánh với K-Means? Kết quả gom cụm có ổn định qua các lần khởi tạo khác nhau không?


Đây là bài toán học không giám sát. Các cụm được hình thành từ đặc trưng đầu vào, không phải từ nhãn hạnh phúc có sẵn. Phân tích được thực hiện riêng cho từng năm, nên kết quả dùng để mô tả cấu trúc nhóm trong từng năm; nghiên cứu không nhằm chứng minh quan hệ nhân quả hoặc dự đoán điểm hạnh phúc.


## Mô tả dữ liệu


Dữ liệu gồm các tệp CSV World Happiness Report theo năm 2015–2019, được lưu trong thư mục data/raw/. Mỗi dòng biểu diễn một quốc gia hoặc vùng lãnh thổ trong một năm. Số bản ghi lần lượt là 158 năm 2015, 157 năm 2016, 155 năm 2017, 156 năm 2018 và 156 năm 2019, tổng cộng 782 bản ghi.


Tên cột và cấu trúc dữ liệu có khác biệt giữa các năm. Các trường liên quan đến phân tích gồm quốc gia, thứ hạng, điểm hạnh phúc và sáu yếu tố: GDP bình quân đầu người, hỗ trợ xã hội, tuổi thọ khỏe mạnh, tự do lựa chọn, hào phóng và nhận thức tham nhũng. Một số tệp còn có thông tin vùng, sai số chuẩn, thành phần dư Dystopia hoặc khoảng tin cậy; các trường phụ này không được dùng làm đặc trưng gom cụm.


Dữ liệu có một trường hợp thiếu đáng chú ý: bản ghi United Arab Emirates năm 2018 không có giá trị về nhận thức tham nhũng. Vì vậy, bản ghi này không có đủ sáu đặc trưng để đưa vào mô hình. Sau khi bỏ các bản ghi thiếu đặc trưng, số quốc gia dùng để gom cụm lần lượt là 158, 157, 155, 155 và 156 theo các năm 2015–2019. Bộ CSV trong repo được ghi nhận là World Happiness Report; khi hoàn thiện bản nộp, nhóm cần bổ sung đường dẫn chính xác đến nguồn tải dữ liệu.


## Tiền xử lý phân tích và khám phá


### Chuẩn hóa và chọn dữ liệu


Tên cột được ánh xạ về một định dạng thống nhất để xử lý dữ liệu qua các năm. Ví dụ, các tên Happiness Score, Happiness.Score và Score được chuẩn hóa thành happiness_score. Các cột về GDP, hỗ trợ xã hội, tuổi thọ, tự do và tham nhũng cũng được đưa về tên chuẩn tương ứng. Sau đó, mỗi bảng được gắn thêm cột year và ghép thành bảng trung gian data/interim/happiness_merged.csv gồm 782 bản ghi.


Khi tạo dữ liệu cho thuật toán, nhóm chọn đúng sáu đặc trưng đã xác định và loại các hàng không có đủ giá trị ở những cột này. Do đó, United Arab Emirates năm 2018 không được đưa vào lần gom cụm của năm đó; nhóm không giả định đã nội suy giá trị còn thiếu. happiness_score và happiness_rank được giữ lại để đối chiếu sau khi gom cụm, không đưa vào ma trận đặc trưng huấn luyện.


### Phân tích khám phá


Notebook phân tích khám phá khảo sát thống kê mô tả của sáu đặc trưng, gồm trung bình, độ lệch chuẩn, các tứ phân vị và độ lệch phân phối. Histogram và KDE được dùng để quan sát hình dạng phân phối; ma trận tương quan được dùng để xem mối liên hệ giữa các đặc trưng và điểm hạnh phúc; boxplot hỗ trợ nhận diện các giá trị có thể là ngoại lệ.


Các kết quả EDA giúp nhóm hiểu thang đo và phân phối dữ liệu trước khi chọn phương pháp chuẩn hóa và thuật toán. EDA ở đây nhằm mô tả dữ liệu, không chứng minh quan hệ nhân quả. Điểm được boxplot đánh dấu là ngoại lệ cần xem xét, không đồng nghĩa với việc điểm đó đã bị loại khỏi dữ liệu.


### Thiết kế thực nghiệm


Nhóm thực hiện năm thí nghiệm độc lập, mỗi thí nghiệm sử dụng dữ liệu của một năm từ 2015 đến 2019. Với từng năm, pipeline gồm: nạp dữ liệu đã chuẩn hóa; chọn sáu đặc trưng; bỏ các bản ghi thiếu đặc trưng; biến đổi thang đo theo cấu hình; chạy thuật toán; tính các metric đánh giá; và dùng điểm hạnh phúc để hậu kiểm kết quả. Nhóm không gộp cả năm năm thành một tập để huấn luyện chung.


Thiết kế thực nghiệm gồm các bước:

- Khảo sát K-Means với k từ 2 đến 9 theo từng năm, dùng Inertia/Elbow và Silhouette để lựa chọn k*. Cấu hình k=3 được giữ làm đối chứng xuyên suốt các năm.
- So sánh năm cấu hình: K-Means/Z-score, K-Means/Min-Max, K-Means/Raw, Ward/Z-score và DBSCAN/Z-score.
- Quét DBSCAN với eps bằng 0,6; 0,8; 1,0; 1,2 và min_samples bằng 3; 4; 5 cho mỗi năm.
- Đánh giá độ ổn định bằng ARI giữa các lần chạy với 10 seed cho K-Means. Ward và DBSCAN được xem là tất định khi dữ liệu và tham số giữ nguyên.
- Hậu kiểm mức độ khác nhau về happiness_score giữa các cụm sau khi phân nhóm. Điểm này không tham gia huấn luyện mô hình.

## Phương pháp mô hình hoá và độ đo


### Đặc trưng và chuẩn hóa


Mỗi quan sát là một quốc gia trong một năm. Ma trận đầu vào gồm sáu yếu tố: GDP bình quân đầu người, hỗ trợ xã hội, tuổi thọ khỏe mạnh, tự do lựa chọn, hào phóng và nhận thức tham nhũng. Điểm hạnh phúc và thứ hạng hạnh phúc chỉ dùng để hậu kiểm, không dùng làm đặc trưng huấn luyện.


Nhóm so sánh ba cách biểu diễn cho K-Means: Z-score, Min-Max và dữ liệu chưa chuẩn hóa (Raw). Z-score chuẩn hóa mỗi đặc trưng theo trung bình và độ lệch chuẩn; Min-Max co giãn về cùng khoảng; Raw giữ nguyên thang đo. Ward và DBSCAN trong ma trận chính dùng Z-score. Việc chuẩn hóa giúp tránh để đặc trưng có thang đo lớn chi phối khoảng cách Euclid.


### Thuật toán

- K-Means: lặp giữa bước gán điểm vào tâm gần nhất và cập nhật tâm bằng trung bình các điểm trong cụm, nhằm giảm tổng bình phương khoảng cách trong cụm (inertia/WCSS). Cần chọn trước k và có thể phụ thuộc khởi tạo.
- Phân cấp Ward: bắt đầu từ các cụm đơn điểm, sau đó gộp cặp cụm làm tăng tổng bình phương sai số trong cụm ít nhất. Cắt cây tại k=3 để so sánh nhất quán.
- DBSCAN: mở rộng cụm từ các vùng có mật độ đủ cao, điều khiển bằng eps và min_samples; điểm ngoài cụm được gán nhãn nhiễu -1. Thuật toán không cần chọn trước số cụm nhưng nhạy với tham số và thang đo.

Các thuật toán và độ đo của pipeline được cài đặt from-scratch. Thư viện chuẩn chỉ dùng trong script kiểm chứng đối chiếu, không thay thế phần triển khai trong notebook hoặc ứng dụng.


### Tham số và độ đo đánh giá


Khảo sát K-Means với k từ 2 đến 9 cho từng năm. Elbow/Inertia phản ánh độ chặt của cụm; Silhouette phản ánh mức gần nhau trong cụm so với cụm lân cận, và giá trị cao hơn thường biểu thị cụm tách biệt hơn. Chọn k* dựa trên Silhouette kết hợp quan sát Elbow, đồng thời dùng k=3 làm cấu hình đối chứng.


Ma trận so sánh gồm K-Means/Z-score, K-Means/Min-Max, K-Means/Raw, Ward/Z-score và DBSCAN/Z-score. Các metric gồm Silhouette, Davies–Bouldin (thấp hơn thường tốt hơn), Calinski–Harabasz (cao hơn thường tốt hơn), số điểm nhiễu và thời gian chạy. Inertia phụ thuộc thang đo nên chỉ so trong cùng cách biểu diễn, không so trực tiếp giữa Raw, Z-score và Min-Max.


Độ ổn định được đo bằng Adjusted Rand Index (ARI) giữa các lần chạy. ARI gần 1 cho thấy các phân hoạch tương tự sau khi tính đến hoán đổi nhãn cụm. Với thuật toán tất định và dữ liệu/tham số cố định, ARI bằng 1 giữa các lần lặp là kết quả dự kiến.


## Khảo sát tham số và độ ổn định


### Khảo sát số cụm


**Bảng 1: Kết quả khảo sát số cụm k* tối ưu (K-Means/Z-score) qua 5 năm**

| NĂM | K | SILHOUETTE | INERTIA |
| --- | --- | --- | --- |
| 2015 | 3 | 0,293 | 481,941 |
| 2016 | 3 | 0,304 | 472,850 |
| 2017 | 3 | 0,313 | 457,087 |
| 2018 | 3 | 0,336 | 446,182 |
| 2019 | 3 | 0,344 | 440,579 |



Kết quả chọn k*=3 ở cả năm năm. Silhouette tại k=3 tăng từ 0,293 năm 2015 lên 0,344 năm 2019. Inertia được dùng để xem Elbow trong từng năm; không diễn giải trị số giữa các năm như thể chúng cùng một thang đo.


Kết quả ủng hộ ba cụm làm cấu hình chính và làm cơ sở cho đối chứng k=3. Các cụm được ước lượng độc lập mỗi năm, nên kết quả không khẳng định cấu trúc quốc gia bất biến theo thời gian.


### Quét tham số DBSCAN


**Bảng 2: Thống kê số tổ hợp tham số DBSCAN đủ điều kiện tính metric qua 5 năm**

| NĂM | ĐỦ CỤM ĐỂ TÍNH METRIC | KHÔNG ĐỦ CỤM ĐỂ TÍNH METRIC | TỔNG |
| --- | --- | --- | --- |
| 2015 | 3 | 9 | 12 |
| 2016 | 5 | 7 | 12 |
| 2017 | 4 | 8 | 12 |
| 2018 | 2 | 10 | 12 |
| 2019 | 1 | 11 | 12 |



DBSCAN được quét với 12 tổ hợp tham số mỗi năm: eps thuộc {0,6; 0,8; 1,0; 1,2} và min_samples thuộc {3; 4; 5}, tổng cộng 60 cấu hình.


Phần lớn tổ hợp không tạo đủ cụm hợp lệ để tính metric nội bộ. Vì DBSCAN đánh dấu một phần quan sát là nhiễu, cần xem đồng thời số cụm, số điểm nhiễu và metric trên các điểm được gán cụm; không nên xếp hạng chỉ bằng Silhouette.


### Độ ổn định


**Bảng 3: Chỉ số Adjusted Rand Index (ARI) đánh giá độ ổn định giữa các lần chạy**

| THUẬT TOÁN | CHUẨN HÓA | TRUNG BÌNH |
| --- | --- | --- |
| DBSCAN | Z-score | 1,000 |
| K-MEANS | Min-Max | 1,000 |
| K-MEANS | Raw | 0,9556 |
| K-MEANS | Z-score | 0,9904 |
| WARD | Z-score | 1,000 |



Ward và DBSCAN là tất định với dữ liệu và tham số cố định nên ARI bằng 1,0000 là phù hợp. K-Means Min-Max đạt 1,0000 trong các lần chạy đã khảo sát; Z-score đạt 0,9904 và Raw đạt 0,9556, cho thấy cấu hình Raw nhạy với khởi tạo hơn tương đối. Đây là kết quả trong thiết lập thí nghiệm này, không phải bảo đảm cho mọi dữ liệu và seed.


## So sánh và đánh giá cấu hình


### Metric trung bình giai đoạn 2015-2019


**Bảng 4: So sánh toàn diện 5 cấu hình gom cụm lõi (trung bình 2015–2019)**

| THUẬT TOÁN | CHUẨN HÓA | SILHOUETTE ↑ | DAVIES–BOULDIN ↓ | CALINSKI–HARABASZ ↑ | INERTIA* | NHIỄU TB | THỜI GIAN (GIÂY) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DBSCAN | Z-score | 0,051 | 0,799 | 14,606 | 511,687 | 31,4 | 0,103 |
| K-Means | Min-Max | **0,329** | 1,090 | 88,696 | 19,640 | 0,0 | 0,439 |
| K-Means | Raw | 0,323 | **1,059** | **148,857** | 18,514 | 0,0 | 0,552 |
| K-Means | Z-score | 0,318 | 1,143 | 79,682 | 459,727 | 0,0 | 0,370 |
| Ward | Z-score | 0,287 | 1,156 | 66,720 | 501,306 | 0,0 | 1,184 |



↑ là metric thường ưu tiên lớn hơn; ↓ là metric thường ưu tiên nhỏ hơn. * Inertia phụ thuộc thang đo, không dùng cột này để kết luận Min-Max/Raw tốt hơn Z-score hay ngược lại. Các metric DBSCAN cần được hiểu cùng trạng thái đủ cụm và số điểm nhiễu; chúng có thể chỉ được tính trên phần điểm được gán cụm.


### Nhận xét kết quả


K-Means/Min-Max đạt Silhouette trung bình cao nhất (0,329), nhỉnh hơn Raw (0,323) và Z-score (0,318). K-Means/Raw có Davies–Bouldin thấp nhất (1,059) và Calinski–Harabasz cao nhất (148,857). Các metric bổ sung góc nhìn khác nhau và phụ thuộc cách biểu diễn, vì vậy không tạo thành một thứ hạng tuyệt đối duy nhất. Ward/Z-score có Silhouette trung bình 0,287.


DBSCAN có Silhouette trung bình 0,051, Calinski–Harabasz trung bình 14,606 và 31,4 điểm nhiễu trung bình. Cùng với việc chỉ 1–5 trong 12 tổ hợp mỗi năm đủ điều kiện tính metric, kết quả cho thấy DBSCAN không tạo phân hoạch phù hợp bằng các cấu hình K-Means trong phạm vi tham số đã khảo sát. DBSCAN có thời gian trung bình thấp nhất, nhưng tốc độ không khắc phục hạn chế về cấu trúc cụm và nhiễu.


### Đối chứng k=3 và hậu kiểm điểm hạnh phúc


Vì k*=3 trong cả năm năm, đối chứng k=3 trùng số cụm tối ưu; ARI giữa hai cấu hình bằng 1,0 ở cả 10 trường hợp (hai thuật toán × năm năm). Đây là kiểm tra tính nhất quán, không phải so sánh độc lập giữa hai giá trị k khác nhau.


happiness_score được dùng để hậu kiểm sau khi gán cụm, không tham gia huấn luyện. Chênh lệch giữa điểm trung bình cụm cao nhất và thấp nhất nằm trong khoảng 2,465–2,943 điểm ở các kết quả đối chứng. Nhãn cụm 0, 1, 2 chỉ là mã định danh có thể đổi giữa thuật toán/năm; nên diễn giải bằng điểm trung bình và profile đặc trưng, không gán cùng ý nghĩa cho cùng số nhãn.


### Kết luận phần thực nghiệm


Trong phạm vi dữ liệu và thiết lập đã khảo sát, k=3 nhất quán cho K-Means qua 2015–2019. K-Means/Min-Max dẫn đầu theo Silhouette trung bình; Raw dẫn đầu theo Davies–Bouldin và Calinski–Harabasz. DBSCAN không phải lựa chọn ưu tiên trong vùng tham số đã quét do số cấu hình hợp lệ ít, Silhouette thấp và số điểm nhiễu đáng kể. Các kết luận này chỉ áp dụng cho sáu đặc trưng, dữ liệu và dải tham số của thí nghiệm.


## Diễn giải chân dung cụm


Kết quả đối chứng k=3 cho thấy ba cụm có mức điểm happiness_score trung bình khác nhau rõ rệt ở cả K-Means và Ward trong năm năm. Với K-Means, điểm trung bình cụm thấp nhất nằm trong khoảng 4,096–4,263; cụm trung bình khoảng 5,577–5,608; cụm cao nhất khoảng 6,728–6,846. Như vậy, các cụm tạo từ sáu đặc trưng cũng phân hóa theo điểm hạnh phúc khi hậu kiểm. Điểm hạnh phúc không được dùng để tạo cụm.


→ Không nên gọi một cụm là “cụm 0 hạnh phúc cao” xuyên suốt các năm: nhãn là mã tùy ý và thay đổi vị trí giữa các năm. Chẳng hạn, cụm điểm cao nhất của K-Means lần lượt mang nhãn 2, 0, 2, 1 và 0 từ 2015 đến 2019. Vì vậy cần xác định mức thấp/trung bình/cao từ giá trị trung bình, rồi dùng trung bình sáu đặc trưng để giải thích profile thực chất của mỗi nhóm.


## So sánh giữa các năm và dịch chuyển cụm


Số cụm tối ưu theo Silhouette là k*=3 trong cả năm năm. Silhouette tại cấu hình này tăng từ 0,293 năm 2015 lên 0,344 năm 2019. Kết quả cho thấy phân hoạch ba cụm duy trì được mức tách biệt tương đối ổn định theo thiết kế, với Silhouette cao hơn ở các năm cuối của giai đoạn.


Tuy nhiên, mỗi năm được gom cụm độc lập nên không thể so trực tiếp nhãn cụm giữa hai năm. Nhóm đã thực hiện thuật toán ghép tham lam các cụm liên năm theo khoảng cách tâm cụm Euclid nhỏ nhất kết hợp thứ tự điểm hạnh phúc (kết quả lưu tại reports/tables/cross_year_matching.csv). Dựa trên ánh xạ này, nhóm đã xây dựng bảng theo dõi dịch chuyển cụm của 156 quốc gia qua 5 năm (data/processed/country_cluster_shift.csv). Kết quả cho thấy đại đa số quốc gia giữ vững phân nhóm ổn định qua 5 năm, trong khi một số quốc gia ghi nhận sự cải thiện hoặc sụt giảm phân hạng phù hợp với biến động kinh tế - xã hội thực tế.


## Ứng dụng phần mềm Demo Streamlit


Theo phần kiểm tra app đã lưu trong notebook, bản app/app.py hiện có giao diện chọn năm, thuật toán và k, cùng các tab tổng quan, bản đồ và tra cứu. Nhưng phần hiển thị vẫn là bản khung: biểu đồ radar dùng số minh họa cố định, tab bản đồ chưa có kết quả, và tra cứu quốc gia chưa trả về phân cụm thực tế. App chưa thể hiện rằng thay đổi lựa chọn sẽ chạy lại mô hình và cập nhật kết quả.


Vì vậy, nếu mô tả đúng trạng thái đã kiểm tra, hãy gọi đây là bản mẫu giao diện cho demo, chưa phải ứng dụng phân tích tương tác hoàn chỉnh. Chỉ mô tả các chức năng như đã hoàn thành sau khi kiểm tra phiên bản app mới nhất cho thấy dữ liệu và API gom cụm được kết nối thực sự.


## Kết luận chung và hướng phát triển


Trong phạm vi sáu đặc trưng và dữ liệu 2015–2019, khảo sát chọn k=3 cho cả năm năm. K-Means/Min-Max có Silhouette trung bình cao nhất trong các cấu hình so sánh (0,329), còn K-Means/Raw có Davies–Bouldin thấp nhất (1,059) và Calinski–Harabasz cao nhất (148,857). DBSCAN có Silhouette trung bình 0,051 và trung bình 31,4 điểm nhiễu; vì vậy cần xem cả metric lẫn số điểm nhiễu khi đánh giá, không chỉ dựa vào một chỉ số.


Kết quả cũng có giới hạn: các năm được phân tích riêng nên chưa đủ để kết luận về sự dịch chuyển của từng quốc gia nếu thiếu bảng ghép cụm; một số dữ liệu bị thiếu, như trường tham nhũng của United Arab Emirates năm 2018; và K-Means/DBSCAN phụ thuộc vào giả định hoặc tham số của thuật toán. Phân tích gom cụm cho thấy sự tương đồng và khác biệt trong dữ liệu, không chứng minh các yếu tố gây ra mức hạnh phúc.


Hướng phát triển phù hợp là bổ sung bảng profile sáu đặc trưng theo cụm cho đủ năm năm, hoàn tất ghép cụm và bảng dịch chuyển quốc gia, khảo sát thêm cách xử lý dữ liệu thiếu và mở rộng so sánh thuật toán. Demo cũng cần nối các lựa chọn trên giao diện với dữ liệu và mô hình để hiển thị kết quả thực tế.
