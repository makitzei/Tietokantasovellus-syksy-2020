from db import db
from flask import session

def new_course(title, level, content, keyword, teacher_id):
    try:
        sql = "INSERT INTO courses (title, level, content, keyword, teacher_id) VALUES (:title, :level, :content, :keyword, :teacher_id)"
        db.session.execute(sql, {"title":title,"level":level,"content":content,"keyword":keyword,"teacher_id":teacher_id})
        db.session.commit()
        return True
    except:
        return False

def get_course_with_teacher(id):
    sql = "SELECT id, title FROM courses WHERE teacher_id =:teacher_id"
    result = db.session.execute(sql, {"teacher_id":id})
    courses = result.fetchall()
    return courses

def get_course_with_id(id):
    sql = "SELECT * FROM courses WHERE id =:id"
    result = db.session.execute(sql, {"id":id})
    course = result.fetchone()
    return course   