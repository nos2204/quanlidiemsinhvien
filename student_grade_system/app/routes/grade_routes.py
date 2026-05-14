from flask import Blueprint, request, jsonify
from app.services.grade_service import GradeService
from app.repositories.student_repo import StudentRepository

# Khởi tạo Dependency (Lab 3)
repo = StudentRepository()
service = GradeService(repo)
grade_bp = Blueprint('grade', __name__)

@grade_bp.route('/students', methods=['GET'])
def get_all():
    return jsonify(service.get_all_students())

@grade_bp.route('/students', methods=['POST'])
def add():
    data = request.json
    res = service.add_student(data['id'], data['name'], data['math'], data['lit'])
    return jsonify(res), 201