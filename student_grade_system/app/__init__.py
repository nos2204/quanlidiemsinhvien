from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Thêm dòng này để fix lỗi RuntimeError: The session is unavailable
    app.config['SECRET_KEY'] = 'kien-truc-phan-mem-bi-mat'
    
    from app.routes.grade_routes import grade_bp
    app.register_blueprint(grade_bp, url_prefix='/api')
    
    return app