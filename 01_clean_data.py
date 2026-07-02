# ==============================================================================
# DHV301 Group Project - Option A (Retail / Revenue)
# Script: 01_clean_data.py
# Vai tro: Data Preparation Lead
#
# NGUON DU LIEU: UCI Machine Learning Repository - "Online Retail" Dataset
#   Tac gia goc: Dr. Daqing Chen (2015)
#   Trang chinh thuc: https://archive.ics.uci.edu/dataset/352/online+retail
#   Trich dan: Chen, D. (2015). Online Retail [Dataset]. UCI ML Repository.
#              https://doi.org/10.24432/C5BW33
#   Day la giao dich THAT cua 1 cong ty ban le online tai Anh, 12/2010-12/2011.
#   File goc day du: 541,909 dong.
#
# PHUONG PHAP LAY MAU (DE TAO Retail_Transactions_raw.csv):
#   df_full = pd.read_csv("online_retail_full.csv", encoding="ISO-8859-1")
#   sample  = df_full.sample(n=2500, random_state=42).sort_index()
#   -> Random sampling co seed co dinh (random_state=42): tai lap 100%,
#      dong thoi dai dien tot hon cho toan bo 13 thang du lieu (so voi cach
#      lay N dong dau tien truoc day, von chi phan anh 2 ngay dau tien).
#
# CACH CHAY:
#   1. Dat file Retail_Transactions_raw.csv vao cung thu muc voi script nay.
#   2. Mo terminal tai thu muc DHV_Groupproject, chay:
#        python 01_clean_data.py
#   3. Ket qua duoc ghi vao thu muc con "clean/"
# ==============================================================================

import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
RAW_FILE = BASE_DIR / "Retail_Transactions_raw.csv"
CLEAN_DIR = BASE_DIR / "clean"
CLEAN_DIR.mkdir(exist_ok=True)

LOG_LINES = []

def log(msg):
    print(msg)
    LOG_LINES.append(str(msg))

log(f"=== BAT DAU LAM SACH DU LIEU | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")

# ------------------------------------------------------------------------
# 1. DOC DU LIEU THO
# ------------------------------------------------------------------------
df = pd.read_csv(RAW_FILE, encoding="ISO-8859-1")
log(f"Da doc: {df.shape[0]} dong, {df.shape[1]} cot\n")

# ------------------------------------------------------------------------
# 2. KIEM TRA CHAT LUONG DU LIEU (TRUOC KHI LAM SACH)
# ------------------------------------------------------------------------
log("--- Kiem tra chat luong du lieu THO ---")
log(f"Gia tri thieu theo cot:\n{df.isnull().sum()}")

n_dup = df.duplicated().sum()
log(f"So dong trung lap hoan toan: {n_dup}")

n_cancel = df['InvoiceNo'].astype(str).str.startswith('C').sum()
log(f"So giao dich la don huy (InvoiceNo bat dau bang 'C'): {n_cancel}")

df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce')
n_neg_qty = (df['Quantity'] < 0).sum()
n_bad_price = (df['UnitPrice'] <= 0).sum()
log(f"So dong Quantity am (thuong la hang tra lai): {n_neg_qty}")
log(f"So dong UnitPrice <= 0 (bat thuong): {n_bad_price}")
log("")

# ------------------------------------------------------------------------
# 3. LAM SACH
# ------------------------------------------------------------------------
clean = df.copy()

clean['InvoiceDate'] = pd.to_datetime(clean['InvoiceDate'], format='mixed', errors='coerce')
clean['Description'] = clean['Description'].astype(str).str.strip()
clean['Country'] = clean['Country'].astype(str).str.strip()

# Danh dau don huy thay vi xoa (giu nguyen thong tin nghiep vu)
clean['IsCancelled'] = clean['InvoiceNo'].astype(str).str.startswith('C')

before = len(clean)
clean = clean.drop_duplicates()
log(f"Da loai bo {before - len(clean)} dong trung lap")

# UnitPrice <= 0 CHI loai neu khong phai don huy (loi nhap lieu thuc su)
before = len(clean)
clean = clean[~((clean['UnitPrice'] <= 0) & (~clean['IsCancelled']))]
log(f"Da loai bo {before - len(clean)} dong UnitPrice<=0 khong phai don huy")

clean['Revenue'] = clean['Quantity'] * clean['UnitPrice']

clean['Year'] = clean['InvoiceDate'].dt.year
clean['Month'] = clean['InvoiceDate'].dt.month
clean['YearMonth'] = clean['InvoiceDate'].dt.to_period('M').astype(str)

log(f"[Transactions] Hoan tat lam sach -> {clean.shape}\n")

# ------------------------------------------------------------------------
# 4. TACH THANH STAR SCHEMA (1 Fact + 2 Dimension)
# ------------------------------------------------------------------------
products = (
    clean.dropna(subset=['StockCode'])
    .groupby('StockCode', as_index=False)['Description']
    .agg(lambda x: x.mode().iat[0] if not x.mode().empty else x.iloc[0])
)
log(f"[Products] So san pham duy nhat: {products.shape[0]}")

customers = (
    clean.dropna(subset=['CustomerID'])
    .drop_duplicates(subset=['CustomerID'])[['CustomerID', 'Country']]
    .reset_index(drop=True)
)
n_missing_cust = clean['CustomerID'].isnull().sum()
log(f"[Customers] So khach hang duy nhat co CustomerID: {customers.shape[0]}")
log(f"[Customers] So giao dich KHONG co CustomerID (giu nguyen trong Fact): {n_missing_cust}")

transactions = clean[[
    'InvoiceNo', 'StockCode', 'CustomerID', 'InvoiceDate', 'Year', 'Month',
    'YearMonth', 'Quantity', 'UnitPrice', 'Revenue', 'IsCancelled', 'Country'
]].reset_index(drop=True)

# ------------------------------------------------------------------------
# 5. XUAT DU LIEU SACH
# ------------------------------------------------------------------------
transactions.to_csv(CLEAN_DIR / "Transactions_clean.csv", index=False)
products.to_csv(CLEAN_DIR / "Products_clean.csv", index=False)
customers.to_csv(CLEAN_DIR / "Customers_clean.csv", index=False)

log(f"\nDa xuat 3 file sach vao: {CLEAN_DIR}")
log(f"  Transactions_clean.csv : {transactions.shape}")
log(f"  Products_clean.csv     : {products.shape}")
log(f"  Customers_clean.csv    : {customers.shape}")

log(f"\n=== HOAN TAT | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")

with open(CLEAN_DIR / "cleaning_log.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(LOG_LINES))

print(f"\n>>> Log day du da duoc luu tai: {CLEAN_DIR / 'cleaning_log.txt'}")
