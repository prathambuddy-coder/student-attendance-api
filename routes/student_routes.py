from flask import Blueprint,jsonify,request
from db import db

student_bp=Blueprint("student",__name__)

@student_bp.route("/students",methods=["POST"])
def add_student():
    data=request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }),400
    if "name" not in data:
        return jsonify({
            "error":"Missing required field:name"
        }),400
    if "age" not in data:
        return jsonify({
            "error":"Missing required field:age"
        }),400
    if "branch" not in data:
        return jsonify({
            "error":"Missing required field:branch"
        }),400
    if "email" not in data:
        return jsonify({
            "error":"Missing required field:email"
        }),400

    name=data["name"]
    age=data["age"]
    branch=data["branch"]
    email=data["email"]
    cursor=db.cursor(dictionary=True)

    cursor.execute("INSERT INTO students (name,age,branch,email) VALUES (%s,%s,%s,%s)",(name,age,branch,email))

    db.commit()

    student_id=cursor.lastrowid
    cursor.close()
    return jsonify({
        "student":{
            "id":student_id,
            "name":name,
            "age":age,
            "branch":branch,
            "email":email
        }
    }),201

@student_bp.route("/students",methods=["GET"])
def get_students():
    cursor=db.cursor(dictionary=True)
    cursor.execute("SELECT * from students")

    students=cursor.fetchall()
    cursor.close()
    return jsonify(students), 200

@student_bp.route("/students/<int:id>",methods=["GET"])
def get_students_id(id):
    cursor=db.cursor(dictionary=True)
    cursor.execute("SELECT * from students where id=%s",(id,))

    student=cursor.fetchone()
    cursor.close()
    if not student:
        return jsonify({
        "error": "Student not found"
    }), 404

    return jsonify(student),200

@student_bp.route("/students/<int:id>",methods=["PUT"])
def update_students(id):
    data=request.get_json()

    if not data:
        return jsonify({
            "error":"Request body is required"
        }),400

    if "name" not in data:
        return jsonify({
            "error":"Missing required field:name"
        }),400

    if "age" not in data:
        return jsonify({
            "error":"Missing required field:age"
        }),400

    if "branch" not in data:
        return jsonify({
            "error":"Missing required field:branch"
        }),400

    if "email" not in data:
        return jsonify({
            "error":"Missing required field:email"
        }),400


    name=data["name"]
    age=data["age"]
    branch=data["branch"]
    email=data["email"]
    cursor=db.cursor(dictionary=True)
    cursor.execute("UPDATE students SET name=%s, age=%s, branch=%s, email=%s WHERE id=%s",(name,age,branch,email,id))

    if cursor.rowcount==0:
        cursor.close()
        return jsonify({
            "error":"Student not found"
        }),404
    
    db.commit()
    cursor.close()

    return jsonify({
        "message":"Student successfully updated",
        "student":{
            "id":id,
            "name":data["name"],
            "age":data["age"],
            "branch":data["branch"],
            "email":data["email"]
        }
    }),200

@student_bp.route("/students/<int:id>",methods=["DELETE"])
def remove_students(id):    
    cursor=db.cursor(dictionary=True)
    cursor.execute("DELETE FROM students WHERE id=%s",(id,))

    if(cursor.rowcount==0):
        cursor.close()
        db.commit()
        return jsonify({
            "error":"Student not found"
        }),404
    
    db.commit()
    cursor.close()
    return jsonify({
        "message":"Student deleted successfully"
    }),200
