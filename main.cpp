#include "student_manager.h"
#include <iostream>

int main() {
    studentManager& manager = studentManager::getInstance();
    char choice;
    
    do {
        std::cout << "\n===== Quản lý sinh viên =====\n";
        std::cout << "1. Thêm sinh viên\n";
        std::cout << "2. Xóa sinh viên\n";
        std::cout << "3. Cập nhật sinh viên\n";
        std::cout << "4. Tìm kiếm sinh viên\n";
        std::cout << "5. Hiển thị danh sách sinh viên\n";
        std::cout << "6. Thoát\n";
        std::cout << "Chọn chức năng: ";
        std::cin >> choice;
        std::cin.ignore();

        switch (choice) {
            case '1': {
                student s = studentManager::inputStudent();
                manager.addStudent(s);
                break;
            }
            case '2': {
                std::string id;
                std::cout << "Nhập MSSV cần xóa: ";
                std::getline(std::cin, id);
                manager.removeStudent(id);
                break;
            }
            case '3': {
                student newInfo = studentManager::inputStudent();
                string id = newInfo._mssv; // id của sinh viên cần cập nhật thông tin
                manager.updateStudent(id, newInfo);
                break;
            }
            case '4': {
                std::string keyword;
                std::cout << "Nhập MSSV hoặc họ tên: ";
                std::getline(std::cin, keyword);
                manager.findStudent(keyword);
                break;
            }
            case '5': {
                manager.displayAll();
                break;
            }
            case '6':
                std::cout << "Thoát chương trình.\n";
                break;
            default:
                std::cout << "Lựa chọn không hợp lệ!\n";
        }
    } while (choice != '6');

    return 0;
}
