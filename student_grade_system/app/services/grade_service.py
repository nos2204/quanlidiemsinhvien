from app.models.student import Student

class GradeService:
    def __init__(self, repository):
        self.repository = repository

    def add_new_student(self, s_id, name, math, lit):
        # Kiểm tra logic: Điểm phải từ 0-10
        if not (0 <= float(math) <= 10 and 0 <= float(lit) <= 10):
            raise ValueError("Điểm số không hợp lệ (phải từ 0-10)")
        
        # Kiểm tra trùng ID
        if self.repository.find_by_id(s_id):
            raise ValueError("Mã sinh viên đã tồn tại!")

        new_student = Student(s_id, name, math, lit)
        return self.repository.add(new_student)

    def get_class_report(self):
        students = self.repository.get_all()
        if not students:
            return {"students": [], "class_average": 0}
        
        total_avg = sum(s.average_score for s in students)
        return {
            "students": [s.to_dict() for s in students],
            "class_average": round(total_avg / len(students), 2)
        }