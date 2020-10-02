from app import app
import users
import courses
import questions
import students
from flask import render_template, request, session, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

@app.route("/")
def index():
    courselist = courses.get_courses()
    return render_template("index.html", courses = courselist)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        firstname=request.form["firstname"]
        status=request.form["status"]
        lastname=request.form["lastname"]
        username=request.form["username"] 
        password=request.form["password"]
        if len(firstname) > 30 or len(lastname) > 30 or len(username) > 30 or len(password) > 30:
            return render_template("error.html", message="Jokin rekisteröinnin syötteistä on liian pitkä. Maksimi on 30 merkkiä.")
        if firstname == "" or lastname == "" or status == "" or username == "" or password == "":
            return render_template("error.html", message="Kenttää ei voi jättää tyhjäksi.")
        if users.register(firstname,lastname,username,password,status):
            return redirect("/welcome")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username,password):
        return redirect("/welcome")
    else:
        return render_template("error.html", message="Kirjautuminen ei onnistunut")

@app.route("/welcome",methods=["GET"])
def welcome():
    id = users.user_id()
    nimi = users.user_firstname(users.user_all(id))
    if users.is_admin(id):
        courselist = courses.get_courses()
        userlist = users.get_users()
        userlist.sort(key=lambda x: x[5])
        return render_template("welcome_admin.html", name = nimi, courses = courselist, users = userlist)
    elif users.is_teacher(id):
        course = courses.get_course_with_teacher(id)
        return render_template("welcome_teacher.html", name = nimi, courses = course)
    elif users.is_student(id):
        mycourselist = students.get_courses(id)
        courselist = courses.get_courses()
        return render_template("welcome_student.html", name = nimi, courses = courselist, mycourses = mycourselist)
    else:
        return render_template("error.html", message="Jokin meni vikaan")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "GET":
        return render_template("new.html")
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        level = request.form["level"]
        content = request.form["content"]
        keyword = request.form["keyword"]
        teacher_id = users.user_id()
        if len(title) > 100 or len(content) > 10000 or len(keyword) > 30 or len(description) > 250:
            return render_template("error.html", message="Jokin syötteistä on liian pitkä. Otsikko max. 100, kuvaus max. 250, kurssiteksti max. 10 000 ja avainsana max. 30 merkkiä.")
        if title == "" or content == "" or keyword == "" or description == "":
            return render_template("error.html", message="Kenttää ei voi jättää tyhjäksi.")
        if courses.new_course(title,description,level,content,keyword,teacher_id):
            return redirect("/welcome")
        else:
            return render_template("error.html", message="Kurssin luominen ei onnistunut")

@app.route("/courses/<int:id>", methods=["GET"])
def course(id):
    course = courses.get_course_with_id(id)
    title = course[1]
    description = course[2]
    level = course[3]
    content = course[4]
    keyword = course[5]
    #get question and choices
    questionlist = questions.get_questions_with_course_id(id)
    return render_template("course.html", title=title, description = description, level=level, content=content, keyword=keyword, id=id, questions=questionlist)

@app.route("/courses/<int:id>/newquestion", methods=["GET", "POST"])
def newquestion(id):
    if request.method == "GET":
        course = courses.get_course_with_id(id)
        title = course[1]
        return render_template("newquestion.html", course_title = title, id = id)
    if request.method == "POST":
        question = request.form["question"]
        course_id = id
        choices = request.form.getlist("choice")
        for choice in choices:
            if len(choice) > 500:
                return render_template("error.html", message="Vastausvaihtoehto on liian pitkä, max. 500 merkkiä")
        if len(question) > 500:
            return render_template("error.html", message="Kysymys on liian pitkä, max. 500 merkkiä")
        if question == "" or len(choices) == 0:
            return render_template("error.html", message="Kysymystä ei voi jättää tyhjäksi ja ainakin yksi vastausvaihtoehto pitää olla")
        if questions.new_question(question, course_id, choices):
            return redirect("/welcome")
        else:
            return render_template("error.html", message="Kysymyksen luominen ei onnistunut")

# Muistilappu: Ei osaa vielä tarkistaa, että ainakin yksi vastausvaihtoehto on annettu.

@app.route("/join", methods=["POST"])
def join():
    course_id = request.form["course_id"]
    if students.join(users.user_id(),course_id):
        return redirect("/welcome")
    else:
        return render_template("error.html", message="Kurssille liittyminen ei onnistunut")

@app.route("/leave", methods=["POST"])
def leave():
    course_id = request.form["course_id"]
    if students.leave_course(users.user_id(),course_id):
        return redirect("/welcome")
    else:
        return render_template("error.html", message="Kurssilta poistuminen ei onnistunut")

    
