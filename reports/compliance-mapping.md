# Compliance mapping

Đối chiếu ngày 12/10/2026 với bản chính thức được công bố bởi Cổng Thông
tin/Công báo Chính phủ và tài liệu OWASP. Đây là mapping giữa yêu cầu và
control của bài lab, **không phải kết luận hay chứng nhận tuân thủ pháp luật**.

| Nguồn / điều khoản đã đối chiếu | Control trong lab | Evidence file:dòng | Giới hạn |
|---|---|---|---|
| [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15](https://chinhphu.vn/?classid=1&docid=214590&orggroupid=1&pageid=27160), Điều 17 về đánh giá tác động xử lý dữ liệu cá nhân | Phân loại dữ liệu; mô tả mục đích, luồng và rủi ro trong DPIA-lite; regex detect/redact; policy chặn restricted egress; audit decision bằng hash chain | `reports/dpia-lite.md:5`; `agent/pii.py:84`; `agent/policy.py:60`; `agent/ledger.py:54` | DPIA-lite chỉ là bài tập trên dữ liệu synthetic, không phải hồ sơ đánh giá tác động chính thức và chưa được gửi cơ quan có thẩm quyền. |
| [Nghị định 356/2025/NĐ-CP](https://chinhphu.vn/?docid=216387&pageid=27160), Điều 19 về thành phần/nội dung hồ sơ đánh giá tác động và Điều 20 về cập nhật hồ sơ | DPIA-lite ghi loại dữ liệu, mục đích, data flow, bên nhận, biện pháp bảo vệ, rủi ro và giới hạn; evidence được cập nhật sau lần prove cuối | `reports/dpia-lite.md:5`; `reports/dpia-lite.md:19`; `reports/dpia-lite.md:35`; `reports/dpia-lite.md:54` | Không có hợp đồng xử lý, thông tin tổ chức, thủ tục nộp hồ sơ hay hoạt động chuyển dữ liệu xuyên biên giới; lab không thay thế nghĩa vụ thực tế. |
| [Luật Trí tuệ nhân tạo 134/2025/QH15](https://chinhphu.vn/?classid=1&docid=216334&orggroupid=1&pageid=27160), khoản 3 Điều 7 về xử lý dữ liệu phù hợp pháp luật; Điều 11 về minh bạch; Điều 12 về xử lý sự cố | CLI công khai `--as` là principal mô phỏng; policy decision có reason; ledger gắn principal/run/TTL; incident note ghi cách ứng phó nếu secret thật bị lộ | `agent/loop.py:83`; `agent/runner.py:96`; `reports/ledger.jsonl:2`; `reports/secrets-incident.md:14` | Chưa phân loại mức rủi ro pháp lý của một hệ thống production; mock deterministic không chứng minh đầy đủ minh bạch, giám sát con người hay quy trình sự cố thực tế. |
| [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) — ASI01 Agent Goal Hijack | 4 lure được replay; Run A cô lập nội dung không tin cậy, chỉ ticket ID typed đi sang Run B; PEP deny egress | `injection-corpus.md:47`; `agent/runner.py:168`; `reports/ledger.jsonl:2`; `reports/attack-after.log` (0 byte) | Mock chỉ bao phủ corpus cố định, không chứng minh chống mọi prompt injection hoặc encoding/đa ngôn ngữ. |
| Cùng tài liệu OWASP — ASI03 Identity & Privilege Abuse | Quyền hiệu lực là giao của principal, agent scope và parent scope; kiểm purpose/TTL; `support_l1` deny và `dpo` còn tiện ích hợp lệ | `agent/policy.py:69`; `agent/policy.py:83`; `agent/runner.py:204`; `tests/test_obo.py:29` | `--as` không phải authentication production; principal là fixture local và TTL được tạo trong process. |
| Cùng tài liệu OWASP — ASI04 Agentic Supply Chain Vulnerabilities | Dependency lock có hash; Gitleaks hook pin v8.30.1; quét lịch sử và current tree; incident response phân biệt detection với rotate | `requirements.lock:7`; `.pre-commit-config.yaml:1`; `reports/secrets-incident.md:3`; `reports/verification.md:6` | Hash/pin không chứng minh nguồn package hoàn toàn đáng tin và không thu hồi credential đã lộ; hook system còn phụ thuộc binary Gitleaks trên PATH. |

## Nguồn chính thức đã dùng

- Luật 91/2025/QH15: trang văn bản và PDF ký số trên `chinhphu.vn` /
  `datafiles.chinhphu.vn`, ban hành 26/06/2025, hiệu lực 01/01/2026.
- Nghị định 356/2025/NĐ-CP: trang văn bản và PDF ký số trên `chinhphu.vn` /
  `datafiles.chinhphu.vn`, ban hành 31/12/2025, hiệu lực 01/01/2026.
- Luật 134/2025/QH15: trang văn bản và PDF chính thức trên `chinhphu.vn` /
  `datafiles.chinhphu.vn`.
- OWASP GenAI Security Project, *Top 10 for Agentic Applications 2026*.
