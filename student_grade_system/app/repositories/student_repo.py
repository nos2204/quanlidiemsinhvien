class StudentRepository:
    def __init__(self):
        # Sử dụng dictionary để mô phỏng Database trong bộ nhớ
        self._students = {}

    def add(self, student):
        self._students[student.student_id] = student
        return student

    def get_all(self):
        return list(self._students.values())

    def find_by_id(self, student_id):
        return self._students.get(student_id)

    def delete(self, student_id):
        if student_id in self._students:
            del self._students[student_id]
            return True
        return False