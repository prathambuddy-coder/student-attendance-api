from flask import Flask,jsonify
from routes.student_routes import student_bp
from routes.subject_routes import subject_bp
from routes.attendance_routes import attendance_bp
from auth.auth_routes import auth_bp

app=Flask(__name__)

app.register_blueprint(student_bp)
app.register_blueprint(subject_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return jsonify({
        "message":"Student api is running"
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error":"Resource not found"
    }),404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error":"Internal Error server Error"
    }),500

if __name__=="__main__":
    app.run(debug=True)