# World Happiness Clustering Context

Ngữ cảnh nghiệp vụ cho Đề tài 16: Phân nhóm các quốc gia dựa trên các chỉ số hạnh phúc từ báo cáo World Happiness Report (WHR).

## Core Factors (6 Đặc trưng cơ sở)

Ma trận đặc trưng $X$ dùng để gom cụm hoàn toàn chỉ được tạo thành từ 6 yếu tố cơ sở này:

**GDP per Capita**:
Mức độ đóng góp của thu nhập bình quân đầu người vào sự hạnh phúc của quốc gia.
_Avoid_: Economic score, Income, GDP thô

**Social Support**:
Mức độ tương trợ xã hội khi người dân gặp khó khăn (tương đương Family ở báo cáo các năm cũ).
_Avoid_: Family support, Social welfare

**Healthy Life Expectancy**:
Tuổi thọ trung bình khỏe mạnh dự tính của người dân tại quốc gia.
_Avoid_: Health score, Life span, Tuổi thọ tổng quát

**Freedom**:
Mức độ tự do của người dân trong việc đưa ra các quyết định và lựa chọn cuộc sống.
_Avoid_: Liberty, Democracy, Freedom of speech

**Generosity**:
Mức độ đóng góp thiện nguyện và sự hào phóng của người dân đối với cộng đồng.
_Avoid_: Charity score, Altruism

**Perceptions of Corruption**:
Mức độ niềm tin của người dân vào sự trong sạch của chính phủ và doanh nghiệp (tham nhũng càng thấp thì chỉ số càng cao).
_Avoid_: Trust, Corruption rate, Government integrity

---

## Evaluation & Invariants (Thuật ngữ đánh giá & Ranh giới)

**Happiness Score**:
Điểm số hạnh phúc tổng thể (hoặc Ladder Score) do người dân tự đánh giá trên thang điểm từ 0 đến 10. Thuộc tính này là biến mục tiêu dùng ĐỘC LẬP để hậu kiểm và đối chiếu ở bước diễn giải tri thức.
_Avoid_: Feature gom cụm, Biến đầu vào, Thuộc tính X

**Happiness Rank**:
Thứ hạng hạnh phúc của các quốc gia trên toàn cầu.
_Avoid_: Rank feature, Cột gom cụm

**Cluster Profile**:
Bức chân dung định tính của từng nhóm quốc gia sau khi gom cụm (ví dụ: nhóm Phát triển toàn diện, nhóm Đang phát triển phụ thuộc kinh tế, nhóm Kém phát triển).
_Avoid_: Cluster label, Nhóm số nguyên thuần túy

---

## Experiment Scope (Phạm vi thực nghiệm)

**Experiment Year**:
Một trong năm năm 2015-2019. Mỗi năm được gom cụm độc lập và là một đơn vị báo cáo riêng, sau đó mới so sánh xu hướng giữa các năm.
_Avoid_: Gộp 5 năm thành một lần chạy, dữ liệu trộn năm, pooled dataset

**Clustering Configuration**:
Cặp (thuật toán, cách chuẩn hóa dữ liệu) kèm tham số tương ứng, ví dụ K-Means với Z-score, phân cấp Ward với Z-score, DBSCAN với Z-score.
_Avoid_: Model, mô hình, pipeline

**Optimal k (Số cụm tối ưu)**:
Số cụm được chọn cho từng năm bằng phương pháp khuỷu tay và hệ số Silhouette. Đây là kết quả chính của báo cáo.
_Avoid_: k mặc định, k chuẩn

**Contrast Configuration (Cấu hình đối chứng k=3)**:
Cấu hình ba cụm dùng để so sánh cấu trúc phân nhóm giữa các năm trên cùng một số cụm.
_Avoid_: Baseline, k cố định

**Cluster Stability (Độ ổn định cụm)**:
Mức trùng khớp nhãn cụm khi chạy lại thuật toán với các seed khác nhau, đo bằng Adjusted Rand Index trên 10 seed. Chỉ áp dụng cho thuật toán có khởi tạo ngẫu nhiên; thuật toán tất định được ghi nhận 1.0 kèm giải thích.
_Avoid_: Độ chính xác, accuracy

**Cross-year Cluster Matching (Ghép cụm liên năm)**:
Việc gán cặp cụm giữa hai năm liền kề theo khoảng cách tâm cụm nhỏ nhất, hoà thì xét điểm hạnh phúc trung bình, để có thể so sánh xu hướng giữa các năm.
_Avoid_: Cluster ID, đánh số cụm cố định

