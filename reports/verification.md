# Verification

- OS / Python / Gitleaks version: macOS 15.5 (24F74), Python 3.14.8,
  Gitleaks 8.30.1.
- `.venv/bin/python -m pytest tests/ -q -s`: 33 passed in 0.62s.
- `pre-commit run --all-files`: Passed (`gitleaks-system`, rev `v8.30.1`).
- `pip install --require-hashes -r requirements.lock`: thành công; tất cả
  dependency đã khớp phiên bản và hash trong lockfile.
- Quét lịch sử: đúng 1 finding synthetic ở commit `1bdd849`, exit code 1 như
  dự kiến. Quét working tree hiện tại: sạch, exit code 0.
- Lần prove thủ công: reset sink, chạy agent `--mock --as dpo` với query gốc;
  `reports/attack-after.log` có kích thước 0 byte.
- Ledger verify: `True`; 23 entries, không entry thiếu `reason`, có một
  `http_post=deny` cho `on_behalf_of=dpo`, không chứa PII/URL/customer ID thô.
- Các lỗi còn lại: không có trong phạm vi bài lab. Các giới hạn production
  được ghi trong `reports/dpia-lite.md` và `reports/compliance-mapping.md`.
