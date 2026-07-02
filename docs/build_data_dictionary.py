import pandas as pd

rows = [
    # --- Transactions_clean (Fact) ---
    ("Transactions_clean", "InvoiceNo", "string", "Ma hoa don, 6 chu so. Bat dau bang 'C' = don huy"),
    ("Transactions_clean", "StockCode", "string", "Khoa ngoai -> Products_clean.StockCode"),
    ("Transactions_clean", "CustomerID", "string (co the rong)", "Khoa ngoai -> Customers_clean.CustomerID. ~20% giao dich khong co (dac diem that cua nguon du lieu goc)"),
    ("Transactions_clean", "InvoiceDate", "datetime", "Ngay gio giao dich"),
    ("Transactions_clean", "Year", "integer", "[Cot phai sinh] Nam, trich tu InvoiceDate"),
    ("Transactions_clean", "Month", "integer", "[Cot phai sinh] Thang, trich tu InvoiceDate"),
    ("Transactions_clean", "YearMonth", "string", "[Cot phai sinh] Nam-Thang (YYYY-MM), phuc vu MoM trong DAX"),
    ("Transactions_clean", "Quantity", "integer", "So luong san pham. Gia tri am = hang tra lai (don huy)"),
    ("Transactions_clean", "UnitPrice", "float", "Don gia (bang Anh - GBP)"),
    ("Transactions_clean", "Revenue", "float", "[Cot phai sinh] = Quantity x UnitPrice"),
    ("Transactions_clean", "IsCancelled", "boolean", "[Cot phai sinh] True neu InvoiceNo bat dau bang 'C'"),
    ("Transactions_clean", "Country", "string", "Quoc gia cua khach hang dat don"),

    # --- Products_clean (Dimension) ---
    ("Products_clean", "StockCode", "string", "Ma san pham duy nhat (khoa chinh)"),
    ("Products_clean", "Description", "string", "Ten/mo ta san pham (lay gia tri pho bien nhat neu StockCode co nhieu mo ta khac nhau)"),

    # --- Customers_clean (Dimension) ---
    ("Customers_clean", "CustomerID", "string", "Ma khach hang duy nhat (khoa chinh). CHI chua khach hang co ID (da loai gia tri rong)"),
    ("Customers_clean", "Country", "string", "Quoc gia cua khach hang"),
]

dd = pd.DataFrame(rows, columns=["Bang (Table)", "Cot (Column)", "Kieu du lieu (Type)", "Mo ta (Description)"])

meta = pd.DataFrame([
    ["Ten du an", "DHV301 - Option A: Ban le / Doanh thu"],
    ["Nguon du lieu goc", "Online Retail Dataset - UCI Machine Learning Repository"],
    ["Tac gia goc", "Dr. Daqing Chen (2015)"],
    ["Trang chinh thuc", "https://archive.ics.uci.edu/dataset/352/online+retail"],
    ["Trich dan", "Chen, D. (2015). Online Retail [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33"],
    ["Loai du lieu", "Giao dich THAT cua 1 cong ty ban le online tai Anh (2010-2011), khong phai du lieu mo phong"],
    ["Cau truc", "Ban goc la 1 bang phang -> da tach thanh star schema: 1 Fact (Transactions) + 2 Dimension (Products, Customers)"],
    ["So dong subset dung trong du an", "2500 dong, lay bang random sampling (pandas .sample(n=2500, random_state=42)) tren toan bo 541,909 dong goc"],
    ["Ly do chon random sampling + seed co dinh", "Dam bao mau dai dien cho toan bo 13 thang du lieu (thay vi chi lay N dong dau file), dong thoi van tai lap 100% nho seed=42"],
    ["Quy trinh lam sach", "Xem chi tiet trong 01_clean_data.py va clean/cleaning_log.txt"],
    ["Nguoi phu trach", "Data Preparation Lead"],
    ["Ngay tao", "01/07/2026"],
], columns=["Thong tin", "Gia tri"])

with pd.ExcelWriter("/home/claude/DHV_Groupproject/docs/data_dictionary.xlsx", engine="openpyxl") as writer:
    meta.to_excel(writer, sheet_name="Thong_tin_chung", index=False)
    dd.to_excel(writer, sheet_name="Data_Dictionary", index=False)
    for sheet, df_ in [("Thong_tin_chung", meta), ("Data_Dictionary", dd)]:
        ws = writer.sheets[sheet]
        for i, col in enumerate(df_.columns):
            width = max(df_[col].astype(str).map(len).max(), len(col)) + 4
            ws.column_dimensions[chr(65 + i)].width = min(width, 70)

print("Data dictionary created.")
print(dd)
