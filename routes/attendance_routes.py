from flask import Flask,Blueprint,jsonify,request
from db import db

attendance_bp=Blueprint("attendance",__name__)

@attendance_bp.route("/attendance",methods=["POST"])
def mark_attendance():
    data=request.get_json()

    if not data:
        return jsonify({
            "error":"Request body is required"
        }),400

    if "student_id" not in data:
        return jsonify({
            "error":"Missing required field:student_id"
        }),400
    
    if "subject_id" not in data:
        return jsonify({
            "error":"Missing required field:subject_id"
        }),400
    
    if "date" not in data:
        return jsonify({
            "error":"Missing required field:date"
        }),400
    
    if "status" not in data:
        return jsonify({
            "error":"Missing required field:status"
        }),400

    attendance=["Present","Absent"] 

    student_id=data["student_id"]
    subject_id=data["subject_id"]
    date=data["date"]
    status=data["status"]

    if status not in attendance:
        return jsonify({
            "error":"Invalid input"
        })

    cursor=db.cursor(dictionary=True)


    cursor.execute(
        "SELECT id FROM students WHERE id=%s",
        (student_id,)
    )

    student=cursor.fetchone()

    if not student:
        return jsonify({
            "error":"Student not found"
        }),404

    cursor.execute(
        "SELECT id FROM subjects WHERE id=%s",
        (subject_id,)
    )   

    subject = cursor.fetchone()

    if not subject:
        cursor.close()
        return jsonify({
            "error": "Subject not found"
        }), 404

    
    cursor.execute("INSERT INTO attendance (student_id, subject_id, date, status) VALUES (%s, %s, %s, %s)",(student_id,subject_id,date,status))

    db.commit()
    attendance_id=cursor.lastrowid
    cursor.close()

    return jsonify({
        "message":"Attendance marked successfully",
        "attendance":{
            "id":attendance_id,
            "student_id":student_id,
            "subject_id":subject_id,
            "date":date,
            "status":status
        }
    }),201

@attendance_bp.route("/attendance",methods=["GET"])
def get_attendance():
    student_id=request.args.get("student_id",type=int)
    subject_id=request.args.get("subject_id",type=int)
    date=request.args.get("date")

    query="""
        SELECT attendance.id,students.name as student_name,subjects.name as subject_name,attendance.status,attendance.date from attendance
        JOIN students
        ON attendance.student_id=students.id
        JOIN subjects
        ON attendance.subject_id=subjects.id
    """

    conditions=[]
    values=[]

    if student_id:
        conditions.append("student_id=%s")
        values.append(student_id)

    if subject_id:
        conditions.append("subject_id=%s")
        values.append(subject_id)

    if date:
        conditions.append("date=%s")
        values.append(date)

    if conditions:
        query+=" WHERE "+ " AND ".join(conditions)

    cursor=db.cursor(dictionary=True)

    cursor.execute(query,tuple(values))

    attendance=cursor.fetchall()
    cursor.close()
    return jsonify(attendance),200

@attendance_bp.route("/attendance/report/<int:student_id>",methods=["GET"])
def attendance_report(student_id):
    cursor=db.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT
    students.id AS student_id,
    students.name AS student_name,
    COUNT(attendance.id) AS total_classes,
    SUM(attendance.status = 'Present') AS present,
    SUM(attendance.status = 'Absent') AS absent,
    ROUND(
        SUM(attendance.status = 'Present') * 100.0 /
        COUNT(attendance.id),
        2
    ) AS attendance_percentage
    FROM students
    JOIN attendance
    ON students.id = attendance.student_id
    WHERE students.id = %s
    GROUP BY students.id, students.name;
    """,
    (student_id,))

    report=cursor.fetchone()
    if not report:
        cursor.close()
        return jsonify({
            "error": "Student not found or no attendance records"
        }), 404
    return jsonify(report),200


@attendance_bp.route("/attendance/report/<int:student_id>",methods=["GET"])
def attendance_subject_report(student_id):
    subject_id=request.args.get("subject_id",type=int)
    if not subject_id:
        return jsonify({
            "error": "subject_id is required"
        }), 400

    cursor=db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            students.id AS student_id,
            students.name AS student_name,
            subjects.id AS subject_id,
            subjects.name AS subject_name,
            COUNT(attendance.id) AS total_classes,
            SUM(attendance.status = 'Present') AS present,
            SUM(attendance.status = 'Absent') AS absent,
            ROUND(
                SUM(attendance.status = 'Present') * 100.0
                / COUNT(attendance.id),
                2
            ) AS attendance_percentage

        FROM attendance

        JOIN students
            ON attendance.student_id = students.id

        JOIN subjects
            ON attendance.subject_id = subjects.id

        WHERE students.id = %s
        AND subjects.id = %s

        GROUP BY
            students.id,
            students.name,
            subjects.id,
            subjects.name
    """, (student_id, subject_id))

    report=cursor.fetchone()
    cursor.close()
    if not report:
        return jsonify({
            "error":"No attendance records found"
        }),404

    return jsonify(report),200
