# HƯỚNG DẪN TRIỂN KHAI (DEPLOY) & BẢO VỆ ĐỒ ÁN TEDDYSHOP

---

## 🌟 1. KIẾN TRÚC HỆ THỐNG TRIỂN KHAI (PRODUCTION ARCHITECTURE)

* **Web Application Framework**: Django 6.1 (Python 3.10+)
* **WSGI Production Server**: **Waitress** (Multi-threaded WSGI Server, 8 luồng xử lý đồng thời).
* **Static & Media Files Handler**: **WhiteNoise** kết hợp `collectstatic` (phục vụ CSS, JS, ảnh nén tốc độ cao).
* **Database Management System**: **Microsoft SQL Server Express (`.\SQLEXPRESS`)** – giữ nguyên 100% dữ liệu 11 sản phẩm gấu bông và đơn hàng thực tế.
* **Internet Gateway / SSL**: **Cloudflare Tunnel** (cấp chứng chỉ bảo mật HTTPS toàn cầu, chống DDoS, không cần NAT Port modem).

---

## 🚀 2. CÁCH KHỞI CHẠY HỆ THỐNG (1 CLICK)

### Cách 1: Chạy có link Internet HTTPS (Khuyên dùng khi báo cáo với thầy cô)
* Bấm đúp vào file ngoài màn hình Desktop: `TEDDYSHOP_DEPLOY_INTERNET.bat`
* Hoặc chạy file: `D:\GauBongDjango\2_CHAY_DEPLOY_INTERNET_HTTPS.bat`
* **Kết quả**:
  - Cửa sổ 1: Máy chủ **Waitress Production** khởi động tại `http://127.0.0.1:8000`.
  - Cửa sổ 2: **Cloudflare Tunnel** in ra đường link công khai dạng:
    👉 `https://xxxx-xxxx-xxxx.trycloudflare.com`
  - Bạn có thể gửi link này cho thầy cô hoặc mở ngay trên điện thoại để demo đặt hàng từ xa.

### Cách 2: Chạy cục bộ nội bộ (Khi máy không có mạng Internet)
* Chạy file: `D:\GauBongDjango\1_CHAY_PRODUCTION_LOCAL.bat`
* Truy cập trên máy tính qua: `http://localhost:8000` hoặc `http://127.0.0.1:8000`.

---

## 🎓 3. KỊCH BẢN TRẢ LỜI CÂU HỎI KHI BẢO VỆ TRƯỚC GIẢNG VIÊN

#### ❓ Câu hỏi 1: "Tại sao em không cài máy ảo Ubuntu / Linux để deploy?"
> **Trả lời:**
> *"Dạ thưa thầy/cô, việc dựng máy ảo VMware/VirtualBox đòi hỏi phân bổ nhiều RAM và CPU của máy thật, dễ gây giật lag trong quá trình vừa trình chiếu vừa demo. Đồng thời, CSDL chính của hệ thống là **Microsoft SQL Server**, vốn tương thích và tối ưu hóa tốt nhất trên nền tảng Windows. Em đã lựa chọn phương án **Native Windows Production Deployment** sử dụng máy chủ WSGI **Waitress** – một chuẩn triển khai doanh nghiệp cho Python trên môi trường Windows. Giải pháp này giúp tận dụng tối đa phần cứng máy tính, độ trễ phản hồi cực thấp (<10ms) và bảo đảm tính toàn vẹn 100% cho CSDL SQL Server."*

#### ❓ Câu hỏi 2: "Tại sao em không dùng lệnh `manage.py runserver` quen thuộc?"
> **Trả lời:**
> *"Dạ thưa thầy/cô, lệnh `runserver` chỉ là Development Server được Django thiết kế riêng cho mục đích gỡ lỗi (debug) và lập trình viên viết code. `runserver` chỉ xử lý đơn luồng tuần tự, không có cơ chế nén tài nguyên tĩnh và không đảm bảo tính ổn định chịu tải. Do đó, em đã chuyển đổi sang **Waitress WSGI Server** với cấu hình 8 luồng (`threads=8`), đồng thời tích hợp middleware **WhiteNoise** để phục vụ tài nguyên tĩnh nén chuẩn, đáp ứng đúng yêu cầu của một môi trường Production thực thụ."*

#### ❓ Câu hỏi 3: "Đường link HTTPS ra ngoài Internet của em hoạt động thế nào?"
> **Trả lời:**
> *"Dạ, em sử dụng công nghệ **Cloudflare Tunnel** (`cloudflared`). Công nghệ này thiết lập một đường truyền mã hóa Outbound an toàn từ máy chủ của em lên mạng lưới biên toàn cầu của Cloudflare qua giao thức QUIC/HTTP2. Ưu điểm là em không cần phải mở cổng (Port Forwarding) trên modem của trường hay gia đình (tránh nguy cơ bị quét cổng mạng), đồng thời website tự động được cấp chứng chỉ SSL/TLS xanh hợp lệ và được bảo vệ bởi tường lửa chống tấn công từ chối dịch vụ (DDoS) của Cloudflare."*
