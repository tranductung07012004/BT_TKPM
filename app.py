import csv
import os
import json
import logging
from datetime import datetime
from validators import validate_email, validate_phone, validate_date, validate_index, validate_non_empty, validate_gender

logging.basicConfig(level=logging.INFO,
                    filename="app.log",
                    filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

VERSION = "2.0.0"
BUILD_DATE = "2025-02-21"

CSV_FILE = 'students.csv'

FACULTIES = ["Khoa Luật", "Khoa Tiếng Anh thương mại", "Khoa Tiếng Nhật", "Khoa Tiếng Pháp"]

def load_student_statuses(filepath="allowed_status_transitions.txt"):
    statuses = []
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            statuses = [line.strip() for line in f if line.strip()]
    else:
        statuses = ["Đang học", "Đã tốt nghiệp", "Đã thôi học", "Tạm dừng học"]
    return statuses

STATUSES = load_student_statuses()

PROGRAMS = ["đại trà", "chất lượng cao", "tiên tiến", "việt pháp"]

students = []

def load_students():
    global students
    students = []
    if os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    students.append(row)
            logging.info("Load dữ liệu sinh viên từ file CSV thành công.")
        except Exception as e:
            logging.error(f"Lỗi khi load dữ liệu từ CSV: {e}")

def save_students():
    global students
    try:
        with open(CSV_FILE, mode='w', encoding='utf-8', newline='') as file:
            fieldnames = ['mssv', 'ho_ten', 'ngay_sinh', 'gioi_tinh', 'khoa', 'khoa_hoc', 'chuong_trinh', 'dia_chi', 'email', 'so_dien_thoai', 'tinh_trang']
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
        'tinh_trang': tinh_trang
    }
    
    students.append(student)
    print("Thêm sinh viên thành công!")
    logging.info(f"Thêm sinh viên: MSSV {mssv}")

def delete_student():
    global students
    print("\n=== Xóa sinh viên ===")
    mssv = input("Nhập MSSV của sinh viên cần xóa: ").strip()
    new_students = [s for s in students if s['mssv'] != mssv]
    if len(new_students) == len(students):
        print("Không tìm thấy sinh viên với MSSV đã nhập.")
    else:
        students[:] = new_students
        print("Xóa sinh viên thành công!")
        logging.info(f"Xóa sinh viên: MSSV {mssv}")

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
                if current_status == "Đang học":
                    if new_status in ["Bảo lưu", "Đã Tốt nghiệp", "Thôi học"]:
                        student['tinh_trang'] = new_status
                        print("Cập nhật tình trạng sinh viên thành công!")
                        logging.info(f"Cập nhật tình trạng: MSSV {mssv} chuyển từ '{current_status}' sang '{new_status}'")
                    else:
                        print(f"Chuyển trạng thái từ '{current_status}' sang '{new_status}' không hợp lệ theo quy tắc.")
                        logging.error(f"Thay đổi trạng thái không hợp lệ: '{current_status}' -> '{new_status}'")
                elif current_status.lower() == "đã tốt nghiệp":
                    if new_status == "Đang học":
                        print(f"Chuyển trạng thái từ '{current_status}' sang '{new_status}' không hợp lệ.")
                        logging.error(f"Thay đổi trạng thái không hợp lệ: '{current_status}' -> '{new_status}'")
                    else:
                        student['tinh_trang'] = new_status
                        print("Cập nhật tình trạng sinh viên thành công!")
                        logging.info(f"Cập nhật tình trạng: MSSV {mssv} chuyển từ '{current_status}' sang '{new_status}'")
                else:
                    student['tinh_trang'] = new_status
                    print("Cập nhật tình trạng sinh viên thành công!")
                    logging.info(f"Cập nhật tình trạng: MSSV {mssv} chuyển từ '{current_status}' sang '{new_status}'")
            
            if field_to_update != 'tinh_trang':
                print("Cập nhật sinh viên thành công!")
                logging.info(f"Cập nhật sinh viên: MSSV {mssv} - trường {field_to_update}")
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

def show_version():
    print("\n=== Phiên bản và Ngày Build ===")
    print(f"Version: {VERSION}")
    print(f"Build Date: {BUILD_DATE}")
    logging.info("Hiển thị version và ngày build")

def main_menu():
    """
    Menu chính của chương trình.
    Khi khởi động, load dữ liệu vào biến toàn cục.
    Khi thoát, lưu dữ liệu vào file CSV.
    """
    load_students() 
    
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
        print("11: Thoát")
        
        choice = input("Chọn chức năng (1-11): ").strip()
        
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
            save_students()
            print("Kết thúc chương trình và lưu dữ liệu.")
            logging.info("Thoát ứng dụng")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

if __name__ == "__main__":
    main_menu()
