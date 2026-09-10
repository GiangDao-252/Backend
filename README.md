Câu 3:

- Try calling /predict without location — confirm it still works and explain why.
  Không có location => location other => multiple = 1
- Try calling /predict without area — confirm you get a 422 error and explain why.
  Vì không có số liệu để tính toán

cat << 'EOF' > README.md

# House Price Prediction API

Dự án này là một ứng dụng web kết nối giữa frontend (HTML/JS) và backend (FastAPI/Python) để dự đoán giá bất động sản dựa trên diện tích, số phòng ngủ và khu vực.

## Hướng dẫn khởi chạy dự án (How to run)

Để khởi chạy dự án trên máy tính cục bộ, hãy thực hiện lần lượt các bước sau trong terminal:

1. Mở terminal và di chuyển vào thư mục chứa mã nguồn backend (nơi chứa tệp `main.py`):
   ```bash
   cd BE
   ```
2. Khởi động server FastAPI bằng Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```
3. Mở trình duyệt web và truy cập vào đường dẫn sau để sử dụng giao diện frontend:
   `http://127.0.0.1:8000/static/house_form.html`

_(Lưu ý: Bạn phải truy cập qua đường dẫn này, tuyệt đối không sử dụng extension Live Server của VS Code để mở file HTML nhằm tránh lỗi CORS)._

---

## Giải thích các câu hỏi (Q&A)

### Task 3: Test API qua URL

**1. Tại sao gọi `/predict` mà không có tham số `location` (ví dụ: `/predict?area=80&bedrooms=3`) thì API vẫn hoạt động?**

- **Trả lời:** Vì trong định nghĩa hàm `predict_price` ở file `main.py`, tham số `location` đã được gán sẵn một giá trị mặc định (`location: str = "other"`). FastAPI dựa vào đó để hiểu đây là một tham số tùy chọn (optional query parameter). Nếu request không gửi lên biến `location`, hệ thống sẽ tự động sử dụng giá trị mặc định là `"other"` để tính toán mà không gây ra lỗi.

**2. Tại sao gọi `/predict` mà không có tham số `area` (ví dụ: `/predict?bedrooms=3&location=hanoi`) thì hệ thống báo lỗi 422?**

- **Trả lời:** Vì tham số `area` được khai báo kiểu dữ liệu (`area: float`) nhưng lại không được cung cấp giá trị mặc định. Do đó, FastAPI xem đây là một tham số bắt buộc (required). Khi request bị thiếu dữ liệu này, cơ chế kiểm tra tính hợp lệ tự động (tích hợp từ thư viện Pydantic) sẽ từ chối xử lý và lập tức trả về mã lỗi HTTP 422 (Unprocessable Entity).

### Task 5: Kết nối Form với API

**3. Tại sao sử dụng URL tương đối (relative URL, ví dụ: `/predict?...`) trong hàm `fetch()` của JavaScript lại hoạt động thành công?**

- **Trả lời:** Bởi vì giao diện frontend (tệp HTML) hiện đang được phân phối (serve) trực tiếp bởi chính server FastAPI thông qua tính năng `StaticFiles`. Điều này có nghĩa là cả frontend và backend đều đang chạy chung trên một nguồn duy nhất (cùng origin là `http://127.0.0.1:8000`). Khi gọi một URL tương đối, trình duyệt sẽ tự động lấy origin hiện tại ghép vào để tạo thành URL hoàn chỉnh. Cách thiết lập này giúp dự án hoạt động trơn tru mà không vấp phải rào cản bảo mật đa nguồn (CORS).
  EOF
