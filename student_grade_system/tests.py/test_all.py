"""
Unit Tests — Student Grade Management System
"""
import sys, os, unittest, tempfile, shutil
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.validators import StudentValidator, GradeValidator, ValidationError
from models.models import Student, Subject, Grade
from repositories.repositories import StudentRepository, GradeRepository, SubjectRepository
from services.services import StudentService, GradeService, ReportService


class TestStudentValidator(unittest.TestCase):
    def test_valid_id(self):       StudentValidator.validate_student_id("SV2401")
    def test_invalid_id(self):
        with self.assertRaises(ValidationError): StudentValidator.validate_student_id("2401")
    def test_valid_email(self):    StudentValidator.validate_email("test@example.com")
    def test_invalid_email(self):
        with self.assertRaises(ValidationError): StudentValidator.validate_email("bad-email")
    def test_valid_date(self):     StudentValidator.validate_date("2003-05-10")
    def test_invalid_date(self):
        with self.assertRaises(ValidationError): StudentValidator.validate_date("10-05-2003")


class TestGradeValidator(unittest.TestCase):
    def test_valid_score(self):    self.assertEqual(GradeValidator.validate_score("8.5"), 8.5)
    def test_out_of_range(self):
        with self.assertRaises(ValidationError): GradeValidator.validate_score("11.0")
    def test_not_number(self):
        with self.assertRaises(ValidationError): GradeValidator.validate_score("abc")


class TestStudentService(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.svc = StudentService(StudentRepository(self.tmp))
    def tearDown(self): shutil.rmtree(self.tmp)

    def test_add(self):
        s = self.svc.add_student("SV0001","Test","2000-01-01","t@t.com","CS")
        self.assertEqual(s.full_name, "Test")
    def test_duplicate(self):
        self.svc.add_student("SV0001","Test","2000-01-01","t@t.com","CS")
        with self.assertRaises(ValidationError):
            self.svc.add_student("SV0001","Other","2000-01-01","o@t.com","IT")
    def test_not_found(self):
        with self.assertRaises(ValidationError): self.svc.get_student("SV9999")


class TestGradeService(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        sr = StudentRepository(self.tmp)
        gr = GradeRepository(self.tmp)
        subr = SubjectRepository(self.tmp)
        sr.save(Student("SV0001","Test","2000-01-01","t@t.com","CS"))
        subr.save(Subject("CS101","Programming",3))
        self.svc = GradeService(gr, sr, subr)
    def tearDown(self): shutil.rmtree(self.tmp)

    def test_assign(self):
        g = self.svc.assign_grade("SV0001","CS101",8.0,"2024-1")
        self.assertEqual(g.letter_grade, "A")
    def test_letter_grades(self):
        cases = [(9.5,"A+"),(8.5,"A"),(7.5,"B"),(6.5,"C"),(5.5,"D"),(4.0,"F")]
        for score, expected in cases:
            self.assertEqual(Grade("x","SV0001","CS101",score,"2024-1").letter_grade, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)