# DHV301 – Group Project | Option A: Bán lẻ / Doanh thu

## 1. Tổng quan dự án

Dự án phân tích hiệu suất bán hàng của một chuỗi bán lẻ, sử dụng dữ liệu giao dịch để xây dựng dashboard Power BI phục vụ ra quyết định về doanh thu, sản phẩm và khu vực.

| Thông tin | Chi tiết |
|---|---|
| Môn học | DHV301 |
| Chủ đề | Option A – Bán lẻ / Doanh thu |
| Vai trò trong nhóm (tài liệu này) | Data Preparation Lead |
| Ngày cập nhật | 01/07/2026 |

## 2. Nguồn dữ liệu

- **Tên dataset:** Online Retail Dataset
- **Nguồn:** UCI Machine Learning Repository — tác giả gốc: Dr. Daqing Chen (2015)
  https://archive.ics.uci.edu/dataset/352/online+retail
- **Trích dẫn:** Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33
- **Loại dữ liệu:** Giao dịch **thật** của một công ty bán lẻ online (đồ quà tặng) tại Anh, từ 01/12/2010 đến 09/12/2011 — không phải dữ liệu mô phỏng.
- **Quy mô đầy đủ:** 541,909 dòng.

### Phương pháp lấy mẫu (rút xuống 2500 dòng)

```python
df_full = pd.read_csv("online_retail_full.csv", encoding="ISO-8859-1")
sample  = df_full.sample(n=2500, random_state=42).sort_index()
```

- **Random sampling với seed cố định (`random_state=42`)** — chạy lại lệnh này bao nhiêu lần cũng cho ra đúng 2500 dòng giống hệt nhau → **tái lập 100%**.
- Khác với cách lấy N dòng đầu tiên (dễ bị thiên lệch vì dữ liệu gốc sắp theo thời gian), random sampling giúp mẫu **đại diện đều cho toàn bộ 13 tháng dữ liệu** (12/2010 – 12/2011), bao gồm cả giai đoạn cao điểm mùa lễ (tháng 11).
- Kiểm tra sau khi lấy mẫu: **cả 13/13 tháng** đều có mặt, **28 quốc gia** khác nhau — đủ đa dạng để tính MoM Growth, Ranking theo sản phẩm/quốc gia.

- **Cấu trúc:** Dữ liệu gốc là **1 bảng phẳng duy nhất** (InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country). Trong quá trình làm sạch, nhóm đã **tự tách thành star schema** (1 Fact + 2 Dimension) để phù hợp với Power BI Data Model.

| Bảng | Vai trò | Số dòng (sau khi làm sạch) |
|---|---|---|
| Transactions_clean | Fact – giao dịch bán hàng | 2,490 |
| Products_clean | Dimension – sản phẩm (StockCode → Description) | 1,345 |
| Customers_clean | Dimension – khách hàng đã xác định | 1,125 |

## 3. Cấu trúc thư mục

```
DHV_Groupproject/
├── README.md                      ← tài liệu này
├── Retail_Transactions_raw.csv    ← dữ liệu thô (raw), chưa qua xử lý, còn nguyên lỗi gốc
├── 01_clean_data.py               ← script làm sạch dữ liệu (Python)
├── clean/                         ← output sau khi chạy script
│   ├── Transactions_clean.csv
│   ├── Products_clean.csv
│   ├── Customers_clean.csv
│   └── cleaning_log.txt           ← nhật ký kiểm tra chất lượng dữ liệu
└── docs/
    ├── data_dictionary.xlsx       ← mô tả toàn bộ cột dữ liệu
    └── build_data_dictionary.py   ← script sinh ra data dictionary
```

## 4. Quy trình xử lý dữ liệu (Data Preparation Workflow)

Quy trình được thực hiện hoàn toàn bằng script (`01_clean_data.py`), không chỉnh sửa thủ công trên file gốc, đảm bảo **tính tái lập (reproducibility)**: chạy lại bao nhiêu lần cũng cho kết quả giống nhau.

**Các bước xử lý:**

