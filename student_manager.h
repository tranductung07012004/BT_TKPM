#ifndef _student_manager_
#define _student_manager_

#include <iostream>
#include <vector>
#include "student.h"

class studentManager {
  private: 
    std::vector<student> students;

    studentManager() {}

  public: 
    studentManager(const studentManager&) = delete;
    studentManager& operator = (const studentManager&) = delete;
    static studentManager& getInstance();
    static student inputStudent();
    void addStudent(const student& s);
    void removeStudent(const string& id);
    void updateStudent(const std::string& id, const student& newInfo);
    void findStudent(const std::string& keyword);
    void displayAll();
};

#endif