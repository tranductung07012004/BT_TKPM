#ifndef _student_
#define _student_

#include <iostream>
#include <string>
using namespace std;


const string ten_khoa[] = {"Luật", "Tiếng anh thương mại", "Tiếng Nhật", "Tiếng Pháp"};
const string tinh_trang[] = {"Đang học", "Đã tốt nghiệp", "Đã thôi học", "Tạm dừng học"};

struct student {
  string _mssv;
  string _hoten;
  string _dob;
  string _gioitinh;
  int _khoa;
  string _k;
  string _chuongtrinh;
  string _diachi;
  string _email;
  string _sdt;
  int _tinhtrang;

  void display() const;
};


#endif