"""
Views — Student Grade Management System
Layer: Presentation Layer (CLI)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from services.validators import ValidationError

LINE  = "─" * 60
DLINE = "═" * 60

def _input(prompt): return input(f"  {prompt}").strip()
def _ok(msg):    print(f"\n  ✓  {msg}\n")
def _err(msg):   print(f"\n  ✗  {msg}\n")
def _header(t):
    print(f"\n{DLINE}\n  {t}\n{DLINE}")


class StudentView:
    def __init__(self, student_service, grade_service):
        self._ss = student_service
        self._gs = grade_service

    def menu(self):
        while True:
            _header("STUDENT MANAGEMENT")
            print("  1. Thêm sinh viên\n  2. Danh sách\n  3. Tìm kiếm\n  4. Chi tiết\n  5. Cập nhật\n  6. Xóa\n  0. Quay lại")
            c = _input("Chọn: ")
            if c == "1": self._add()
            elif c == "2": self._list_all()
            elif c == "3": self._search()
            elif c == "4": self._detail()
            elif c == "5": self._update()
            elif c == "6": self._delete()
            elif c == "0": break
            else: _err("Lựa chọn không hợp lệ.")

    def _add(self):
        _header("Thêm Sinh Viên")
        try:
            sid  = _input("Mã SV (vd SV2401): ")
            name = _input("Họ tên: ")
            dob  = _input("Ngày sinh (YYYY-MM-DD): ")
            email= _input("Email: ")
            major= _input("Ngành học: ")
            s = self._ss.add_student(sid, name, dob, email, major)
            _ok(f"Đã thêm sinh viên '{s.full_name}'.")
        except ValidationError as e: _err(str(e))

    def _list_all(self):
        _header("Danh Sách Sinh Viên")
        students = self._ss.get_all_students()
        if not students: print("  (Chưa có sinh viên)\n"); return
        print(f"  {'Mã SV':<10} {'Họ tên':<25} {'Ngành':<20} {'Email'}")
        print(f"  {LINE}")
        for s in students:
            print(f"  {s.student_id:<10} {s.full_name:<25} {s.major:<20} {s.email}")
        print()

    def _search(self):
        kw = _input("Tìm theo tên: ")
        results = self._ss.search_students(kw)
        _header(f"Kết quả tìm '{kw}'")
        if not results: print("  Không tìm thấy.\n"); return
        for s in results: print(f"  {s}")
        print()

    def _detail(self):
        sid = _input("Mã SV: ")
        try:
            s = self._ss.get_student(sid)
            _header(f"Chi tiết — {s.student_id}")
            print(f"  Họ tên   : {s.full_name}\n  Ngày sinh: {s.date_of_birth}\n  Email    : {s.email}\n  Ngành    : {s.major}")
            grades = self._gs.get_grades_by_student(sid)
            print(f"  Số môn   : {len(grades)}\n")
        except ValidationError as e: _err(str(e))

    def _update(self):
        sid = _input("Mã SV cần cập nhật: ")
        _header("Cập nhật (bỏ trống = giữ nguyên)")
        try:
            name  = _input("Họ tên mới: ") or None
            email = _input("Email mới: ")  or None
            major = _input("Ngành mới: ")  or None
            s = self._ss.update_student(sid, name, email, major)
            _ok(f"Đã cập nhật '{s.full_name}'.")
        except ValidationError as e: _err(str(e))

    def _delete(self):
        sid = _input("Mã SV cần xóa: ")
        cfm = _input(f"Xóa '{sid}' và toàn bộ điểm? (yes/no): ")
        if cfm.lower() != "yes": print("  Đã hủy.\n"); return
        try:
            self._ss.delete_student(sid, self._gs._grade_repo)
            _ok(f"Đã xóa sinh viên '{sid}'.")
        except ValidationError as e: _err(str(e))


class SubjectView:
    def __init__(self, subject_service):
        self._ss = subject_service

    def menu(self):
        while True:
            _header("SUBJECT MANAGEMENT")
            print("  1. Thêm môn học\n  2. Danh sách môn học\n  0. Quay lại")
            c = _input("Chọn: ")
            if c == "1": self._add()
            elif c == "2": self._list_all()
            elif c == "0": break
            else: _err("Lựa chọn không hợp lệ.")

    def _add(self):
        _header("Thêm Môn Học")
        try:
            sid     = _input("Mã môn (vd CS101): ")
            name    = _input("Tên môn học: ")
            credits_str = _input("Số tín chỉ (1–10): ")
            from services.validators import SubjectValidator
            credits = SubjectValidator.validate_credits(credits_str)
            s = self._ss.add_subject(sid, name, credits)
            _ok(f"Đã thêm môn '{s.subject_name}'.")
        except ValidationError as e: _err(str(e))

    def _list_all(self):
        _header("Danh Sách Môn Học")
        subjects = self._ss.get_all_subjects()
        if not subjects: print("  (Chưa có môn học)\n"); return
        print(f"  {'Mã môn':<10} {'Tên môn':<30} {'Tín chỉ'}")
        print(f"  {LINE}")
        for s in subjects:
            print(f"  {s.subject_id:<10} {s.subject_name:<30} {s.credits}")
        print()


class GradeView:
    def __init__(self, grade_service):
        self._gs = grade_service

    def menu(self):
        while True:
            _header("GRADE MANAGEMENT")
            print("  1. Nhập/cập nhật điểm\n  2. Xem điểm theo sinh viên\n  3. Xem điểm theo môn\n  0. Quay lại")
            c = _input("Chọn: ")
            if c == "1": self._assign()
            elif c == "2": self._by_student()
            elif c == "3": self._by_subject()
            elif c == "0": break
            else: _err("Lựa chọn không hợp lệ.")

    def _assign(self):
        _header("Nhập Điểm")
        try:
            sid  = _input("Mã SV: ")
            subj = _input("Mã môn: ")
            sc   = _input("Điểm (0.0–10.0): ")
            sem  = _input("Học kỳ (vd 2024-1): ")
            from services.validators import GradeValidator
            score = GradeValidator.validate_score(sc)
            g = self._gs.assign_grade(sid, subj, score, sem)
            _ok(f"Đã nhập điểm {g.score} ({g.letter_grade}).")
        except ValidationError as e: _err(str(e))

    def _by_student(self):
        sid = _input("Mã SV: ")
        grades = self._gs.get_grades_by_student(sid)
        _header(f"Điểm của {sid}")
        if not grades: print("  Chưa có điểm.\n"); return
        print(f"  {'Môn':<12} {'Điểm':<8} {'Xếp loại':<10} {'Học kỳ':<10} {'KQ'}")
        print(f"  {LINE}")
        for g in grades:
            print(f"  {g.subject_id:<12} {g.score:<8.1f} {g.letter_grade:<10} {g.semester:<10} {'ĐẬU' if g.passed else 'RỚT'}")
        print()

    def _by_subject(self):
        subj = _input("Mã môn: ")
        grades = self._gs.get_grades_by_subject(subj)
        _header(f"Điểm môn {subj}")
        if not grades: print("  Chưa có điểm.\n"); return
        print(f"  {'Mã SV':<12} {'Điểm':<8} {'Xếp loại':<10} {'KQ'}")
        print(f"  {LINE}")
        for g in grades:
            print(f"  {g.student_id:<12} {g.score:<8.1f} {g.letter_grade:<10} {'ĐẬU' if g.passed else 'RỚT'}")
        print()


class ReportView:
    def __init__(self, report_service):
        self._rs = report_service

    def menu(self):
        while True:
            _header("REPORTS")
            print("  1. Bảng điểm sinh viên\n  2. Thống kê lớp theo môn\n  3. Xếp hạng sinh viên\n  0. Quay lại")
            c = _input("Chọn: ")
            if c == "1": self._transcript()
            elif c == "2": self._class_summary()
            elif c == "3": self._top()
            elif c == "0": break
            else: _err("Lựa chọn không hợp lệ.")

    def _transcript(self):
        sid = _input("Mã SV: ")
        try:
            r = self._rs.student_transcript(sid)
            s = r["student"]
            _header(f"Bảng điểm — {s.full_name} ({s.student_id})")
            print(f"  Ngành: {s.major}\n")
            print(f"  {'Môn học':<30} {'TC':<6} {'Điểm':<8} {'Loại':<8} {'Học kỳ'}")
            print(f"  {LINE}")
            for row in r["grades"]:
                print(f"  {row['subject']:<30} {str(row['credits']):<6} {row['score']:<8.1f} {row['letter']:<8} {row['semester']}")
            print(f"\n  GPA  : {r['gpa']:.2f}/10.0")
            print(f"  Đậu  : {r['passed_count']}  |  Rớt: {r['failed_count']}\n")
        except ValidationError as e: _err(str(e))

    def _class_summary(self):
        subj = _input("Mã môn: ")
        try:
            r = self._rs.class_summary(subj)
            sub = r["subject"]
            _header(f"Thống kê — {sub.subject_name}")
            print(f"  {'Sinh viên':<25} {'Điểm':<8} {'Loại':<8} {'KQ'}")
            print(f"  {LINE}")
            for row in r["rows"]:
                print(f"  {row['student']:<25} {row['score']:<8.1f} {row['letter']:<8} {'ĐẬU' if row['passed'] else 'RỚT'}")
            print(f"\n  Số SV   : {r['count']}  |  TB: {r['average']:.2f}  |  Cao: {r['highest']:.1f}  |  Thấp: {r['lowest']:.1f}")
            print(f"  Tỷ lệ đậu: {r['pass_rate']}%\n")
        except ValidationError as e: _err(str(e))

    def _top(self):
        n = int(_input("Top N sinh viên (mặc định 5): ") or "5")
        results = self._rs.top_students(n)
        _header(f"Top {n} Sinh Viên theo GPA")
        if not results: print("  Chưa có dữ liệu.\n"); return
        print(f"  {'Hạng':<6} {'Họ tên':<25} {'GPA':<8} {'Số môn'}")
        print(f"  {LINE}")
        for i, r in enumerate(results, 1):
            print(f"  {i:<6} {r['student'].full_name:<25} {r['gpa']:<8.2f} {r['count']}")
        print()