**Country Cluster Shift (Bảng dịch chuyển cụm)**:
Bảng theo dõi cụm của từng quốc gia qua năm năm, dùng để nhận diện quốc gia đổi nhóm.
_Avoid_: Bảng theo dõi quốc gia, lịch sử nhóm

---

## Methodology & Pipeline (Phương pháp luận)

**11-Step Pipeline**:
Chu trình khai phá dữ liệu 11 bước bắt buộc theo đề cương: (1) Xác định bài toán → (2) Hiểu dữ liệu → (3) Tiền xử lý → (4) Khám phá EDA → (5) Biến đổi đặc trưng → (6) Huấn luyện mô hình → (7) So sánh phương án → (8) Tinh chỉnh tham số → (9) Diễn giải tri thức → (10) Demo tương tác → (11) Đánh giá & Hạn chế.
_Avoid_: Ad-hoc analysis, Quy trình tự do

**From-Scratch Algorithm**:
Thuật toán do sinh viên tự code logic toán học từng bước bằng NumPy/Pandas cơ bản, không sử dụng API huấn luyện của thư viện Scikit-Learn. Theo ADR 0003, phạm vi này bao gồm K-Means, phân cấp Ward, DBSCAN, giảm chiều PCA và các độ đo Silhouette, Davies-Bouldin, Calinski-Harabasz, Adjusted Rand Index.
_Avoid_: Black-box model, Built-in clusterer

**Reproducible Path (Đường dẫn tái lập độc lập môi trường)**:
Cơ chế quản lý đường dẫn mã nguồn và dữ liệu dựa trên gốc thư mục dự án (`Path(__file__).resolve()`) hoặc đường dẫn tương đối, bảo đảm toàn bộ pipeline khai phá dữ liệu chạy lại được từ đầu trên bất kỳ máy cá nhân hay môi trường máy chấm nào mà không bị lỗi hardcoded paths.
_Avoid_: Đường dẫn tuyệt đối, C:\Users\..., /home/..., hardcoded path

---

## Submission & Quality Invariants (Quy chuẩn nộp bài & Kiểm soát chất lượng)

**Rubric 10.0 (Cơ cấu thang điểm toàn diện đồ án)**:
Cơ cấu điểm chính thức theo hướng dẫn của giảng viên: Báo cáo Word chiếm 6,0 điểm (3,0đ Nội dung 5 Chương + 3,0đ Hình thức chuẩn); Mã nguồn / Notebook Run All chiếm 2,0 điểm; Video báo cáo chiếm 2,0 điểm.
_Avoid_: Thang điểm cũ, chia điểm không rõ ràng

**Anti-AI Writing Style (Văn phong người thật thực chứng)**:
Quy chuẩn biên soạn báo cáo Word dựa 100% trên trải nghiệm nghiên cứu và thực nghiệm của sinh viên, đi thẳng vào bản chất kỹ thuật, số liệu cụ thể và quá trình thử-sai, loại bỏ hoàn toàn các câu từ sáo rỗng, phóng đại, từ nối công thức và cấu trúc nhân tạo của AI để tránh bị chế tài 0đ nội dung.
_Avoid_: Văn phong AI, câu từ sáo rỗng, triết lý thiếu số liệu

**Human-Centric Commit Protocol (Quy chuẩn Git commit thuần người thật)**:
Nguyên tắc cam kết thông điệp Git commit thuần túy phản ánh công việc kỹ thuật do chính các thành viên sinh viên (Trường, Trí, Trung) thực hiện; tuyệt đối không chứa bất kỳ từ khóa hay dấu vết nào của AI/bot (như `AI`, `bot`, `LLM`, `prompt`, `agent`, `tự động sinh`, `AI viết báo cáo`).
_Avoid_: Commit chứa từ khóa AI, bot commit, thông điệp tự động

**Video Presentation Rule (Quy tắc Video thuyết trình <= 12 phút)**:
Yêu cầu bắt buộc video báo cáo đồ án không vượt quá 12 phút, link truy cập trực tiếp không yêu cầu cấp quyền (được ghi tại trang bìa và phụ lục Word), và cả 3 thành viên đều tham gia trình bày với thời lượng cân bằng.
_Avoid_: Video quá 12 phút, link Google Drive riêng tư, chỉ một thành viên thuyết trình
