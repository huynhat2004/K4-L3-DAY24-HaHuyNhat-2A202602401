# Secret giả trong lịch sử Git

- Scanner và phiên bản: Gitleaks 8.30.1, dùng cấu hình `.gitleaks.toml` của lab.
- Commit chứa token giả: `1bdd849922156c868a5ee9293d68f5b72e242d2c` (`1bdd849`).
- File, rule và kết quả quét lịch sử: `lab-fake-secret.txt`, rule
  `lab24-synthetic-token`; lệnh `gitleaks git --config .gitleaks.toml
  --redact --verbose .` quét 7 commit, báo đúng 1 finding và trả exit code 1
  như dự kiến. Giá trị đã được redact trong output. Đây là token synthetic,
  vô hiệu được cài sẵn cho bài lab, không phải credential thật.
- Kết quả quét file hiện tại: `gitleaks dir --config .gitleaks.toml --redact
  --verbose .` trả exit code 0 và `no leaks found`.
- Xử lý trong lab: file chứa token đã bị xoá khỏi HEAD; giữ finding trong lịch
  sử làm bằng chứng của checkpoint, không tạo hay sử dụng secret thật.
- Nếu đây là credential thật: phải thu hồi/rotate ngay tại nhà cung cấp, kiểm
  tra log sử dụng và phạm vi ảnh hưởng, cập nhật nơi dùng credential mới, rồi
  mới cân nhắc rewrite lịch sử Git và phối hợp để mọi clone cũ được xử lý.
- Xoá file khỏi HEAD không thu hồi giá trị đã xuất hiện trong commit cũ. Pin
  dependency và hook Gitleaks giúp giảm rủi ro supply-chain và phát hiện lần
  commit tiếp theo, nhưng không thể làm credential đã lộ mất hiệu lực; bước
  rotate/thu hồi vẫn bắt buộc đối với secret thật.