1. **Đọc dữ liệu thô** — file `Retail_Transactions_raw.csv` (2500 dòng, đã lấy mẫu ngẫu nhiên có seed cố định như mô tả ở mục 2).
2. **Kiểm tra chất lượng dữ liệu thô:** phát hiện 651 giao dịch thiếu CustomerID (~26%, đặc điểm thật của nguồn dữ liệu gốc), 4 dòng thiếu Description, 49 đơn hủy (InvoiceNo bắt đầu bằng 'C'), 51 dòng Quantity âm (hàng trả lại), 10 dòng UnitPrice ≤ 0, 0 dòng trùng lặp.
3. **Chuẩn hóa kiểu dữ liệu:** chuyển InvoiceDate về datetime; chuẩn hóa chuỗi (Description, Country).
4. **Đánh dấu đơn hủy** bằng cột `IsCancelled` thay vì xóa — giữ nguyên giá trị nghiệp vụ.
5. **Loại bỏ 10 dòng có UnitPrice ≤ 0 và không phải đơn hủy** (lỗi nhập liệu thật sự).
6. **Tính Revenue** = Quantity × UnitPrice, và các cột thời gian `Year`, `Month`, `YearMonth` phục vụ MoM/YoY trong DAX.
7. **Tách thành star schema:** tách `Products_clean` (1,345 sản phẩm duy nhất) và `Customers_clean` (1,125 khách hàng đã xác định CustomerID), giữ `Transactions_clean` làm bảng Fact.
8. **Ghi log** toàn bộ kết quả kiểm tra vào `clean/cleaning_log.txt` làm minh chứng.

### Kết quả kiểm tra chất lượng (lần chạy gần nhất)

| Kiểm tra | Kết quả |
|---|---|
| Giá trị thiếu — CustomerID | 651 / 2500 (~26%, giữ nguyên trong Fact, không loại bỏ) |
| Giá trị thiếu — Description | 4 |
| Dòng trùng lặp | 0 |
| Đơn hủy (IsCancelled) | 49 |
| Quantity âm (hàng trả lại) | 51 |
| UnitPrice ≤ 0 đã loại bỏ | 10 |
| Số dòng Transactions sau cùng | 2,490 |
| Số tháng có mặt trong mẫu | 13/13 (bao phủ toàn bộ khung thời gian gốc) |
| Số quốc gia có mặt trong mẫu | 28 |

## 5. Cách chạy lại (Reproducibility)

```bash
cd DHV_Groupproject
python 01_clean_data.py
```

Yêu cầu: Python 3 với thư viện `pandas`. Script sẽ tự động tạo thư mục `clean/` nếu chưa tồn tại và ghi đè kết quả mới nhất.

## 6. Data Dictionary

Xem chi tiết đầy đủ tại `docs/data_dictionary.xlsx`, gồm 2 sheet:
- **Thong_tin_chung:** metadata của toàn bộ dataset.
- **Data_Dictionary:** mô tả từng cột trong 4 bảng (tên cột, kiểu dữ liệu, ý nghĩa), đánh dấu rõ cột nào là dữ liệu gốc và cột nào là phái sinh.

## 7. Giới hạn của dữ liệu

- Mẫu 2500 dòng là **random sample** từ 541,909 dòng gốc (không phải toàn bộ dữ liệu), nên các con số tổng (Total Revenue...) chỉ mang tính đại diện thống kê, không phản ánh doanh thu thực tế của công ty trong giai đoạn đó.
- ~26% giao dịch không có CustomerID (khách vãng lai hoặc dữ liệu gốc bị thiếu) — các phân tích theo khách hàng (ví dụ RFM) sẽ chỉ dựa trên 1,125 khách hàng đã xác định.
- Đơn vị tiền tệ là Bảng Anh (GBP), không phải VNĐ — cần lưu ý khi trình bày số liệu.
- Do lấy mẫu ngẫu nhiên trên toàn bộ 13 tháng, dữ liệu bị "ngắt quãng" theo ngày (không có đủ toàn bộ giao dịch của từng ngày cụ thể) — phù hợp cho phân tích xu hướng theo tháng/quý, nhưng không phù hợp nếu muốn phân tích chi tiết theo từng ngày/giờ.

## 8. Bước tiếp theo

Dữ liệu trong `clean/` đã sẵn sàng để:
- **EDA & Visualization Lead:** import vào notebook, vẽ ≥4 biểu đồ nháp cho Milestone 2 (gợi ý: doanh thu theo ngày, top sản phẩm theo Revenue, tỷ lệ đơn hủy, phân bố theo quốc gia).
- **BI Dashboard Lead:** import vào Power BI, thiết lập quan hệ giữa Transactions (fact) và Products/Customers (dimension), xây DAX measures (Total Revenue, % đơn hủy, Ranking sản phẩm, MoM Growth...).
