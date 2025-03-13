# validators.py
import os
import re
from datetime import datetime

# --- Cấu hình email cho phép ---
ALLOWED_EMAIL_DOMAINS = []
def load_allowed_email_domains(filepath="allowed_email_domains.txt"):
    global ALLOWED_EMAIL_DOMAINS
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            ALLOWED_EMAIL_DOMAINS = [line.strip() for line in f if line.strip()]
    else:
        # Nếu không tìm thấy file, dùng mặc định
        ALLOWED_EMAIL_DOMAINS = ["@student.university.edu.vn"]

load_allowed_email_domains()

def validate_email(email):
    """
    Kiểm tra định dạng email hợp lệ và phải thuộc tên miền được cấu hình.
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email) is None:
        return False
    # Kiểm tra tên miền
    return any(email.endswith(domain) for domain in ALLOWED_EMAIL_DOMAINS)

# --- Cấu hình số điện thoại hợp lệ theo mẫu ---
ALLOWED_PHONE_PATTERNS = []
def load_allowed_phone_patterns(filepath="allowed_phone_patterns.txt"):
    global ALLOWED_PHONE_PATTERNS
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            ALLOWED_PHONE_PATTERNS = [line.strip() for line in f if line.strip()]
    else:
        # Mặc định cho Việt Nam: +84XXXXXXXXX hoặc 0[3|5|7|8|9]XXXXXXXX
        ALLOWED_PHONE_PATTERNS = [r'^\+84\d{9}$', r'^0[35789]\d{8}$']

load_allowed_phone_patterns()

def validate_phone(phone):
    """
    Kiểm tra số điện thoại theo các mẫu cấu hình (regex).
    """
    for pattern in ALLOWED_PHONE_PATTERNS:
        if re.fullmatch(pattern, phone):
            return True
    return False

def validate_date(date_str):
    """
    Kiểm tra định dạng ngày sinh theo dd/mm/yyyy.
    """
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def validate_index(input_str, max_index):
    """
    Kiểm tra chỉ số nhập vào có phải là số nguyên và nằm trong khoảng [0, max_index - 1].
    Nếu hợp lệ, trả về số nguyên; nếu không, trả về None.
    """
    try:
        index = int(input_str)
        if 0 <= index < max_index:
            return index
        else:
            return None
    except ValueError:
        return None

def validate_non_empty(value):
    """
    Kiểm tra giá trị không rỗng.
    """
    return value.strip() != ""

def validate_gender(gender):
    """
    Kiểm tra giới tính phải là 'Nam' hoặc 'Nữ'.
    """
    if gender.lower() in ['nam', 'nữ', 'nu']:
        return True
    return False

def validator_transition_states(from_status, to_status, rules):
    return to_status not in rules.get(from_status, set())
