# DPIA-lite

## 1. Phạm vi và dữ liệu

Đây là đánh giá kỹ thuật thu gọn cho agent mock trong repo, dùng hoàn toàn dữ
liệu tổng hợp. `data/customers.json` chứa customer ID, họ tên, CCCD, số điện
thoại, số tài khoản ngân hàng, email và ticket liên quan. Lab phân loại record
khách hàng là `restricted`; nội dung ticket là `internal` nhưng không tin cậy;
ledger chỉ chứa metadata và hash tham số. Không dùng PII hay credential thật.

## 2. Mục đích, principal và cơ sở quyết định

- `summarize-tickets`: tìm và tóm tắt ticket cho principal hợp lệ.
- `support-reply`: chỉ `dpo` trong fixture được đọc customer gắn với ticket;
  `support_l1` chỉ được `search_docs`.
- `--as` chỉ chọn principal mô phỏng. Nó không xác thực danh tính người dùng và
  không được xem là authentication/authorization production.

## 3. Luồng dữ liệu và nơi nhận

1. Run A nhận query, gọi `search_docs` sau policy allow và đọc toàn văn corpus
   không tin cậy. Mock phát hiện chỉ thị injection trong Run A.
2. Nếu free text yêu cầu egress, PEP ghi `http_post=deny` trước khi private
   record được đọc. URL chỉ tham gia tính `args_hash`, không được ghi thô.
3. Boundary A→B chỉ truyền `list[int]` ticket ID parse từ tên file. Run B suy
   customer ID từ `related_tickets`, rồi kiểm principal, purpose, agent scope,
   parent scope và TTL ngay trước `read_customer`.
4. Endpoint egress duy nhất của lab là `http://127.0.0.1:10024`; lần prove sau
   containment không gọi POST, nên `reports/attack-after.log` rỗng. Không có
   cloud, bên nhận ngoài localhost hay chuyển dữ liệu xuyên biên giới.
5. Mỗi allow/deny được ghi vào `reports/ledger.jsonl` với `agent_id`, `run_id`,
   `on_behalf_of`, `expires_at`, classification, decision, reason và
   `args_hash`; không ghi raw tool arguments hoặc PII.

## 4. Rủi ro và biện pháp giảm thiểu

| Rủi ro | Ảnh hưởng | Control / bằng chứng | Rủi ro còn lại |
|---|---|---|---|
| Prompt injection đổi mục tiêu và yêu cầu exfil | Đọc/gửi sai record restricted | Trifecta split, typed boundary, PEP; `tests/test_split.py`, `tests/test_injection.py` | Corpus/mock không bao phủ mọi kỹ thuật tấn công thực tế. |
| Vượt quyền hoặc delegation mở rộng quyền | `support_l1` đọc CCCD/STK | Giao principal/agent/parent scopes, purpose và TTL; `tests/test_obo.py` | Principal fixture không phải hệ thống IAM hay xác thực thật. |
| PII lọt qua text boundary/log | Lộ dữ liệu khách hàng | Regex gate đạt precision/recall 1.000 trên testset; ledger chỉ dùng `args_hash` | Regex có thể bỏ sót format mới, Unicode lạ hoặc PII không có trong testset. |
| Sửa audit trail | Mất khả năng đối chiếu decision | SHA-256 hash chain và `ledger.verify()` | Không phát hiện cắt dòng cuối hoặc viết lại cả chain nếu không có trusted external anchor. |
| Dependency/hook hoặc secret trong lịch sử | Chèn mã độc, credential bị lạm dụng | Hash lock, Gitleaks v8.30.1, incident note và pre-commit hook | Pin/hash không thay thế provenance review; scanner có thể false positive/negative; secret thật vẫn phải rotate. |

## 5. Lưu giữ, truy cập và xóa

Corpus, customer fixture và evidence nằm trong repo local phục vụ chấm bài.
`sink.log` là file tạm và bị `.gitignore`; `attack-before.log`,
`attack-after.log` và ledger là evidence synthetic phải được kiểm nội dung trước
khi force-add. Bài lab chưa định nghĩa retention production, quy trình đáp ứng
quyền của chủ thể dữ liệu hay delete cascade. Nếu triển khai thật phải xác định
thời hạn, owner, quyền truy cập, backup, xóa và quy trình xử lý yêu cầu pháp lý.

## 6. Kết quả prove và giới hạn

- Full suite: 33 test pass; PII precision/recall 1.000/1.000.
- `reports/attack-after.log`: 0 byte sau lần chạy thủ công dưới `dpo`.
- Ledger: 23 entries, `verify=True`, không entry thiếu reason, có một
  `http_post=deny` cho `dpo`, không chứa PII/URL/customer ID thô.
- Đây chỉ là mock deterministic trên dữ liệu synthetic và localhost. Nó không
  chứng minh tuân thủ pháp luật, độ an toàn production, bất biến tuyệt đối của
  ledger, chất lượng mô hình thật hoặc hiệu lực của cơ chế xác thực thật.
