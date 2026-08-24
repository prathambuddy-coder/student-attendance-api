from flask import Blueprint,Flask,request,jsonify
from db import db

subject_bp=Blueprint("subject",__name__)

@subject_bp.route("/subjects",methods=["POST"])
def add_subjects():
    data=request.get_json()

    if not data:
        return jsonify({
            "error":"Request body is required"
        }),400

    if "name" not in data:
        return jsonify({
            "error":"Missing required field:subject"
        })

    if "code" not in data:
        return jsonify({
            "error":"Missing required field:code"
        })

    name=data["name"]
    code=data["code"]

    cursor=db.cursor(dictionary=True)
    cursor.execute("INSERT INTO subjects (name,code) VALUES (%s,%s)",(name,code))

    subject_id=cursor.lastrowid
    db.commit()
    cursor.close()

    
    return jsonify({
        "students":{
                "id":subject_id,
                "subject":data["name"],
                "code":data["code"]
            }
    }),201

@subject_bp.route("/subjects",methods=["GET"])
def get_subjects():
    cursor=db.cursor(dictionary=True)
    cursor.execute("SELECT * from subjects")

    subjects=cursor.fetchall()

    cursor.close()
    return jsonify(subjects), 200

@subject_bp.route("/subjects/<int:id>",methods=["GET"])
def get_subject_id(id):
    cursor=db.cursor(dictionary=True)
    cursor.execute("SELECT * from subjects where id=%s",(id,))

    subject=cursor.fetchone()
    cursor.close()
    if not subject:
        return jsonify({
        "error": "Subject not found"
    }), 404

    return jsonify(subject)

@subject_bp.route("/subjects/<int:id>",methods=["PUT"])
def update_subject(id):
    data=request.get_json()

    if not data:
        return jsonify({
            "error":"Request body is required"
        }),400

    if "name" not in data:
        return jsonify({
            "error":"Missing required field:name"
        }),400

    if "code" not in data:
        return jsonify({
            "error":"Missing required field:code"
        }),400

    if "email" not in data:
        return jsonify({
            "error":"Missing required field:email"
        }),400


    name=data["name"]
    code=data["code"]
    cursor=db.cursor(dictionary=True)
    cursor.execute("UPDATE subjects SET name=%s, code=%s WHERE id=%s",(name,code,id))

    if cursor.rowcount==0:
        cursor.close()
        return jsonify({
            "error":"Subject not found"
        }),404
    
    db.commit()
    cursor.close()

    return jsonify({
        "message":"Subject successfully updated",
        "subject":{
            "name":data["name"],
            "code":data["code"]
        }
    }),200

@subject_bp.route("/subjects/<int:id>",methods=["DELETE"])
def remove_subjects(id):    
    cursor=db.cursor(dictionary=True)
    cursor.execute("DELETE FROM subjects WHERE id=%s",(id,))

    if(cursor.rowcount==0):
        cursor.close()
        db.commit()
        return jsonify({
            "error":"Subject not found"
        }),404
    
    db.commit()
    cursor.close()
    return jsonify({
        "message":"Subject deleted successfully"
    }),200