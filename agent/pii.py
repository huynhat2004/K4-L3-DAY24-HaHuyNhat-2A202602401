"""BƯỚC 3a — PII gate TRƯỚC KHI vào context/store (12').

Đọc CHECKPOINTS.md (§3a) trước khi bắt đầu: Presidio không có tiếng Việt
sẵn (AnalyzerEngine() mặc định chỉ hỗ trợ "en"). Đường an toàn cho 2h là
regex recognizer + deny-list cho PERSON — coi spaCy/transformers NER là
stretch goal, KHÔNG bắt buộc.

Interface bắt buộc (tests/test_pii.py gọi trực tiếp 2 hàm này):

    detect(text: str) -> list[dict]
        Mỗi entity: {"type": str, "start": int, "end": int}
        `type` là một trong: "VN_CCCD", "VN_PHONE", "VN_BANK_ACCOUNT", "EMAIL"
        `start`/`end` là offset ký tự trong `text` (offset đầu bao gồm,
        offset cuối KHÔNG bao gồm — giống slice Python text[start:end]).
        Format này khớp với tests/vn_pii_testset.jsonl.

    redact(text: str) -> str
        Trả về `text` sau khi mọi entity từ detect() bị thay bằng
        "[REDACTED_<TYPE>]". Phải xử lý overlap/thứ tự đúng khi có nhiều
        entity (gợi ý: thay từ cuối văn bản về đầu để offset không bị lệch).

Gợi ý định dạng (không bắt buộc đúng regex này, miễn đạt ngưỡng trên test
set ở tests/vn_pii_testset.jsonl):
    VN_CCCD          12 chữ số liên tiếp
    VN_PHONE         0 + 9-10 chữ số, có thể có dấu cách/gạch ngang
    VN_BANK_ACCOUNT  8-16 chữ số liên tiếp, thường đi kèm "STK"/"số tài khoản"
    EMAIL            dạng chuẩn local@domain.tld

Đo bằng: pytest tests/test_pii.py -v -s   (in ra precision/recall)
"""
from __future__ import annotations

import re


_PATTERNS = (
    (
        "EMAIL",
        re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
        0,
        100,
    ),
    (
        "VN_CCCD",
        re.compile(r"\bCCCD\b[^\d]{0,20}(\d{12})\b", re.IGNORECASE),
        1,
        100,
    ),
    (
        "VN_BANK_ACCOUNT",
        re.compile(r"(?:\bSTK\b|số\s+tài\s+khoản)[^\d]{0,30}(\d{8,16})\b", re.IGNORECASE),
        1,
        100,
    ),
    (
        "VN_PHONE",
        re.compile(
            r"(?:\bSĐT\b|số\s+điện\s+thoại(?:\s+liên\s+hệ)?)[^\d]{0,50}"
            r"(0\d(?:[ -]?\d){8,9})\b",
            re.IGNORECASE,
        ),
        1,
        100,
    ),
    (
        "VN_PHONE",
        re.compile(r"(?<!\d)(0\d(?:[ -]?\d){8,9})(?!\d)"),
        1,
        20,
    ),
    (
        "VN_CCCD",
        re.compile(r"(?<!\d)(\d{12})(?!\d)"),
        1,
        10,
    ),
)


def _overlaps(left: dict, right: dict) -> bool:
    return left["start"] < right["end"] and right["start"] < left["end"]


def detect(text: str) -> list[dict]:
    candidates: list[tuple[int, dict]] = []
    for entity_type, pattern, group, priority in _PATTERNS:
        for match in pattern.finditer(text):
            start, end = match.span(group)
            candidates.append(
                (priority, {"type": entity_type, "start": start, "end": end})
            )

    # Ưu tiên pattern có nhãn rõ ràng (CCCD/STK/SĐT) trước pattern fallback
    # để một STK 12 số không bị nhận nhầm thành CCCD.
    selected: list[dict] = []
    for _, candidate in sorted(
        candidates,
        key=lambda item: (-item[0], item[1]["start"], item[1]["end"]),
    ):
        if not any(_overlaps(candidate, existing) for existing in selected):
            selected.append(candidate)
    return sorted(selected, key=lambda entity: (entity["start"], entity["end"]))


def redact(text: str) -> str:
    result = text
    for entity in sorted(detect(text), key=lambda item: item["start"], reverse=True):
        marker = f"[REDACTED_{entity['type']}]"
        result = result[: entity["start"]] + marker + result[entity["end"] :]
    return result
