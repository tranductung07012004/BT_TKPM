#include "student_manager.h"
#include <iostream>
#include <algorithm>
#include <regex>
studentManager& studentManager::getInstance() {
  static studentManager instance;
  return instance;
}

bool isValidEmail(const string& email) {
  const regex pattern(R"(^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$)");
  return regex_match(email, pattern);
}

bool isValidPhoneNumber(const string& phone) {
  const regex pattern(R"(^(\+84|0)[0-9]{9,10}$)");
  return regex_match(phone, pattern);
}

student studentManager::inputStudent() {
  student input;
  cout << "Nhập mssv: "; cin >> input._mssv;
  cin.ignore();
  cout << "Nhập họ tên: "; getline(cin, input._hoten);
  cout << "Nhập ngày tháng năm sinh: "; cin >> input._dob;
  cout << "Nhập vào giới tính: "; cin >> input._gioitinh;
  
  bool validInputKhoa = true;
  do {
    cout << "Nhập vào khoa: \n"
        << "0. Khoa luật \n"
        << "1. Khoa Tiếng anh thương mại \n"
        << "2. Khoa tiếng Nhật \n"
        << "3. Khoa tiếng Pháp \n";
    
    string khoa_temp;
    cin >> khoa_temp;
    try {
      input._khoa = stoi(khoa_temp);
      validInputKhoa = true;

    } catch (const invalid_argument& e){
      cout << "Nhập thông tin \"khoa\" không hợp lệ, hãy nhập số từ 0 đến 3 \n";
      validInputKhoa = false;
    } catch (const out_of_range& e) {
      cout << "Số out of range integer \n";
      validInputKhoa = false;
    }
  } while (validInputKhoa == false
           || (input._khoa != 0 
            && input._khoa != 1 
            && input._khoa != 2 
            && input._khoa != 3));
  cout << "Nhập vào khóa (số hoặc ký tự không cách): "; cin >> input._k;
  cin.ignore();
  cout << "Nhập vào chương trình: "; getline(cin, input._chuongtrinh);
  cout << "Nhập vào địa chỉ: "; getline(cin, input._diachi);

  bool validEmail = true;
  do {
    cout << "Nhập vào email: "; cin >> input._email;
    validEmail = isValidEmail(input._email);
    if (!validEmail) 
      cout << "Email sai định dạng, hãy nhập lại email!";
  } while(!validEmail);

  bool validPhone = true;
  do {
    cout << "Nhập vào số điện thoại: "; cin >> input._sdt;
    validPhone = isValidPhoneNumber(input._sdt);
    if (!validPhone) 
      cout << "Số điện thoại sai định dạng, hãy nhập lại!";
  } while(!validPhone);

  bool validInputTT = true;
  do {
    cout << "Nhập vào tình trạng sinh viên: \n"
        << "0. Đang học \n"
        << "1. Đã tốt nghiệp \n"
        << "2. Đã thôi học \n"
        << "3. Tạm dừng học \n"; 
    
    string TT_temp;
    cin >> TT_temp;
    try {
      input._tinhtrang = stoi(TT_temp);
      validInputTT = true;
    } catch (const invalid_argument& e){
      cout << "Nhập thông tin \"khoa\" không hợp lệ, hãy nhập số từ 0 đến 3 \n";
      validInputTT = false;
    } catch (const out_of_range& e) {
      cout << "Số out of range integer \n";
      validInputTT = false;
    }
  } while (validInputTT == false
           || (input._tinhtrang != 0 
            && input._tinhtrang != 1 
            && input._tinhtrang != 2 
            && input._tinhtrang != 3));

  return input;
}
void studentManager::addStudent(const student& s) {
  this->students.push_back(s);
  cout << '\n' << "Đã thêm sinh viên." << '\n';
}

void studentManager::removeStudent(const string& id) {
  for (auto it = this->students.begin(); it != this->students.end(); it++) {
    if ((*it)._mssv == id) {
      cout << "Đã xóa sinh viên có mssv là: " << id << '\n';
      break;
    }
  }
  cout << "Không có sinh viên có mssv là: " << id << "trong danh sách" << '\n';
}
void studentManager::updateStudent(const std::string& id, const student& newInfo) {
  for (auto& student: this->students) {
    if (student._mssv == id) {
      student = newInfo;
      std::cout << "Cập nhật thành công thông tin sinh viên có mssv: " << id << '\n'; 
      return;
    }
  }
  std::cout << "Không tìm thấy sinh viên để cập nhật \n";
}

void studentManager::findStudent(const std::string& keyword) {
  bool found = false;
  for (const auto& student: this->students) {
    if (student._mssv == keyword || student._hoten.find(keyword) != std::string::npos) {
      student.display();
      found = true;
    }
  }
  if (!found) {
    std::cout << "Không tìm thấy sinh viên \n";
  }
}
void studentManager::displayAll() {
  if (this->students.empty()) {
    cout << "Hiện tại chưa có sinh viên nào!" << '\n';
  } else {
    for (const auto& student : students) {
      student.display();
    }
  }
}