"""
Concrete Repositories — Student Grade Management System
Layer: Data Access Layer
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.models import Student, Grade, Subject
from repositories.base_repository import JSONRepository


class StudentRepository(JSONRepository):
    _filepath = "students.json"

    @property
    def _id_field(self) -> str:
        return "student_id"

    def _deserialize(self, data: dict) -> Student:
        return Student.from_dict(data)

    def find_by_name(self, keyword: str) -> list[Student]:
        keyword = keyword.lower()
        return [
            self._deserialize(item) for item in self._cache
            if keyword in item["full_name"].lower()
        ]

    def exists(self, student_id: str) -> bool:
        return self.find_by_id(student_id) is not None


class GradeRepository(JSONRepository):
    _filepath = "grades.json"

    @property
    def _id_field(self) -> str:
        return "grade_id"

    def _deserialize(self, data: dict) -> Grade:
        return Grade.from_dict(data)

    def find_by_student(self, student_id: str) -> list[Grade]:
        return [
            self._deserialize(item) for item in self._cache
            if item["student_id"] == student_id
        ]

    def find_by_subject(self, subject_id: str) -> list[Grade]:
        return [
            self._deserialize(item) for item in self._cache
            if item["subject_id"] == subject_id
        ]

    def find_by_student_and_subject(self, student_id: str, subject_id: str) -> Grade | None:
        for item in self._cache:
            if item["student_id"] == student_id and item["subject_id"] == subject_id:
                return self._deserialize(item)
        return None

    def delete_by_student(self, student_id: str) -> int:
        before = len(self._cache)
        self._cache = [i for i in self._cache if i["student_id"] != student_id]
        removed = before - len(self._cache)
        if removed:
            self._save()
        return removed


class SubjectRepository(JSONRepository):
    _filepath = "subjects.json"

    @property
    def _id_field(self) -> str:
        return "subject_id"

    def _deserialize(self, data: dict) -> Subject:
        return Subject.from_dict(data)

    def exists(self, subject_id: str) -> bool:
        return self.find_by_id(subject_id) is not None