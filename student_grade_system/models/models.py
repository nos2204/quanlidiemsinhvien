"""
Domain Models — Student Grade Management System
Layer: Data Access Layer (Model definitions)
"""

from dataclasses import dataclass


@dataclass
class Student:
    student_id: str
    full_name: str
    date_of_birth: str
    email: str
    major: str

    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "full_name": self.full_name,
            "date_of_birth": self.date_of_birth,
            "email": self.email,
            "major": self.major,
        }

    @staticmethod
    def from_dict(data: dict) -> "Student":
        return Student(
            student_id=data["student_id"],
            full_name=data["full_name"],
            date_of_birth=data["date_of_birth"],
            email=data["email"],
            major=data["major"],
        )

    def __str__(self) -> str:
        return f"[{self.student_id}] {self.full_name} — {self.major}"


@dataclass
class Subject:
    subject_id: str
    subject_name: str
    credits: int

    def to_dict(self) -> dict:
        return {
            "subject_id": self.subject_id,
            "subject_name": self.subject_name,
            "credits": self.credits,
        }

    @staticmethod
    def from_dict(data: dict) -> "Subject":
        return Subject(
            subject_id=data["subject_id"],
            subject_name=data["subject_name"],
            credits=data["credits"],
        )

    def __str__(self) -> str:
        return f"[{self.subject_id}] {self.subject_name} ({self.credits} credits)"


@dataclass
class Grade:
    grade_id: str
    student_id: str
    subject_id: str
    score: float
    semester: str

    def to_dict(self) -> dict:
        return {
            "grade_id": self.grade_id,
            "student_id": self.student_id,
            "subject_id": self.subject_id,
            "score": self.score,
            "semester": self.semester,
        }

    @staticmethod
    def from_dict(data: dict) -> "Grade":
        return Grade(
            grade_id=data["grade_id"],
            student_id=data["student_id"],
            subject_id=data["subject_id"],
            score=float(data["score"]),
            semester=data["semester"],
        )

    @property
    def letter_grade(self) -> str:
        if self.score >= 9.0:   return "A+"
        elif self.score >= 8.0: return "A"
        elif self.score >= 7.0: return "B"
        elif self.score >= 6.0: return "C"
        elif self.score >= 5.0: return "D"
        else:                   return "F"

    @property
    def passed(self) -> bool:
        return self.score >= 5.0