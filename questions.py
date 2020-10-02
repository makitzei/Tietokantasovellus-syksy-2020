from db import db
from flask import session, request

def new_question(question, course_id, choices):
    try:
        sql = "INSERT INTO questions (question, course_id) VALUES (:question, :course_id) RETURNING id"
        result = db.session.execute(sql, {"question":question,"course_id":course_id})
        question_id = result.fetchone()[0]
        choices = request.form.getlist("choice")
        laskuri = 0
        for choice in choices:
            laskuri +=1
            if choice != "":
                truefalse = "truefalse" + str(laskuri)
                correct = request.form[truefalse]
                sql = "INSERT INTO choices (choice, correct, question_id) VALUES (:choice, :correct, :question_id)"
                db.session.execute(sql, {"choice":choice, "correct":correct, "question_id":question_id})
        db.session.commit()
        return True
    except:
        return False

def get_questions_with_course_id(id):
    sql = "SELECT * FROM questions WHERE course_id=:id"
    result = db.session.execute(sql, {"id":id})
    questions = result.fetchall()
    return questions

"""
def get_choices(question_id):
    sql = "SELECT * FROM choices WHERE question_id=:question_id"
    result = db.session.execute(sql, {"question_id":question_id})
    choices = result.fetchall()
    return choices
"""
