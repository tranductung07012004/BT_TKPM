#include "student.h"

void student::display() const {
  cout << "MSSV: " << _mssv << ","
       << "Họ tên: " << _hoten << ","
       << "Số điện thoại: " << _sdt << ","
       << "Chương trình: " << _chuongtrinh << ","
       << "Tình trạng: " <<  tinh_trang[_tinhtrang] << '\n'; 
}