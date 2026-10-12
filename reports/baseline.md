# Baseline — điền trong checkpoint 1

1. Chưa. Bởi vì trong `agent/loop.py`, hàm `_naive_loop()` chỉ nhận `message` và `llm`, sau đó gọi thẳng các tool. Luồng này thì chưa tạo `agent_id`, `run_id` hay gắn principal riêng cho từng lần chạy (dòng 27-54).
2. Hiện tại không có policy nào để duyệt lệnh này.  `_naive_loop()` gọi trực tiếp `tools.http_post()` khi tìm thấy dữ liệu khách hàng (dòng 42-44 trong `agent/loop.py`). Hàm `http_post()` ở `agent/tools.py` chỉ kiểm tra URL có đúng `127.0.0.1:10024` hay không (dòng 68-85), chứ không kiểm tra quyền hoặc loại dữ liệu được gửi.
3. Bằng chứng em thấy nằm trong `reports/sink.log`. Ở `sink/sink.py`, hàm `make_handler()` tạo `do_POST()` để đọc toàn bộ request body rồi ghi lại thành một dòng JSON gồm `path` và `body` (dòng 40-50). Vì vậy nếu PII bị gửi nhầm thì nội dung đó sẽ xuất hiện trực tiếp trong file log này.
