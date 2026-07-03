# BI Dashboard Lead — Gói bàn giao (DHV301, Option A)

Phần việc của vai trò **BI Dashboard Lead**: Power BI model + DAX + UX dashboard.
Nối tiếp dữ liệu sạch (`../clean/`) và báo cáo EDA (`../EDA_Visualization_Report.docx`).

## Nội dung thư mục

| File | Mô tả | Dùng để |
|---|---|---|
| `KPI_DAX_Documentation.docx` | Tài liệu chính: giải thích KPI, hướng dẫn dựng model, thiết kế UX, kiểm thử, phụ lục số liệu | Nộp bài + đọc hiểu |
| `DAX_Measures.txt` | Toàn bộ code DAX (bảng Dim_Date + 2 cột tính + 15 measure) | Copy-paste thẳng vào Power BI |
| `assets/star_schema.png` | Sơ đồ Star Schema tham chiếu | Nhúng tài liệu / đối chiếu khi dựng model |
| `assets/dashboard_wireframe.png` | Wireframe layout dashboard 1 trang | Tham chiếu khi thiết kế UX |

## Cần bạn tự làm trong Power BI

1. Import 3 CSV trong `../clean/` → làm sạch kiểu dữ liệu (xem Mục 3 tài liệu).
2. Chạy DAX tạo `Dim_Date`, 2 cột `OrderDate`/`Region`, thiết lập 3 quan hệ.
3. Dán 15 measure từ `DAX_Measures.txt`.
4. Dựng dashboard theo wireframe (Mục 6) → xuất **file PBIX**.
5. Chụp **model screenshot** (Mục 7).

## Đối chiếu yêu cầu đề bài

- ✅ ≥ 5 DAX/KPI → **15 measure**
- ✅ ≥ 2 DAX nâng cao → **5** (MoM Growth %, Revenue YTD, RANKX, Pareto TOPN, SWITCH)
- ✅ KPI có giải thích + kiểm thử slicer (Mục 4 & 5)
- ✅ Dashboard 1 trang, ≤ 6–7 visual, hiểu trong 10 giây (Mục 6)

## Giá trị baseline để kiểm tra (không lọc slicer)

Total Revenue = **£43.408,87** · Total Orders = **1.994** · % Cancelled = **2,35%** · AOV = **£21,77** (theo đơn).
Xem đầy đủ ở Phụ lục Mục 8 của tài liệu.
