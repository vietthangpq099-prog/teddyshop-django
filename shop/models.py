"""
models.py - Các model tương ứng với bảng SQL Server hiện có
Dùng managed = False để Django không tự tạo/sửa bảng (bảng đã tồn tại)
"""
from django.db import models


class Category(models.Model):
    """Bảng dbo.Categories"""
    categoryid = models.AutoField(db_column='CategoryId', primary_key=True)
    categoryname = models.CharField(db_column='CategoryName', max_length=100)
    description = models.CharField(db_column='Description', max_length=300, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Categories'

    def __str__(self):
        return self.categoryname


class Product(models.Model):
    """Bảng dbo.Products"""
    productid = models.AutoField(db_column='ProductId', primary_key=True)
    productname = models.CharField(db_column='ProductName', max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        db_column='CategoryId', related_name='products'
    )
    baseprice = models.DecimalField(db_column='BasePrice', max_digits=18, decimal_places=0, default=0)
    imageurl = models.CharField(db_column='ImageUrl', max_length=500, null=True, blank=True)
    material = models.CharField(db_column='Material', max_length=300, null=True, blank=True)
    sizeoptions = models.CharField(db_column='SizeOptions', max_length=200, null=True, blank=True)
    description = models.TextField(db_column='Description', null=True, blank=True)
    stock = models.IntegerField(db_column='Stock', default=0)
    isavailable = models.BooleanField(db_column='IsAvailable', default=True)
    createdat = models.DateTimeField(db_column='CreatedAt', auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'Products'

    def __str__(self):
        return self.productname

    def get_sizes(self):
        """Trả về list các size từ chuỗi '40cm,80cm,120cm'"""
        if self.sizeoptions:
            return [s.strip() for s in self.sizeoptions.split(',')]
        return ['40cm']

    def get_image_url(self):
        """Trả về URL ảnh, tương thích cả /Content/images/... và static"""
        if self.imageurl:
            # Chuyển /Content/images/xxx sang /static/images/xxx
            return self.imageurl.replace('/Content/images/', '/static/images/')
        return '/static/images/gau-1.jpg'


class ShopUser(models.Model):
    """Bảng dbo.Users - tài khoản thành viên"""
    userid = models.AutoField(db_column='UserId', primary_key=True)
    username = models.CharField(db_column='Username', max_length=50, unique=True)
    password = models.CharField(db_column='Password', max_length=100)
    fullname = models.CharField(db_column='FullName', max_length=100)
    email = models.CharField(db_column='Email', max_length=100, null=True, blank=True)
    phone = models.CharField(db_column='Phone', max_length=20, null=True, blank=True)
    address = models.CharField(db_column='Address', max_length=300, null=True, blank=True)
    role = models.CharField(db_column='Role', max_length=20, default='Customer')
    createdat = models.DateTimeField(db_column='CreatedAt', auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'Users'

    def __str__(self):
        return self.username


class Order(models.Model):
    """Bảng dbo.Orders"""
    STATUS_CHOICES = [
        ('Chờ xác nhận', 'Chờ xác nhận'),
        ('Đang giao', 'Đang giao'),
        ('Hoàn thành', 'Hoàn thành'),
        ('Đã hủy', 'Đã hủy'),
    ]
    orderid = models.AutoField(db_column='OrderId', primary_key=True)
    ordercode = models.CharField(db_column='OrderCode', max_length=30)
    customername = models.CharField(db_column='CustomerName', max_length=200)
    phone = models.CharField(db_column='Phone', max_length=20)
    address = models.CharField(db_column='Address', max_length=500)
    orderdate = models.DateTimeField(db_column='OrderDate', auto_now_add=True)
    totalamount = models.DecimalField(db_column='TotalAmount', max_digits=18, decimal_places=0, default=0)
    paymentmethod = models.CharField(db_column='PaymentMethod', max_length=50, default='COD')
    isgiftwrapped = models.BooleanField(db_column='IsGiftWrapped', default=False)
    giftmessage = models.CharField(db_column='GiftMessage', max_length=500, null=True, blank=True)
    status = models.CharField(db_column='Status', max_length=50, default='Chờ xác nhận')

    class Meta:
        managed = False
        db_table = 'Orders'

    def __str__(self):
        return self.ordercode


class OrderDetail(models.Model):
    """Bảng dbo.OrderDetails"""
    orderdetailid = models.AutoField(db_column='OrderDetailId', primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, db_column='OrderId', related_name='details')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, db_column='ProductId')
    productname = models.CharField(db_column='ProductName', max_length=200)
    imageurl = models.CharField(db_column='ImageUrl', max_length=500, null=True, blank=True)
    selectedsize = models.CharField(db_column='SelectedSize', max_length=20)
    quantity = models.IntegerField(db_column='Quantity', default=1)
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=18, decimal_places=0, default=0)

    class Meta:
        managed = False
        db_table = 'OrderDetails'

    def get_subtotal(self):
        return self.quantity * self.unitprice
