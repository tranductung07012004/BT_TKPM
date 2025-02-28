import unittest
from unittest.mock import patch
import io
import os
import tempfile
import json
import csv
import app

class TestApp(unittest.TestCase):
    def setUp(self):
        app.students = []
        app.STATUSES = ["Đang học", "Bảo lưu", "Tốt nghiệp", "Đình chỉ", "Đã tốt nghiệp"]

    @patch('builtins.input', side_effect=[
        "123", "Nguyen Van A", "01/01/2000", "Nam", "0", "2022", "1", 
        "Some Address", "user@student.hcmus.edu.vn", "0351234567", "0"
    ])
    def test_add_student(self, mock_inputs):
        app.add_student()
        self.assertEqual(len(app.students), 1)
        student = app.students[0]
        self.assertEqual(student['mssv'], "123")
        self.assertEqual(student['ho_ten'], "Nguyen Van A")
        self.assertEqual(student['tinh_trang'], "Đang học")

    @patch('builtins.input', side_effect=["123"])
    def test_delete_student(self, mock_inputs):
        app.students.append({
            'mssv': "123",
            'ho_ten': "Test Student",
            'ngay_sinh': "01/01/2000",
            'gioi_tinh': "Nam",
            'khoa': "Khoa Luật",
            'khoa_hoc': "2022",
            'chuong_trinh': "đại trà",
            'dia_chi': "Address",
            'email': "user@student.hcmus.edu.vn",
            'so_dien_thoai': "0351234567",
            'tinh_trang': "Đang học"
        })
        app.delete_student()
        self.assertEqual(len(app.students), 0)

    @patch('builtins.input', side_effect=["456", "9", "0"])
    def test_update_student_invalid_status_change(self, mock_inputs):
        app.students.append({
            'mssv': "456",
            'ho_ten': "Tran Thi B",
            'ngay_sinh': "02/02/2000",
            'gioi_tinh': "Nữ",
            'khoa': "Khoa Tiếng Nhật",
            'khoa_hoc': "2020",
            'chuong_trinh': "tiên tiến",
            'dia_chi': "Address 2",
            'email': "user2@student.hcmus.edu.vn",
            'so_dien_thoai': "0351234567",
            'tinh_trang': "Đã tốt nghiệp"
        })
        app.update_student()
        self.assertEqual(app.students[0]['tinh_trang'], "Đã tốt nghiệp")

    @patch('builtins.input', side_effect=["789", "9", "1"])
    def test_update_student_valid_status_change(self, mock_inputs):
        app.students.append({
            'mssv': "789",
            'ho_ten': "Le Van C",
            'ngay_sinh': "03/03/2000",
            'gioi_tinh': "Nam",
            'khoa': "Khoa Tiếng Anh thương mại",
            'khoa_hoc': "2021",
            'chuong_trinh': "đại trà",
            'dia_chi': "Address 3",
            'email': "user3@student.hcmus.edu.vn",
            'so_dien_thoai': "0351234567",
            'tinh_trang': "Đang học"
        })
        app.update_student()
        self.assertEqual(app.students[0]['tinh_trang'], "Bảo lưu")

    @patch('builtins.input', side_effect=["1", "123"])
    def test_search_student_by_mssv(self, mock_inputs):
        app.students.append({
            'mssv': "123",
            'ho_ten': "Student One",
            'ngay_sinh': "01/01/2000",
            'gioi_tinh': "Nam",
            'khoa': "Khoa Luật",
            'khoa_hoc': "2022",
            'chuong_trinh': "đại trà",
            'dia_chi': "Address",
            'email': "user1@student.hcmus.edu.vn",
            'so_dien_thoai': "0351234567",
            'tinh_trang': "Đang học"
        })
        captured_output = io.StringIO()
        with patch('sys.stdout', new=captured_output):
            app.search_student()
        self.assertIn("Student One", captured_output.getvalue())

    @patch('builtins.input', side_effect=["2", "student"])
    def test_search_student_by_name(self, mock_inputs):
        app.students.append({
            'mssv': "123",
            'ho_ten': "Student One",
            'ngay_sinh': "01/01/2000",
            'gioi_tinh': "Nam",
            'khoa': "Khoa Luật",
            'khoa_hoc': "2022",
            'chuong_trinh': "đại trà",
            'dia_chi': "Address",
            'email': "user1@student.hcmus.edu.vn",
            'so_dien_thoai': "0351234567",
            'tinh_trang': "Đang học"
        })
        captured_output = io.StringIO()
        with patch('sys.stdout', new=captured_output):
            app.search_student()
        self.assertIn("Student One", captured_output.getvalue())

    @patch('builtins.input', side_effect=["0"])
    def test_search_by_faculty(self, mock_inputs):
        app.students.append({
            'mssv': "123",
            'ho_ten': "Student One",
            'ngay_sinh': "01/01/2000",
            'gioi_tinh': "Nam",
            'khoa': "Khoa Luật",
            'khoa_hoc': "2022",
            'chuong_trinh': "đại trà",
            'dia_chi': "Address",
            'email': "user1@student.hcmus.edu.vn",
            'so_dien_thoai': "0351234567",
            'tinh_trang': "Đang học"
        })
        captured_output = io.StringIO()
        with patch('sys.stdout', new=captured_output):
            app.search_by_faculty()
        self.assertIn("Student One", captured_output.getvalue())

    @patch('builtins.input', side_effect=["0", "Student"])
    def test_search_by_faculty_and_name(self, mock_inputs):
        app.students.append({
            'mssv': "123",
            'ho_ten': "Student One",
            'ngay_sinh': "01/01/2000",
            'gioi_tinh': "Nam",
            'khoa': "Khoa Luật",
            'khoa_hoc': "2022",
            'chuong_trinh': "đại trà",
            'dia_chi': "Address",
            'email': "user1@student.hcmus.edu.vn",
            'so_dien_thoai': "0351234567",
            'tinh_trang': "Đang học"
        })
        captured_output = io.StringIO()
        with patch('sys.stdout', new=captured_output):
            app.search_by_faculty_and_name()
        self.assertIn("Student One", captured_output.getvalue())

    @patch('builtins.input', side_effect=["2", "1", "0", "New Status", "3"])
    def test_manage_categories(self, mock_inputs):
        captured_output = io.StringIO()
        with patch('sys.stdout', new=captured_output):
            app.manage_categories()
        self.assertIn("New Status", app.STATUSES)

    def test_import_data_csv(self):
        fd, temp_csv = tempfile.mkstemp(suffix=".csv", text=True)
        os.close(fd)
        data = [
            {'mssv': "111", 'ho_ten': "CSV Student", 'ngay_sinh': "04/04/2000", 'gioi_tinh': "Nam", 'khoa': "Khoa Luật",
             'khoa_hoc': "2022", 'chuong_trinh': "đại trà", 'dia_chi': "Address CSV", 'email': "csv@student.hcmus.edu.vn",
             'so_dien_thoai': "0351234567", 'tinh_trang': "Đang học"}
        ]
        with open(temp_csv, "w", encoding="utf-8", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        with patch('builtins.input', side_effect=["1", temp_csv]):
            app.import_data()
        self.assertEqual(len(app.students), 1)
        os.remove(temp_csv)

    def test_import_data_json(self):
        fd, temp_json = tempfile.mkstemp(suffix=".json", text=True)
        os.close(fd)
        data = [{
            'mssv': "222", 'ho_ten': "JSON Student", 'ngay_sinh': "05/05/2000", 'gioi_tinh': "Nữ", 'khoa': "Khoa Tiếng Nhật",
            'khoa_hoc': "2021", 'chuong_trinh': "tiên tiến", 'dia_chi': "Address JSON", 'email': "json@student.hcmus.edu.vn",
            'so_dien_thoai': "0351234567", 'tinh_trang': "Đang học"
        }]
        with open(temp_json, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        with patch('builtins.input', side_effect=["2", temp_json]):
            app.import_data()
        self.assertEqual(len(app.students), 1)
        os.remove(temp_json)

    def test_export_data_json(self):
        app.students.append({
            'mssv': "333",
            'ho_ten': "Export Student",
            'ngay_sinh': "06/06/2000",
            'gioi_tinh': "Nam",
            'khoa': "Khoa Tiếng Anh thương mại",
            'khoa_hoc': "2023",
            'chuong_trinh': "chất lượng cao",
            'dia_chi': "Address Export",
            'email': "export@student.hcmus.edu.vn",
            'so_dien_thoai': "0351234567",
            'tinh_trang': "Đang học"
        })
        fd, temp_export = tempfile.mkstemp(suffix=".json", text=True)
        os.close(fd)
        with patch('builtins.input', side_effect=[temp_export]):
            app.export_data_json()
        with open(temp_export, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)
        os.remove(temp_export)

    def test_show_version(self):
        captured_output = io.StringIO()
        with patch('sys.stdout', new=captured_output):
            app.show_version()
        output = captured_output.getvalue()
        self.assertIn(app.VERSION, output)
        self.assertIn(app.BUILD_DATE, output)

if __name__ == '__main__':
    unittest.main()
