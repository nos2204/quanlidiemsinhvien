class Student:
    def __init__(self, student_id, name, math_score, literature_score):
        self.student_id = student_id
        self.name = name
        self.math_score = float(math_score)
        self.literature_score = float(literature_score)
        # Tự động tính điểm trung bình khi khởi tạo
        self.average_score = (self.math_score + self.literature_score) / 2

    def to_dict(self):
        """Chuyển đổi object sang dictionary để trả về JSON API"""
        return {
            "id": self.student_id,
            "name": self.name,
            "math": self.math_score,
            "literature": self.literature_score,
            "average": round(self.average_score, 2),
            "rank": self.get_rank()
        }

    def get_rank(self):
        if self.average_score >= 8.0: return "Giỏi"
        if self.average_score >= 6.5: return "Khá"
        if self.average_score >= 5.0: return "Trung bình"
        return "Yếu"