"""
export_to_sqlite.py - Chuyen toan bo du lieu tu SQL Server sang SQLite
"""
import os
import sys
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# 1. Ket noi SQL Server qua Django hien tai de lay du lieu
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaubong.settings')
import django
django.setup()

from shop.models import Category, Product, ShopUser, Order, OrderDetail

print("--- 1. DOC DU LIEU TU SQL SERVER ---")
cats = list(Category.objects.all().values())
prods = list(Product.objects.all().values())
users = list(ShopUser.objects.all().values())
orders = list(Order.objects.all().values())
details = list(OrderDetail.objects.all().values())

print(f" > Categories: {len(cats)}")
print(f" > Products: {len(prods)}")
print(f" > Users: {len(users)}")
print(f" > Orders: {len(orders)}")
print(f" > OrderDetails: {len(details)}")

# 2. Tao file db.sqlite3 va khoi tao schema
sqlite_path = BASE_DIR / 'db.sqlite3'
if sqlite_path.exists():
    sqlite_path.unlink()

conn = sqlite3.connect(sqlite_path)
cursor = conn.cursor()

# Tao bang Categories
cursor.execute('''
CREATE TABLE Categories (
    CategoryId INTEGER PRIMARY KEY AUTOINCREMENT,
    CategoryName TEXT NOT NULL,
    Description TEXT
);
''')

# Tao bang Products
cursor.execute('''
CREATE TABLE Products (
    ProductId INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductName TEXT NOT NULL,
    CategoryId INTEGER NOT NULL,
    BasePrice REAL NOT NULL DEFAULT 0,
    ImageUrl TEXT,
    Material TEXT,
    SizeOptions TEXT,
    Description TEXT,
    Stock INTEGER DEFAULT 0,
    IsAvailable INTEGER DEFAULT 1,
    CreatedAt TEXT,
    FOREIGN KEY (CategoryId) REFERENCES Categories (CategoryId)
);
''')

# Tao bang Users
cursor.execute('''
CREATE TABLE Users (
    UserId INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT UNIQUE NOT NULL,
    Password TEXT NOT NULL,
    FullName TEXT NOT NULL,
    Email TEXT,
    Phone TEXT,
    Address TEXT,
    Role TEXT DEFAULT 'Customer',
    CreatedAt TEXT
);
''')

# Tao bang Orders
cursor.execute('''
CREATE TABLE Orders (
    OrderId INTEGER PRIMARY KEY AUTOINCREMENT,
    OrderCode TEXT NOT NULL,
    CustomerName TEXT NOT NULL,
    Phone TEXT NOT NULL,
    Address TEXT NOT NULL,
    OrderDate TEXT,
    TotalAmount REAL DEFAULT 0,
    PaymentMethod TEXT DEFAULT 'COD',
    IsGiftWrapped INTEGER DEFAULT 0,
    GiftMessage TEXT,
    Status TEXT DEFAULT 'Chờ xác nhận'
);
''')

# Tao bang OrderDetails
cursor.execute('''
CREATE TABLE OrderDetails (
    OrderDetailId INTEGER PRIMARY KEY AUTOINCREMENT,
    OrderId INTEGER NOT NULL,
    ProductId INTEGER NOT NULL,
    ProductName TEXT NOT NULL,
    ImageUrl TEXT,
    SelectedSize TEXT NOT NULL,
    Quantity INTEGER DEFAULT 1,
    UnitPrice REAL DEFAULT 0,
    FOREIGN KEY (OrderId) REFERENCES Orders (OrderId),
    FOREIGN KEY (ProductId) REFERENCES Products (ProductId)
);
''')

print("\n--- 2. CHEN DU LIEU VAO SQLITE ---")
for c in cats:
    cursor.execute(
        "INSERT INTO Categories (CategoryId, CategoryName, Description) VALUES (?, ?, ?)",
        (c['categoryid'], c['categoryname'], c['description'])
    )

for p in prods:
    cursor.execute(
        """INSERT INTO Products (ProductId, ProductName, CategoryId, BasePrice, ImageUrl, Material, SizeOptions, Description, Stock, IsAvailable, CreatedAt)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (p['productid'], p['productname'], p['category_id'], float(p['baseprice']), p['imageurl'], p['material'], p['sizeoptions'], p['description'], p['stock'], 1 if p['isavailable'] else 0, str(p['createdat']))
    )

for u in users:
    cursor.execute(
        """INSERT INTO Users (UserId, Username, Password, FullName, Email, Phone, Address, Role, CreatedAt)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (u['userid'], u['username'], u['password'], u['fullname'], u['email'], u['phone'], u['address'], u['role'], str(u['createdat']))
    )

for o in orders:
    cursor.execute(
        """INSERT INTO Orders (OrderId, OrderCode, CustomerName, Phone, Address, OrderDate, TotalAmount, PaymentMethod, IsGiftWrapped, GiftMessage, Status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (o['orderid'], o['ordercode'], o['customername'], o['phone'], o['address'], str(o['orderdate']), float(o['totalamount']), o['paymentmethod'], 1 if o['isgiftwrapped'] else 0, o['giftmessage'], o['status'])
    )

for d in details:
    cursor.execute(
        """INSERT INTO OrderDetails (OrderDetailId, OrderId, ProductId, ProductName, ImageUrl, SelectedSize, Quantity, UnitPrice)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (d['orderdetailid'], d['order_id'], d['product_id'], d['productname'], d['imageurl'], d['selectedsize'], d['quantity'], float(d['unitprice']))
    )

conn.commit()
conn.close()
print(" [SUCCESS] Da sao chep toan bo du lieu sang db.sqlite3 thanh cong!")
