import re
from datetime import datetime

def validate_email(email):
    """
    Kiểm tra định dạng email hợp lệ.
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """
    Kiểm tra số điện thoại chỉ chứa chữ số và có độ dài từ 9 đến 12 ký tự.
    """
    return phone.isdigit() and (9 <= len(phone) <= 12)

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
