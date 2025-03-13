import csv
import os
import json
import logging
from datetime import datetime
from validators import validate_email, validate_phone, validate_date, validate_index, validate_non_empty, validate_gender, validator_transition_states
import subprocess
from datetime import datetime
from datetime import timedelta 

logging.basicConfig(level=logging.INFO,
                    filename="app.log",
                    filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

CSV_FILE = 'students.csv'
CONFIG_FILE = 'overall_config.txt'

FACULTIES = ["Khoa Luật", "Khoa Tiếng Anh thương mại", "Khoa Tiếng Nhật", "Khoa Tiếng Pháp"]

def load_student_statuses(filepath="allowed_status_transitions.txt"):
    statuses = []
    rules = {}

    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        N = int(lines[0])
        statuses = lines[1:N+1]

        M = int(lines[N+1])
        rule_lines = lines[N+2:N+2+M]

        for rule in rule_lines:
            left, right = rule.split(" != ")
            rules[left.strip()] = {s.strip() for s in right.split(",") if s.strip()}
    else:
        statuses = ["Đang học", "Đã Tốt nghiệp", "Đã Thôi học", "Bảo lưu"]
        rules = {}

    return statuses, rules

STATUSES, RULES = load_student_statuses()

PROGRAMS = ["đại trà", "chất lượng cao", "tiên tiến", "việt pháp"]

students = []

def load_overall_config(filepath=CONFIG_FILE):
    """
    Đọc file cấu hình overall_config.txt
    """
    config = {}
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
    else:
        config['creation_time_limit_for_delete'] = '30'
        config['school_name'] = 'Trường Đại Học Bách Khoa'
    config.setdefault('school_address', '123 Đường A, Quận B, TP. HCM')
    config.setdefault('school_phone', '0123456789')
    config.setdefault('school_email', 'contact@123.edu.vn')
    return config


def load_students():
    global students
    students = []
    if os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if 'creation_time' not in row:
                        row['creation_time'] = ""
                    students.append(row)
            logging.info("Load dữ liệu sinh viên từ file CSV thành công.")
        except Exception as e:
            logging.error(f"Lỗi khi load dữ liệu từ CSV: {e}")

def save_students():
    global students
    try:
        with open(CSV_FILE, mode='w', encoding='utf-8', newline='') as file:
            fieldnames = ['mssv', 'ho_ten', 'ngay_sinh', 'gioi_tinh', 'khoa', 'khoa_hoc', 'chuong_trinh', 'dia_chi', 'email', 'so_dien_thoai', 'tinh_trang', 'creation_time']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for student in students:
                writer.writerow(student)
        logging.info("Lưu dữ liệu sinh viên vào file CSV thành công.")
    except Exception as e:
        logging.error(f"Lỗi khi lưu dữ liệu vào CSV: {e}")

def input_validated(prompt, validation_func, error_msg, transform_func=None):
    while True:
        value = input(prompt)
        if transform_func:
            value = transform_func(value)
        if validation_func(value):
            return value
        else:
            print(error_msg)

def input_index(prompt, options):
    while True:
        print(prompt)
        for idx, option in enumerate(options):
            print(f"{idx}: {option}")
        user_input = input("Chọn số tương ứng: ")
        index = validate_index(user_input, len(options))
        if index is not None:
            return options[index]
        else:
            print("Chỉ số không hợp lệ. Vui lòng nhập lại.")

def add_student():
    global students
    print("\n=== Thêm sinh viên mới ===")
    
    while True:
        mssv = input("Nhập MSSV: ").strip()
        if not validate_non_empty(mssv):
            print("MSSV không được để trống!")
            continue
        if any(s['mssv'] == mssv for s in students):
            print("MSSV đã tồn tại. Vui lòng nhập MSSV khác!")
        else:
            break
    
    ho_ten = input_validated("Nhập họ tên: ", validate_non_empty, "Họ tên không được để trống!")
    ngay_sinh = input_validated("Nhập ngày sinh (dd/mm/yyyy): ", validate_date, "Ngày sinh không hợp lệ! Vui lòng nhập theo định dạng dd/mm/yyyy.")
    
    while True:
        gioi_tinh = input("Nhập giới tính (Nam/Nữ): ").strip()
        if validate_gender(gioi_tinh):
            break
        else:
            print("Giới tính không hợp lệ. Vui lòng nhập 'Nam' hoặc 'Nữ'.")
    
    khoa = input_index("Chọn khoa:", FACULTIES)
    
    while True:
        khoa_hoc = input("Nhập khóa (năm): ").strip()
        if khoa_hoc.isdigit():
            break
        else:
            print("Khóa phải là số. Vui lòng nhập lại.")
    
    chuong_trinh = input_index("Chọn chương trình đào tạo:", PROGRAMS)
    
    dia_chi = input_validated("Nhập địa chỉ: ", validate_non_empty, "Địa chỉ không được để trống!")
    email = input_validated("Nhập email: ", validate_email, "Email không hợp lệ. Vui lòng nhập lại!")
    so_dien_thoai = input_validated("Nhập số điện thoại: ", validate_phone, "Số điện thoại không hợp lệ. Vui lòng nhập lại!")
    
    tinh_trang = input_index("Chọn tình trạng sinh viên:", STATUSES)

    creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    student = {
        'mssv': mssv,
        'ho_ten': ho_ten,
        'ngay_sinh': ngay_sinh,
        'gioi_tinh': gioi_tinh,
        'khoa': khoa,
        'khoa_hoc': khoa_hoc,
        'chuong_trinh': chuong_trinh,
        'dia_chi': dia_chi,
        'email': email,
        'so_dien_thoai': so_dien_thoai,
        'tinh_trang': tinh_trang,
        'creation_time': creation_time
    }
    
    students.append(student)
    print("Thêm sinh viên thành công!")
    logging.info(f"Thêm sinh viên: MSSV {mssv}")

def delete_student():
    global students
    print("\n=== Xóa sinh viên ===")
    mssv = input("Nhập MSSV của sinh viên cần xóa: ").strip()
    found = False
    for i, student in enumerate(students):
        if student['mssv'] == mssv:
            found = True
            if student.get('creation_time'):
                try:
                    creation_dt = datetime.strptime(student['creation_time'], "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    print("Dữ liệu thời gian tạo không hợp lệ, không thể xóa.")
                    logging.error(f"Thời gian tạo của sinh viên {mssv} không hợp lệ.")
                    return
                now = datetime.now()
                diff_minutes = (now - creation_dt).total_seconds() / 60
                config = load_overall_config()
                limit_minutes = float(config.get('creation_time_limit_for_delete', 30))
                if diff_minutes <= limit_minutes:
                    students.pop(i)
                    print("Xóa sinh viên thành công!")
                    logging.info(f"Xóa sinh viên: MSSV {mssv}")
                else:
                    print(f"Không thể xóa sinh viên. Thời gian tạo đã vượt quá giới hạn cho phép ({limit_minutes} phút).")
                    logging.info(f"Không xóa sinh viên {mssv}: đã vượt quá giới hạn {limit_minutes} phút (chênh lệch {diff_minutes:.2f} phút).")
            else:
                print("Không có thông tin thời gian tạo, không thể kiểm tra điều kiện xóa.")
            break
    if not found:
        print("Không tìm thấy sinh viên với MSSV đã nhập.")

def update_student():
    global students
    print("\n=== Cập nhật thông tin sinh viên ===")
    mssv = input("Nhập MSSV của sinh viên cần cập nhật: ").strip()
    student = None
    for s in students:
        if s['mssv'] == mssv:
            student = s
            break
    if student is None:
        print("Không tìm thấy sinh viên với MSSV đã nhập.")
        return
    
    print("Sinh viên tìm thấy:")
    print(student)
    print("Chọn thông tin cần cập nhật:")
    
    fields = ['ho_ten', 'ngay_sinh', 'gioi_tinh', 'khoa', 'khoa_hoc', 'chuong_trinh', 'dia_chi', 'email', 'so_dien_thoai', 'tinh_trang']
    field_names = {
        'ho_ten': "Họ tên",
        'ngay_sinh': "Ngày sinh",
        'gioi_tinh': "Giới tính",
        'khoa': "Khoa",
        'khoa_hoc': "Khóa",
        'chuong_trinh': "Chương trình đào tạo",
        'dia_chi': "Địa chỉ",
        'email': "Email",
        'so_dien_thoai': "Số điện thoại",
        'tinh_trang': "Tình trạng sinh viên"
    }
    
    for idx, field in enumerate(fields):
        print(f"{idx}: {field_names[field]}")
    
    try:
        choice = int(input("Chọn số tương ứng với thông tin cần cập nhật: "))
        if 0 <= choice < len(fields):
            field_to_update = fields[choice]
            if field_to_update == 'ho_ten':
                student['ho_ten'] = input_validated("Nhập họ tên mới: ", validate_non_empty, "Họ tên không được để trống!")
            elif field_to_update == 'ngay_sinh':
                student['ngay_sinh'] = input_validated("Nhập ngày sinh mới (dd/mm/yyyy): ", validate_date, "Ngày sinh không hợp lệ!")
            elif field_to_update == 'gioi_tinh':
                while True:
                    new_gender = input("Nhập giới tính mới (Nam/Nữ): ").strip()
                    if validate_gender(new_gender):
                        student['gioi_tinh'] = new_gender
                        break
                    else:
                        print("Giới tính không hợp lệ. Vui lòng nhập lại.")
            elif field_to_update == 'khoa':
                student['khoa'] = input_index("Chọn khoa mới:", FACULTIES)
            elif field_to_update == 'khoa_hoc':
                while True:
                    new_khoa_hoc = input("Nhập khóa mới (năm): ").strip()
                    if new_khoa_hoc.isdigit():
                        student['khoa_hoc'] = new_khoa_hoc
                        break
                    else:
                        print("Khóa phải là số. Vui lòng nhập lại.")
            elif field_to_update == 'chuong_trinh':
                student['chuong_trinh'] = input_index("Chọn chương trình đào tạo mới:", PROGRAMS)
            elif field_to_update == 'dia_chi':
                student['dia_chi'] = input_validated("Nhập địa chỉ mới: ", validate_non_empty, "Địa chỉ không được để trống!")
            elif field_to_update == 'email':
                student['email'] = input_validated("Nhập email mới: ", validate_email, "Email không hợp lệ!")
            elif field_to_update == 'so_dien_thoai':
                student['so_dien_thoai'] = input_validated("Nhập số điện thoại mới: ", validate_phone, "Số điện thoại không hợp lệ!")
            elif field_to_update == 'tinh_trang':
                new_status = input_index("Chọn tình trạng mới:", STATUSES)
                current_status = student['tinh_trang']
                if (validator_transition_states(current_status, new_status, RULES)):
                    
                    student['tinh_trang'] = new_status
                    print("Cập nhật tình trạng sinh viên thành công!")
                    logging.info(f"Cập nhật tình trạng: MSSV {mssv} chuyển từ '{current_status}' sang '{new_status}'")
                else:
                    print(f"Chuyển trạng thái từ '{current_status}' sang '{new_status}' không hợp lệ.")
                    logging.error(f"Thay đổi trạng thái không hợp lệ: '{current_status}' -> '{new_status}'")
        else:
            print("Lựa chọn không hợp lệ!")
    except ValueError:
        print("Lựa chọn không hợp lệ!")

def search_student():
    global students
    print("\n=== Tìm kiếm sinh viên ===")
    print("Tìm kiếm theo:")
    print("1: MSSV")
    print("2: Họ tên")
    choice = input("Chọn phương thức tìm kiếm (1 hoặc 2): ").strip()
    
    if choice == '1':
        mssv = input("Nhập MSSV cần tìm: ").strip()
        results = [s for s in students if s['mssv'] == mssv]
    elif choice == '2':
        ho_ten = input("Nhập họ tên cần tìm: ").strip().lower()
        results = [s for s in students if ho_ten in s['ho_ten'].lower()]
    else:
        print("Lựa chọn không hợp lệ!")
        return
    
    if results:
        print("Kết quả tìm kiếm:")
        for student in results:
            print(student)
    else:
        print("Không tìm thấy sinh viên nào.")

def search_by_faculty():
    global students
    print("\n=== Tìm kiếm theo Khoa ===")
    faculty = input_index("Chọn khoa cần tìm:", FACULTIES)
    results = [s for s in students if s['khoa'] == faculty]
    if results:
        print("Kết quả tìm kiếm:")
        for student in results:
            print(student)
    else:
        print("Không tìm thấy sinh viên nào trong khoa này.")

def search_by_faculty_and_name():
    global students
    print("\n=== Tìm kiếm theo Khoa và Tên sinh viên ===")
    faculty = input_index("Chọn khoa cần tìm:", FACULTIES)
    name = input("Nhập tên sinh viên cần tìm: ").strip().lower()
    results = [s for s in students if s['khoa'] == faculty and name in s['ho_ten'].lower()]
    if results:
        print("Kết quả tìm kiếm:")
        for student in results:
            print(student)
    else:
        print("Không tìm thấy sinh viên nào.")

def manage_categories():
    while True:
        print("\n=== Quản lý danh mục ===")
        print("1: Quản lý Khoa (Faculty)")
        print("2: Quản lý Tình trạng sinh viên (Student Status)")
        print("3: Quản lý Chương trình đào tạo (Program)")
        print("4: Quay lại menu chính")
        choice = input("Chọn chức năng (1-4): ").strip()
        if choice == '1':
            manage_list("Khoa", FACULTIES)
        elif choice == '2':
            manage_list("Tình trạng sinh viên", STATUSES)
        elif choice == '3':
            manage_list("Chương trình đào tạo", PROGRAMS)
        elif choice == '4':
            break
        else:
            print("Lựa chọn không hợp lệ!")

def manage_list(name, category_list):
    while True:
        print(f"\n--- Quản lý {name} ---")
        print("Danh sách hiện tại:")
        for idx, item in enumerate(category_list):
            print(f"{idx}: {item}")
        print("1: Đổi tên mục đã có")
        print("2: Thêm mới mục")
        print("3: Quay lại")
        choice = input("Chọn chức năng (1-3): ").strip()
        if choice == '1':
            idx_input = input("Nhập chỉ số của mục cần đổi tên: ").strip()
            index = validate_index(idx_input, len(category_list))
            if index is not None:
                new_name = input("Nhập tên mới: ").strip()
                if new_name != "":
                    category_list[index] = new_name
                    print(f"Đã đổi tên mục {index} thành {new_name}.")
                    logging.info(f"Đổi tên danh mục {name}: mục {index} thành {new_name}")
                else:
                    print("Tên không được để trống!")
            else:
                print("Chỉ số không hợp lệ!")
        elif choice == '2':
            new_item = input("Nhập tên mục mới cần thêm: ").strip()
            if new_item != "":
                category_list.append(new_item)
                print(f"Đã thêm mục mới: {new_item}.")
                logging.info(f"Thêm mới vào danh mục {name}: {new_item}")
            else:
                print("Tên không được để trống!")
        elif choice == '3':
            break
        else:
            print("Lựa chọn không hợp lệ!")

def import_data():
    global students
    print("\n=== Import Dữ liệu ===")
    print("Chọn định dạng file để import:")
    print("1: CSV")
    print("2: JSON")
    choice = input("Chọn (1 hoặc 2): ").strip()
    imported_students = []
    
    if choice == "1":
        file_path = input("Nhập đường dẫn file CSV: ").strip()
        if os.path.exists(file_path):
            try:
                with open(file_path, mode='r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    imported_students = list(reader)
                logging.info(f"Import dữ liệu từ CSV: {file_path}")
            except Exception as e:
                print(f"Lỗi khi import CSV: {e}")
                logging.error(f"Lỗi import CSV {file_path}: {e}")
                return
        else:
            print("File không tồn tại.")
            return
    elif choice == "2":
        file_path = input("Nhập đường dẫn file JSON: ").strip()
        if os.path.exists(file_path):
            try:
                with open(file_path, mode='r', encoding='utf-8') as file:
                    imported_students = json.load(file)
                logging.info(f"Import dữ liệu từ JSON: {file_path}")
            except Exception as e:
                print(f"Lỗi khi import JSON: {e}")
                logging.error(f"Lỗi import JSON {file_path}: {e}")
                return
        else:
            print("File không tồn tại.")
            return
    else:
        print("Lựa chọn không hợp lệ!")
        return

    count_added = 0
    count_skipped = 0
    for imp_student in imported_students:
        duplicate = False
        for existing_student in students:
            if imp_student.get('mssv') == existing_student.get('mssv'):
                duplicate = True
                break
        if not duplicate:
            if 'creation_time' not in imp_student or not imp_student['creation_time']:
                imp_student['creation_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            students.append(imp_student)
            count_added += 1
        else:
            count_skipped += 1

    print(f"Import hoàn thành: {count_added} sinh viên được thêm, {count_skipped} sinh viên bị trùng và không được thêm.")
    logging.info(f"Import dữ liệu: {count_added} thêm, {count_skipped} bị trùng.")

def export_data_json():
    global students
    print("\n=== Export Dữ liệu ra JSON ===")
    file_path = input("Nhập đường dẫn file JSON để lưu (ví dụ: export.json): ").strip()
    try:
        with open(file_path, mode='w', encoding='utf-8') as file:
            json.dump(students, file, ensure_ascii=False, indent=4)
        print("Export dữ liệu ra JSON thành công.")
        logging.info(f"Export dữ liệu ra JSON: {file_path}")
    except Exception as e:
        print(f"Lỗi khi export dữ liệu: {e}")
        logging.error(f"Lỗi export JSON {file_path}: {e}")


def get_git_version():
    try:
        version = subprocess.check_output(["git", "describe", "--tags"], stderr=subprocess.DEVNULL).strip().decode()
        return version
    except subprocess.CalledProcessError:
        return "unknown"
    
def save_build_time():
    build_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("build_info.txt", "w") as f:
        f.write(f"{build_time}\n")

def read_build_info():
    try:
        with open("build_info.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "No build info available"
    
def show_version():
    print("\n=== Phiên bản và Ngày Build ===")
    version = get_git_version()
    build_date = read_build_info()
    print(f"Version Hiện tại: {version}")    
    print(f"Ngày build gần nhất: {build_date}")
    logging.info("Hiển thị version và ngày build")

def export_status_confirmation():
    """
    Xuất giấy xác nhận tình trạng sinh viên ra HTML hoặc Markdown.
    Nội dung bao gồm phần header chứa thông tin trường (tên, địa chỉ, điện thoại, email)
    và phần nội dung xác nhận với các thông tin sinh viên, mục đích xác nhận (chọn từ 4 mục)
    và thời gian cấp giấy (ngày hiện tại và hiệu lực đến 30 ngày sau).
    """
    print("\n=== Xuất giấy xác nhận tình trạng sinh viên ===")
    mssv = input("Nhập MSSV của sinh viên cần xuất giấy xác nhận: ").strip()
    student = None
    for s in students:
        if s['mssv'] == mssv:
            student = s
            break
    if student is None:
        print("Không tìm thấy sinh viên với MSSV đã nhập.")
        return

    # Yêu cầu chọn mục đích xác nhận
    print("Chọn mục đích xác nhận:")
    print("0: Xác nhận đang học để vay vốn ngân hàng")
    print("1: Xác nhận làm thủ tục tạm hoãn nghĩa vụ quân sự")
    print("2: Xác nhận làm hồ sơ xin việc / thực tập")
    print("3: Xác nhận lý do khác")
    option = input("Chọn (0-3): ").strip()
    if option == "3":
        purpose = "Xác nhận lý do khác: " + input("Nhập lý do xác nhận: ")
    elif option == "0":
        purpose = "Xác nhận đang học để vay vốn ngân hàng"
    elif option == "1":
        purpose = "Xác nhận làm thủ tục tạm hoãn nghĩa vụ quân sự"
    elif option == "2":
        purpose = "Xác nhận làm hồ sơ xin việc / thực tập"
    else:
        print("Lựa chọn không hợp lệ, sử dụng mặc định: Xác nhận đang học để vay vốn ngân hàng")
        purpose = "Xác nhận đang học để vay vốn ngân hàng"

    # Tính toán ngày cấp và hiệu lực (30 ngày kể từ hôm nay)
    issue_date = datetime.now().strftime('%d/%m/%Y')
    effective_date = (datetime.now() + timedelta(days=30)).strftime('%d/%m/%Y')

    # Đọc thông tin trường từ file cấu hình
    config = load_overall_config()
    school_name = config.get('school_name', 'Trường Đại Học Demo')
    school_address = config.get('school_address', '123 Đường ABC, Quận XYZ, TP. HCM')
    school_phone = config.get('school_phone', '0123456789')
    school_email = config.get('school_email', 'contact@demo.edu.vn')

    # Chuẩn bị nội dung header và nội dung xác nhận chung
    header_text = (
        f"TRƯỜNG ĐẠI HỌC {school_name}\n"
        f"PHÒNG ĐÀO TẠO\n"
        f"📍 Địa chỉ: {school_address}\n"
        f"📞 Điện thoại: {school_phone} | 📧 Email: {school_email}"
    )

    student_info = (
        f"Họ và tên: {student['ho_ten']}\n"
        f"Mã số sinh viên: {student['mssv']}\n"
        f"Ngày sinh: {student['ngay_sinh']}\n"
        f"Giới tính: {student['gioi_tinh']}\n"
        f"Khoa: {student['khoa']}\n"
        f"Chương trình đào tạo: {student['chuong_trinh']}\n"
        f"Khóa: K{student['khoa_hoc']} - Năm nhập học"
    )

    content_text = (
        f"GIẤY XÁC NHẬN TÌNH TRẠNG SINH VIÊN\n"
        f"Trường Đại học {school_name} xác nhận:\n\n"
        f"1. Thông tin sinh viên:\n\n"
        f"{student_info}\n\n"
        f"2. Tình trạng sinh viên hiện tại:\n\n"
        f"{student['tinh_trang']}\n\n"
        f"3. Mục đích xác nhận:\n\n"
        f"{purpose}\n\n"
        f"4. Thời gian cấp giấy:\n\n"
        f"Giấy xác nhận có hiệu lực đến ngày: {effective_date} (1 tháng)\n"
        f"📍 Xác nhận của Trường Đại học {school_name}\n\n"
        f"📅 Ngày cấp: {issue_date}\n\n"
        f"🖋 Trưởng Phòng Đào Tạo\n"
        f"(Ký, ghi rõ họ tên, đóng dấu)"
    )

    # Yêu cầu chọn định dạng xuất file
    print("Chọn định dạng xuất:")
    print("1: HTML")
    print("2: Markdown")
    choice = input("Chọn (1 hoặc 2): ").strip()
    output_path = input("Nhập đường dẫn file xuất (ví dụ: confirmation.html hoặc confirmation.md): ").strip()

    try:
        if choice == '1':
            # Xuất ra HTML với style cải tiến
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Giấy Xác Nhận Tình Trạng Sinh Viên</title>
    <style>
        body {{
            background-color: #e0e0e0;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #ffffff;
            border: 1px solid #ccc;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}
        .header, .content {{
            text-align: center;
            margin-bottom: 20px;
        }}
        hr {{
            border: 0;
            border-top: 1px solid #ccc;
            margin: 20px 0;
        }}
        pre {{
            text-align: left;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <pre>{header_text}</pre>
        </div>
        <hr>
        <div class="content">
            <pre>{content_text}</pre>
        </div>
    </div>
</body>
</html>"""
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print("Xuất giấy xác nhận ra file HTML thành công.")
            logging.info(f"Xuất giấy xác nhận ra HTML: {output_path}")
        elif choice == '2':
            md_content = (
                f"# TRƯỜNG ĐẠI HỌC {school_name}\n"
                f"**PHÒNG ĐÀO TẠO**\n\n"
                f"**📍 Địa chỉ:** {school_address}\n"
                f"**📞 Điện thoại:** {school_phone} | **📧 Email:** {school_email}\n\n"
                f"---\n\n"
                f"# GIẤY XÁC NHẬN TÌNH TRẠNG SINH VIÊN\n\n"
                f"Trường Đại học {school_name} xác nhận:\n\n"
                f"### 1. Thông tin sinh viên:\n\n"
                f"- Họ và tên: {student['ho_ten']}\n"
                f"- Mã số sinh viên: {student['mssv']}\n"
                f"- Ngày sinh: {student['ngay_sinh']}\n"
                f"- Giới tính: {student['gioi_tinh']}\n"
                f"- Khoa: {student['khoa']}\n"
                f"- Chương trình đào tạo: {student['chuong_trinh']}\n"
                f"- Khóa: K{student['khoa_hoc']} - Năm nhập học\n\n"
                f"### 2. Tình trạng sinh viên hiện tại:\n\n"
                f"{student['tinh_trang']}\n\n"
                f"### 3. Mục đích xác nhận:\n\n"
                f"{purpose}\n\n"
                f"### 4. Thời gian cấp giấy:\n\n"
                f"- Giấy xác nhận có hiệu lực đến ngày: {effective_date} (1 tháng)\n"
                f"- 📍 Xác nhận của Trường Đại học {school_name}\n"
                f"- 📅 Ngày cấp: {issue_date}\n\n"
                f"🖋 **Trưởng Phòng Đào Tạo**\n"
                f"(Ký, ghi rõ họ tên, đóng dấu)"
            )
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            print("Xuất giấy xác nhận ra file Markdown thành công.")
            logging.info(f"Xuất giấy xác nhận ra Markdown: {output_path}")
        else:
            print("Lựa chọn không hợp lệ!")
    except Exception as e:
        print(f"Lỗi khi xuất giấy xác nhận: {e}")
        logging.error(f"Lỗi khi xuất giấy xác nhận: {e}")



def main_menu():
    """
    Menu chính của chương trình.
    Khi khởi động, load dữ liệu vào biến toàn cục.
    Khi thoát, lưu dữ liệu vào file CSV.
    """
    save_build_time()
    load_students()
    config = load_overall_config()
    school_name = config.get('school_name', 'Trường Đại Học Bách Khoa')
    
    print(f"Chào mừng đến với hệ thống quản lý sinh viên - {school_name}")
    
    while True:
        print("\n===== Quản lý danh sách sinh viên =====")
        print("1: Thêm sinh viên")
        print("2: Xóa sinh viên")
        print("3: Cập nhật thông tin sinh viên")
        print("4: Tìm kiếm sinh viên (MSSV hoặc Họ tên)")
        print("5: Tìm kiếm theo Khoa")
        print("6: Tìm kiếm theo Khoa và Tên sinh viên")
        print("7: Quản lý danh mục (Khoa, Tình trạng, Chương trình)")
        print("8: Import dữ liệu (CSV/JSON)")
        print("9: Export dữ liệu ra JSON")
        print("10: Hiển thị version và ngày build")
        print("11: Xuất giấy xác nhận tình trạng sinh viên (HTML/Markdown)")
        print("12: Thoát")
        
        choice = input("Chọn chức năng (1-12): ").strip()
        
        if choice == '1':
            add_student()
        elif choice == '2':
            delete_student()
        elif choice == '3':
            update_student()
        elif choice == '4':
            search_student()
        elif choice == '5':
            search_by_faculty()
        elif choice == '6':
            search_by_faculty_and_name()
        elif choice == '7':
            manage_categories()
        elif choice == '8':
            import_data()
        elif choice == '9':
            export_data_json()
        elif choice == '10':
            show_version()
        elif choice == '11':
            export_status_confirmation()
        elif choice == '12':
            save_students()
            print("Kết thúc chương trình và lưu dữ liệu.")
            logging.info("Thoát ứng dụng")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

if __name__ == "__main__":
    main_menu()
