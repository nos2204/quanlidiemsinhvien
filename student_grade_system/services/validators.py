"""
Validators — Student Grade Management System
Layer: Business Logic Layer
"""

import re


class ValidationError(Exception):
    pass


class StudentValidator:
    @staticmethod
    def validate_student_id(sid: str) -> None:
        if not re.match(r"^SV\d{4,8}$", sid):
            raise ValidationError("Student ID phải bắt đầu bằng 'SV' + 4–8 số (vd: SV2401).")

    @staticmethod
    def validate_email(email: str) -> None:
        if not re.match(r"^[\w.+-]+@[\w-]+\.\w+$", email):
            raise ValidationError(f"Email không hợp lệ: {email}")

    @staticmethod
    def validate_date(date_str: str) -> None:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
            raise ValidationError("Ngày sinh phải theo định dạng YYYY-MM-DD.")

    @staticmethod
    def validate_name(name: str) -> None:
        if len(name.strip()) < 2:
            raise ValidationError("Tên phải có ít nhất 2 ký tự.")


class GradeValidator:
    @staticmethod
    def validate_score(score_str: str) -> float:
        try:
            score = float(score_str)
        except ValueError:
            raise ValidationError("Điểm phải là số.")
        if not (0.0 <= score <= 10.0):
            raise ValidationError("Điểm phải từ 0.0 đến 10.0.")
        return score

    @staticmethod
    def validate_semester(semester: str) -> None:
        if not re.match(r"^\d{4}-[12]$", semester):
            raise ValidationError("Học kỳ theo định dạng YYYY-S (vd: 2024-1 hoặc 2024-2).")


class SubjectValidator:
    @staticmethod
    def validate_credits(credits_str: str) -> int:
        try:
            credits = int(credits_str)
        except ValueError:
            raise ValidationError("Số tín chỉ phải là số nguyên.")
        if credits < 1 or credits > 10:
            raise ValidationError("Số tín chỉ phải từ 1 đến 10.")
        return credits

    @staticmethod
    def validate_subject_id(sid: str) -> None:
        if not re.match(r"^[A-Z]{2,5}\d{3}$", sid):
            raise ValidationError("Mã môn: 2–5 chữ HOA + 3 số (vd: CS101).")