# HƯỚNG DẪN ĐƯA WEBSITE LÊN RENDER.COM (CHẠY 24/24 MIỄN PHÍ)

---

### BƯỚC 1: TẠO REPOSITORY TRÊN GITHUB & ĐẨY CODE LÊN

1. Truy cập https://github.com và đăng nhập.
2. Bấm nút **New** (Tạo repository mới):
   - Đặt tên: `teddyshop-django`
   - Chọn chế độ: **Public**
   - **Lưu ý:** KHÔNG tích chọn "Add a README file" hay .gitignore (vì ta đã có sẵn).
   - Bấm **Create repository**.
3. Mở PowerShell tại `D:\GauBongDjango` và chạy 2 lệnh sau (thay URL bằng link GitHub của bạn):
   ```powershell
   git remote add origin https://github.com/<TÊN-GITHUB-CỦA-BẠN>/teddyshop-django.git
   git push -u origin main
   ```

---

### BƯỚC 2: KẾT NỐI VÀ DEPLOY TRÊN RENDER.COM

1. Truy cập https://render.com và đăng ký / đăng nhập bằng chính tài khoản **GitHub**.
2. Tại trang Dashboard của Render, bấm nút **New +** ở góc phải trên -> Chọn **Web Service**.
3. Chọn mục **Build and deploy from a Git repository** -> Bấm **Next**.
4. Tìm và bấm nút **Connect** bên cạnh repository `teddyshop-django` vừa tạo.
5. Điền thông tin cấu hình (chỉ mất 30 giây):
   - **Name**: `teddyshop` (hoặc tên bất kỳ bạn thích)
   - **Region**: Singapore (hoặc Oregon / Frankfurt - ưu tiên Singapore để truy cập nhanh ở VN)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn gaubong.wsgi:application`
   - **Instance Type**: Chọn gói **Free** ($0/tháng).
6. Cuộn xuống cuối trang và bấm nút **Create Web Service**.

---

### BƯỚC 3: LẤY LINK NỘP BÀI BÁO CÁO

* Render sẽ tự động chạy cài đặt thư viện, nén file tĩnh và khởi động web trong khoảng 2 - 3 phút.
* Sau khi hoàn tất (báo `Your service is live 🎉`), bạn sẽ nhận được một đường link cố định vĩnh viễn dạng:
  👉 `https://teddyshop-xxxx.onrender.com`
* **Xong!** Bạn có thể nộp đường link này cho thầy cô. Website chạy 24/24 trên đám mây, có đầy đủ 11 sản phẩm gấu bông, giỏ hàng, đặt hàng, quản trị admin. Bạn tắt máy gập laptop đi ngủ thì web vẫn sống bình thường!
