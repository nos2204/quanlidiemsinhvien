"""
Main Entry Point — Student Grade Management System
Pattern: Manual Dependency Injection (Composition Root)
"""

import sys, os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
sys.path.insert(0, BASE_DIR)

from repositories.repositories import StudentRepository, GradeRepository, SubjectRepository
from services.services import StudentService, SubjectService, GradeService, ReportService
from views.views import StudentView, SubjectView, GradeView, ReportView

DLINE = "═" * 60


def build_app():
    student_repo = StudentRepository(DATA_DIR)
    grade_repo   = GradeRepository(DATA_DIR)
    subject_repo = SubjectRepository(DATA_DIR)

    student_svc = StudentService(student_repo)
    subject_svc = SubjectService(subject_repo)
    grade_svc   = GradeService(grade_repo, student_repo, subject_repo)
    report_svc  = ReportService(grade_repo, student_repo, subject_repo)

    student_view = StudentView(student_svc, grade_svc)
    subject_view = SubjectView(subject_svc)
    grade_view   = GradeView(grade_svc)
    report_view  = ReportView(report_svc)

    return student_view, subject_view, grade_view, report_view


def seed_demo_data():
    from models.models import Student, Subject, Grade
    import uuid
    sr   = StudentRepository(DATA_DIR)
    gr   = GradeRepository(DATA_DIR)
    subr = SubjectRepository(DATA_DIR)
    if sr.get_all():
        return
    for s in [
        Student("SV2401", "Nguyen Van An",  "2003-05-10", "an@student.edu.vn",   "Computer Science"),
        Student("SV2402", "Tran Thi Bich",  "2003-08-22", "bich@student.edu.vn", "Information Technology"),
        Student("SV2403", "Le Hoang Nam",   "2004-01-15", "nam@student.edu.vn",  "Software Engineering"),
    ]: sr.save(s)
    for s in [
        Subject("CS101", "Introduction to Programming", 3),
        Subject("CS201", "Data Structures & Algorithms", 3),
        Subject("MA101", "Calculus I", 4),
    ]: subr.save(s)
    for sid, subj, score, sem in [
        ("SV2401","CS101",8.5,"2024-1"), ("SV2401","CS201",7.0,"2024-1"), ("SV2401","MA101",6.5,"2024-1"),
        ("SV2402","CS101",9.2,"2024-1"), ("SV2402","MA101",5.5,"2024-1"),
        ("SV2403","CS101",4.5,"2024-1"), ("SV2403","CS201",8.0,"2024-1"),
    ]: gr.save(Grade(str(uuid.uuid4())[:8], sid, subj, score, sem))
    print("\n  [Demo data: 3 sinh viên, 3 môn học, 7 điểm]\n")


def main():
    print(f"{DLINE}\n  Simple Student Grade Management System\n  Kiến Trúc Phần Mềm — 2024\n{DLINE}")
    seed_demo_data()
    student_view, subject_view, grade_view, report_view = build_app()
    while True:
        print(f"\n{DLINE}\n  MAIN MENU\n{DLINE}")
        print("  1. Quản lý Sinh Viên\n  2. Quản lý Môn Học\n  3. Quản lý Điểm\n  4. Báo cáo & Thống kê\n  0. Thoát")
        c = input("  Chọn: ").strip()
        if   c == "1": student_view.menu()
        elif c == "2": subject_view.menu()
        elif c == "3": grade_view.menu()
        elif c == "4": report_view.menu()
        elif c == "0": print("\n  Tạm biệt!\n"); sys.exit(0)
        else: print("\n  ✗  Lựa chọn không hợp lệ.\n")


if __name__ == "__main__":
    main()