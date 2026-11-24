"""
views.py - Toàn bộ logic xử lý cho Cửa Hàng Gấu Bông Django
"""
import uuid
from datetime import datetime
from functools import wraps

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Category, Product, ShopUser, Order, OrderDetail


# =============================================================
# DECORATORS BẢO VỆ TRANG ADMIN
# =============================================================

def login_required_custom(view_func):
    """Yêu cầu đăng nhập"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.error(request, 'Vui lòng đăng nhập để tiếp tục.')
            return redirect(f'/account/login/?next={request.path}')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Yêu cầu quyền Admin"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.error(request, 'Vui lòng đăng nhập.')
            return redirect(f'/account/login/?next={request.path}')
        if request.session.get('user_role') != 'Admin':
            messages.error(request, '⛔ Bạn không có quyền truy cập trang quản trị!')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


# =============================================================
# HOME - TRANG CHỦ
# =============================================================

def home(request):
    """Trang chủ: danh mục + sản phẩm nổi bật"""
    try:
        categories = list(Category.objects.all())
        featured_products = list(Product.objects.filter(isavailable=True).order_by('-productid')[:8])
    except Exception as e:
        categories = []
        featured_products = []
        messages.warning(request, f'Không thể kết nối database: {e}')

    return render(request, 'shop/home.html', {
        'categories': categories,
        'featured_products': featured_products,
    })


# =============================================================
# PRODUCT - DANH SÁCH & CHI TIẾT SẢN PHẨM
# =============================================================

def product_list(request):
    """Danh sách sản phẩm - tìm kiếm, lọc danh mục, sắp xếp"""
    search = request.GET.get('search', '').strip()
    category_id = request.GET.get('category', '')
    sort = request.GET.get('sort', '')

    try:
        products = Product.objects.filter(isavailable=True)

        if search:
            products = products.filter(productname__icontains=search)

        if category_id:
            products = products.filter(category_id=category_id)

        if sort == 'price_asc':
            products = products.order_by('baseprice')
        elif sort == 'price_desc':
            products = products.order_by('-baseprice')
        else:
            products = products.order_by('productid')

        products = list(products)
        categories = list(Category.objects.all())

    except Exception as e:
        products = []
        categories = []
        messages.warning(request, f'Lỗi kết nối database: {e}')

    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'current_search': search,
        'current_category': category_id,
        'current_sort': sort,
    })


def product_detail(request, pk):
    """Chi tiết sản phẩm"""
    product = get_object_or_404(Product, pk=pk, isavailable=True)
    related = list(
        Product.objects.filter(category=product.category, isavailable=True)
        .exclude(pk=pk)[:4]
    )
    sizes = product.get_sizes()

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related': related,
        'sizes': sizes,
    })


# =============================================================
# CART - GIỎ HÀNG
# =============================================================

def cart(request):
    """Hiển thị giỏ hàng"""
    cart_data = request.session.get('cart', {})
    cart_items = []
    total = 0

    for key, item in cart_data.items():
        subtotal = item['price'] * item['quantity']
        total += subtotal
        cart_items.append({
            'key': key,
            'name': item['name'],
            'image': item['image'],
            'size': item['size'],
            'price': item['price'],
            'quantity': item['quantity'],
            'subtotal': subtotal,
        })

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


def cart_add(request):
    """Thêm sản phẩm vào giỏ"""
    if request.method != 'POST':
        return redirect('cart')

    product_id = request.POST.get('product_id')
    size = request.POST.get('size', '40cm').strip()
    quantity = int(request.POST.get('quantity', 1))

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        messages.error(request, 'Sản phẩm không tồn tại!')
        return redirect('home')

    # Key = productId_size để phân biệt cùng sản phẩm khác size
    cart_key = f"{product_id}_{size}"
    cart = request.session.get('cart', {})

    if cart_key in cart:
        cart[cart_key]['quantity'] += quantity
    else:
        cart[cart_key] = {
            'product_id': product_id,
            'name': product.productname,
            'image': product.get_image_url(),
            'size': size,
            'price': float(product.baseprice),
            'quantity': quantity,
        }

    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, f'✅ Đã thêm "{product.productname}" ({size}) vào giỏ hàng!')
    return redirect('cart')


def cart_remove(request, key):
    """Xóa sản phẩm khỏi giỏ"""
    cart = request.session.get('cart', {})
    if key in cart:
        name = cart[key]['name']
        del cart[key]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f'Đã xóa "{name}" khỏi giỏ hàng.')
    return redirect('cart')


def checkout(request):
    """Trang đặt hàng"""
    cart_data = request.session.get('cart', {})
    if not cart_data:
        messages.warning(request, 'Giỏ hàng của bạn đang trống!')
        return redirect('cart')

    cart_items = []
    total = 0
    for key, item in cart_data.items():
        subtotal = item['price'] * item['quantity']
        total += subtotal
        cart_items.append({**item, 'key': key, 'subtotal': subtotal})

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        payment = request.POST.get('payment', 'COD')
        gift_wrapped = request.POST.get('gift_wrapped') == 'on'
        gift_message = request.POST.get('gift_message', '').strip()

        if not name or not phone or not address:
            messages.error(request, 'Vui lòng điền đầy đủ thông tin!')
            return render(request, 'shop/checkout.html', {'cart_items': cart_items, 'total': total})

        # Tạo đơn hàng
        order_code = f"GB{datetime.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4())[:4].upper()}"
        order = Order.objects.create(
            ordercode=order_code,
            customername=name,
            phone=phone,
            address=address,
            totalamount=total,
            paymentmethod=payment,
            isgiftwrapped=gift_wrapped,
            giftmessage=gift_message if gift_wrapped else '',
            status='Chờ xác nhận',
        )

        for item in cart_items:
            try:
                product = Product.objects.get(pk=item['product_id'])
            except Product.DoesNotExist:
                product = None

            OrderDetail.objects.create(
                order=order,
                product=product if product else Product.objects.first(),
                productname=item['name'],
                imageurl=item['image'],
                selectedsize=item['size'],
                quantity=item['quantity'],
                unitprice=item['price'],
            )

        # Xóa giỏ hàng
        request.session['cart'] = {}
        request.session.modified = True
        messages.success(request, f'🎉 Đặt hàng thành công! Mã đơn: {order_code}')
        return redirect('order_success', order_id=order.orderid)

    return render(request, 'shop/checkout.html', {'cart_items': cart_items, 'total': total})


def order_success(request, order_id):
    """Trang đặt hàng thành công"""
    order = get_object_or_404(Order, pk=order_id)
    details = list(OrderDetail.objects.filter(order=order))
    return render(request, 'shop/order_success.html', {'order': order, 'details': details})


# =============================================================
# ACCOUNT - ĐĂNG NHẬP / ĐĂNG XUẤT / ĐĂNG KÝ
# =============================================================

def login_view(request):
    """Đăng nhập"""
    if request.session.get('user_id'):
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            user = ShopUser.objects.get(username=username, password=password)
            request.session['user_id'] = user.userid
            request.session['username'] = user.username
            request.session['user_fullname'] = user.fullname
            request.session['user_role'] = user.role
            messages.success(request, f'👋 Chào mừng {user.fullname}!')
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        except ShopUser.DoesNotExist:
            messages.error(request, '❌ Tên đăng nhập hoặc mật khẩu không đúng!')

    return render(request, 'shop/login.html')


def logout_view(request):
    """Đăng xuất"""
    request.session.flush()
    messages.success(request, 'Đã đăng xuất thành công!')
    return redirect('home')


def register_view(request):
    """Đăng ký tài khoản mới"""
    if request.session.get('user_id'):
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        fullname = request.POST.get('fullname', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()

        if not username or not password or not fullname:
            messages.error(request, 'Vui lòng điền đầy đủ thông tin bắt buộc!')
            return render(request, 'shop/register.html')

        if ShopUser.objects.filter(username=username).exists():
            messages.error(request, f'Tên đăng nhập "{username}" đã tồn tại!')
            return render(request, 'shop/register.html')

        user = ShopUser.objects.create(
            username=username,
            password=password,
            fullname=fullname,
            email=email,
            phone=phone,
            role='Customer',
        )
        messages.success(request, '🎉 Đăng ký thành công! Vui lòng đăng nhập.')
        return redirect('login')

    return render(request, 'shop/register.html')


# =============================================================
# ADMIN PANEL - QUẢN TRỊ
# =============================================================

@admin_required
def admin_dashboard(request):
    """Dashboard tổng quan Admin"""
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_revenue = sum(o.totalamount for o in Order.objects.filter(status='Hoàn thành'))
    pending_orders = Order.objects.filter(status='Chờ xác nhận').count()
    recent_orders = list(Order.objects.order_by('-orderdate')[:5])

    return render(request, 'shop/admin/dashboard.html', {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'pending_orders': pending_orders,
        'recent_orders': recent_orders,
    })


@admin_required
def admin_products(request):
    """Danh sách sản phẩm trong Admin"""
    products = list(Product.objects.all().order_by('productid'))
    return render(request, 'shop/admin/product_list.html', {'products': products})


@admin_required
def admin_product_add(request):
    """Thêm sản phẩm mới"""
    categories = list(Category.objects.all())

    if request.method == 'POST':
        name = request.POST.get('productname', '').strip()
        cat_id = request.POST.get('category')
        price = request.POST.get('baseprice', 0)
        material = request.POST.get('material', '').strip()
        sizes = request.POST.get('sizeoptions', '').strip()
        desc = request.POST.get('description', '').strip()
        stock = request.POST.get('stock', 0)
        image_url = ''

        # Xử lý upload ảnh
        if 'image' in request.FILES:
            img = request.FILES['image']
            import os
            from django.conf import settings as django_settings
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:18]
            ext = os.path.splitext(img.name)[1]
            filename = f'gau-{timestamp}{ext}'
            save_path = django_settings.BASE_DIR / 'shop' / 'static' / 'images' / filename
            with open(save_path, 'wb+') as dest:
                for chunk in img.chunks():
                    dest.write(chunk)
            image_url = f'/static/images/{filename}'

        try:
            category = Category.objects.get(pk=cat_id)
            Product.objects.create(
                productname=name,
                category=category,
                baseprice=price,
                imageurl=image_url,
                material=material,
                sizeoptions=sizes,
                description=desc,
                stock=stock,
                isavailable=True,
            )
            messages.success(request, f'✅ Đã thêm sản phẩm "{name}" thành công!')
            return redirect('admin_products')
        except Exception as e:
            messages.error(request, f'Lỗi: {e}')

    return render(request, 'shop/admin/product_form.html', {
        'categories': categories,
        'action': 'Thêm',
        'product': None,
    })


@admin_required
def admin_product_edit(request, pk):
    """Sửa sản phẩm"""
    product = get_object_or_404(Product, pk=pk)
    categories = list(Category.objects.all())

    if request.method == 'POST':
        product.productname = request.POST.get('productname', product.productname).strip()
        product.category = Category.objects.get(pk=request.POST.get('category'))
        product.baseprice = request.POST.get('baseprice', product.baseprice)
        product.material = request.POST.get('material', '').strip()
        product.sizeoptions = request.POST.get('sizeoptions', '').strip()
        product.description = request.POST.get('description', '').strip()
        product.stock = request.POST.get('stock', product.stock)
        product.isavailable = request.POST.get('isavailable') == 'on'

        if 'image' in request.FILES:
            img = request.FILES['image']
            import os
            from django.conf import settings as django_settings
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:18]
            ext = os.path.splitext(img.name)[1]
            filename = f'gau-{timestamp}{ext}'
            save_path = django_settings.BASE_DIR / 'shop' / 'static' / 'images' / filename
            with open(save_path, 'wb+') as dest:
                for chunk in img.chunks():
                    dest.write(chunk)
            product.imageurl = f'/static/images/{filename}'

        product.save()
        messages.success(request, f'✅ Đã cập nhật "{product.productname}"!')
        return redirect('admin_products')

    return render(request, 'shop/admin/product_form.html', {
        'categories': categories,
        'action': 'Sửa',
        'product': product,
    })


@admin_required
def admin_product_delete(request, pk):
    """Xóa sản phẩm"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.productname
        product.delete()
        messages.success(request, f'🗑️ Đã xóa "{name}"!')
        return redirect('admin_products')
    return render(request, 'shop/admin/product_confirm_delete.html', {'product': product})


@admin_required
def admin_orders(request):
    """Danh sách đơn hàng"""
    orders = list(Order.objects.order_by('-orderdate'))
    return render(request, 'shop/admin/order_list.html', {'orders': orders})


@admin_required
def admin_order_detail(request, pk):
    """Chi tiết đơn hàng"""
    order = get_object_or_404(Order, pk=pk)
    details = list(OrderDetail.objects.filter(order=order))
    return render(request, 'shop/admin/order_detail.html', {'order': order, 'details': details})


@admin_required
def admin_order_update(request, pk):
    """Cập nhật trạng thái đơn hàng"""
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        messages.success(request, f'✅ Đơn {order.ordercode}: đã cập nhật → "{new_status}"')
    return redirect('admin_order_detail', pk=pk)
