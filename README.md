1. Chương trình sử dụng ngôn ngữ C++ và giao diện console. 
Khi mới khởi động chương trình
![Alt text](Demo/pic1.png)
Chức năng thêm thông tin sinh viên mới
![Alt text](Demo/pic2.png)
Chức năng cập nhật thông tin cho sinh viên
![Alt text](Demo/pic3.png)
Chức năng tìm kiếm sinh viên 
![Alt text](Demo/pic4.png)
Chức năng hiển thị danh sách sinh viên
![Alt text](Demo/pic5.png)
Chức năng xóa sinh viên khỏi danh sách
![Alt text](Demo/pic6.png)
1. Cấu trúc chương trình: 
- Chương trình áp dụng **singleton pattern**, với class **studentManager** có một và chỉ một instance để quản lí các sinh viên và thực hiện các thao tác chính của chương trình.
- Trong file **main.cpp** thực hiện tạo một menu hướng dẫn cho người dùng trong console.
- Trong file **student.h** định nghĩa một struct là student, dùng để đại diện cho các thông tin của một sinh viên.
- Trong file **student.cpp** implement hàm display() dùng để in thông tin của một sinh viên.
- Trong file **student_manger.h** định nghĩa một class studentManger, class này quản lí các thao tác của chương trình và chứa 1 trường dữ liệu static là students, dùng để lưu trữ thông tin của các student trong chương trình.
- Trong file **student_manager.cpp** implement các phương thức (method) của class studentManager trong file student_manager.h, đồng thời implement 1 số hàm phụ.
1. Nếu chưa cài đặt compiler cho C++, vui lòng đọc tài liệu ở đường dẫn sau: https://code.visualstudio.com/docs/languages/cpp 
2. Để compile code, cần mở terminal tại đường dẫn nơi thư mục main.cpp và chạy câu lệnh sau: "g++ *.cpp"
3. Để chạy chương trình, tiếp tục gõ: ".\a"
