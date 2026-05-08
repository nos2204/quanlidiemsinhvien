"""
Services — Student Grade Management System
Layer: Business Logic Layer
"""

import uuid, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.models import Student, Grade, Subject
from repositories.repositories import StudentRepository, GradeRepository, SubjectRepository
from services.validators import StudentValidator, GradeValidator, SubjectValidator, ValidationError


class StudentService:
    def __init__(self, student_repo: StudentRepository):
        self._repo = student_repo

    def add_student(self, student_id, full_name, date_of_birth, email, major) -> Student:
        StudentValidator.validate_student_id(student_id)
        StudentValidator.validate_name(full_name)
        StudentValidator.validate_date(date_of_birth)
        StudentValidator.validate_email(email)
        if self._repo.exists(student_id):
            raise ValidationError(f"Mã sinh viên '{student_id}' đã tồn tại.")
        student = Student(student_id, full_name, date_of_birth, email, major)
        self._repo.save(student)
        return student

    def update_student(self, student_id, full_name=None, email=None, major=None) -> Student:
        student = self._repo.find_by_id(student_id)
        if not student:
            raise ValidationError(f"Không tìm thấy sinh viên '{student_id}'.")
        if full_name:
            StudentValidator.validate_name(full_name)
            student.full_name = full_name
        if email:
            StudentValidator.validate_email(email)
            student.email = email
        if major:
            student.major = major
        self._repo.save(student)
        return student

    def delete_student(self, student_id, grade_repo: GradeRepository) -> bool:
        if not self._repo.exists(student_id):
            raise ValidationError(f"Không tìm thấy sinh viên '{student_id}'.")
        grade_repo.delete_by_student(student_id)
        return self._repo.delete(student_id)

    def get_all_students(self) -> list[Student]:
        return self._repo.get_all()

    def get_student(self, student_id) -> Student:
        s = self._repo.find_by_id(student_id)
        if not s:
            raise ValidationError(f"Không tìm thấy sinh viên '{student_id}'.")
        return s

    def search_students(self, keyword) -> list[Student]:
        return self._repo.find_by_name(keyword)


class SubjectService:
    def __init__(self, subject_repo: SubjectRepository):
        self._repo = subject_repo

    def add_subject(self, subject_id, subject_name, credits) -> Subject:
        SubjectValidator.validate_subject_id(subject_id)
        if self._repo.exists(subject_id):
            raise ValidationError(f"Mã môn '{subject_id}' đã tồn tại.")
        subject = Subject(subject_id, subject_name, credits)
        self._repo.save(subject)
        return subject

    def get_all_subjects(self) -> list[Subject]:
        return self._repo.get_all()

    def get_subject(self, subject_id) -> Subject:
        s = self._repo.find_by_id(subject_id)
        if not s:
            raise ValidationError(f"Không tìm thấy môn '{subject_id}'.")
        return s


class GradeService:
    def __init__(self, grade_repo, student_repo, subject_repo):
        self._grade_repo = grade_repo
        self._student_repo = student_repo
        self._subject_repo = subject_repo

    def assign_grade(self, student_id, subject_id, score, semester) -> Grade:
        GradeValidator.validate_score(str(score))
        GradeValidator.validate_semester(semester)
        if not self._student_repo.exists(student_id):
            raise ValidationError(f"Không tìm thấy sinh viên '{student_id}'.")
        if not self._subject_repo.exists(subject_id):
            raise ValidationError(f"Không tìm thấy môn '{subject_id}'.")
        existing = self._grade_repo.find_by_student_and_subject(student_id, subject_id)
        if existing:
            existing.score = score
            existing.semester = semester
            self._grade_repo.save(existing)
            return existing
        grade = Grade(str(uuid.uuid4())[:8], student_id, subject_id, score, semester)
        self._grade_repo.save(grade)
        return grade

    def get_grades_by_student(self, student_id) -> list[Grade]:
        return self._grade_repo.find_by_student(student_id)

    def get_grades_by_subject(self, subject_id) -> list[Grade]:
        return self._grade_repo.find_by_subject(subject_id)


class ReportService:
    def __init__(self, grade_repo, student_repo, subject_repo):
        self._grade_repo = grade_repo
        self._student_repo = student_repo
        self._subject_repo = subject_repo

    def student_transcript(self, student_id) -> dict:
        student = self._student_repo.find_by_id(student_id)
        if not student:
            raise ValidationError(f"Không tìm thấy sinh viên '{student_id}'.")
        grades = self._grade_repo.find_by_student(student_id)
        rows = []
        for g in grades:
            subject = self._subject_repo.find_by_id(g.subject_id)
            rows.append({
                "subject": subject.subject_name if subject else g.subject_id,
                "credits": subject.credits if subject else "?",
                "score": g.score, "letter": g.letter_grade,
                "passed": g.passed, "semester": g.semester,
            })
        gpa = round(sum(g.score for g in grades) / len(grades), 2) if grades else 0.0
        return {
            "student": student, "grades": rows, "gpa": gpa,
            "passed_count": sum(1 for r in rows if r["passed"]),
            "failed_count": sum(1 for r in rows if not r["passed"]),
        }

    def class_summary(self, subject_id) -> dict:
        subject = self._subject_repo.find_by_id(subject_id)
        if not subject:
            raise ValidationError(f"Không tìm thấy môn '{subject_id}'.")
        grades = self._grade_repo.find_by_subject(subject_id)
        rows = []
        for g in grades:
            student = self._student_repo.find_by_id(g.student_id)
            rows.append({
                "student": student.full_name if student else g.student_id,
                "score": g.score, "letter": g.letter_grade, "passed": g.passed,
            })
        scores = [r["score"] for r in rows]
        return {
            "subject": subject, "rows": rows, "count": len(rows),
            "average": round(sum(scores) / len(scores), 2) if scores else 0.0,
            "highest": max(scores) if scores else 0.0,
            "lowest": min(scores) if scores else 0.0,
            "pass_rate": round(sum(1 for r in rows if r["passed"]) / len(rows) * 100, 1) if rows else 0.0,
        }

    def top_students(self, n=5) -> list[dict]:
        students = self._student_repo.get_all()
        results = []
        for student in students:
            grades = self._grade_repo.find_by_student(student.student_id)
            if grades:
                gpa = round(sum(g.score for g in grades) / len(grades), 2)
                results.append({"student": student, "gpa": gpa, "count": len(grades)})
        results.sort(key=lambda x: x["gpa"], reverse=True)
        return results[:n]