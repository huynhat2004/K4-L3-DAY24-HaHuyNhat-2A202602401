# Verification

- OS / Python / Gitleaks version: macOS 15.5 (24F74), Python 3.14.8,
  Gitleaks 8.30.1.
- `.venv/bin/python -m pytest tests/ -q -s`: 33 passed in 0.60s.
- `pre-commit run --all-files`: Passed (`gitleaks-system`, rev `v8.30.1`).
- `pip install --require-hashes -r requirements.lock`: thành công; tất cả
  dependency đã khớp phiên bản và hash trong lockfile.
- Quét lịch sử: đúng 1 finding synthetic ở commit `1bdd849`, exit code 1 như
  dự kiến. Quét working tree hiện tại: sạch, exit code 0.
- Ledger verify: chưa chạy ở checkpoint 4; sẽ cập nhật sau khi tạo
  `reports/ledger.jsonl` trong checkpoint 5.
- Các lỗi còn lại: không có lỗi CP4; evidence của checkpoint 5 chưa được tạo.
