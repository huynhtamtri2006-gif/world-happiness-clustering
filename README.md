# Phân nhóm quốc gia theo các yếu tố tạo nên mức độ hạnh phúc (World Happiness Report)

Đồ án môn **Khai thác dữ liệu** — Đề tài 16 — Nhóm 12.
Chuyên ngành Khoa học dữ liệu, năm 3.

## Nhóm thực hiện

| STT | Mã số SV | Họ và tên | Vai trò | Tỷ lệ đóng góp |
|:---:|:---:|:---|:---:|:---:|
| 1 | 2045240326 | Hà Mạnh Trường | Nhóm trưởng | 34% |
| 2 | 2045240315 | Huỳnh Tâm Trí | Thành viên | 33% |
| 3 | 2045240325 | Ngô Quang Trung | Thành viên | 33% |

## Nội dung

Dự án gom cụm các quốc gia dựa trên sáu yếu tố cơ sở của World Happiness Report giai đoạn 2015-2019:
GDP per capita, Social support, Healthy life expectancy, Freedom, Generosity và Perceptions of corruption.

Điểm hạnh phúc (`Happiness Score`) và thứ hạng hạnh phúc (`Happiness Rank`) **không** được đưa vào ma trận
đặc trưng dùng để gom cụm; hai thuộc tính này chỉ dùng để hậu kiểm sau khi đã gom cụm.

Các thuật toán gom cụm (K-Means, phân cấp Ward, DBSCAN), phần giảm chiều PCA và các độ đo đánh giá
(Silhouette, Davies-Bouldin, Calinski-Harabasz, Adjusted Rand Index) đều do nhóm tự cài đặt bằng
`numpy`/`pandas`. Thư viện `scikit-learn` chỉ được dùng trong script kiểm chứng để đối chiếu kết quả,
không dùng trong notebook hay ứng dụng demo.

## Cấu trúc thư mục

```text
data_mining/
├── data/
│   ├── raw/            # dữ liệu gốc 2015.csv ... 2019.csv
│   ├── interim/        # bảng trung gian 5 năm do notebook 01 sinh ra
│   └── processed/      # kết quả gom cụm, chân dung cụm, bảng dịch chuyển cụm
├── notebooks/          # 01 hiểu dữ liệu -> 02 EDA -> 03 gom cụm -> 04 diễn giải
├── src/
│   ├── data/           # nạp và chuẩn hóa dữ liệu
│   ├── features/       # chuẩn hóa thang đo và giảm chiều PCA
│   ├── models/         # K-Means, phân cấp Ward, DBSCAN và các độ đo
│   └── visualization/  # hàm vẽ biểu đồ cho báo cáo
├── scripts/            # script kiểm chứng thuật toán tự viết
├── app/                # ứng dụng demo Streamlit
├── models/             # tâm cụm, tham số chuẩn hóa và metric (JSON)
├── reports/
│   ├── figures/        # hình 300 DPI chèn vào báo cáo
│   ├── tables/         # bảng số liệu dùng làm nguồn cho báo cáo
│   └── final_report/   # bản gốc markdown, script sinh Word, báo cáo và slide
└── docs/               # tài liệu tham khảo, đề cương môn học, ADR
```

## Cài đặt

Khuyến nghị Python 3.12:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows PowerShell
source .venv/bin/activate          # Linux / macOS
pip install --upgrade pip
pip install -r requirements.txt
```

## Thứ tự chạy

1. Chạy lần lượt bốn notebook trong `notebooks/` theo thứ tự 01 → 04 (notebook sau đọc kết quả của notebook trước).
2. Kiểm chứng thuật toán tự viết: `python scripts/verify_scratch_implementations.py`.
3. Mở ứng dụng demo: `streamlit run app/app.py` (mặc định tại `http://localhost:8501`).
4. Sinh lại báo cáo Word: `python reports/final_report/build_report.py`.

## Dữ liệu

- Nguồn: [World Happiness Report trên Kaggle](https://www.kaggle.com/datasets/synful/world-happiness-report),
  tham chiếu chính thức tại [worldhappiness.report](https://worldhappiness.report/).
- Năm tệp dữ liệu gốc nằm trong `data/raw/`; bảng dữ liệu trung gian dùng chung cho cả 5 năm do
  notebook 01 sinh ra ở `data/interim/happiness_merged.csv`.
- Lưu ý đã kiểm tra: năm 2018 thiếu giá trị `Perceptions of corruption` ở United Arab Emirates;
  cột `Region` chỉ có ở hai năm 2015-2016; một số quốc gia đổi tên giữa các năm nên đã được chuẩn hóa.

## Kết quả chính

Phần này sẽ được cập nhật sau khi hoàn thành notebook 03 và 04 (số cụm tối ưu của từng năm, so sánh
các cấu hình gom cụm, chân dung từng nhóm quốc gia và mức phân hóa điểm hạnh phúc giữa các nhóm).
