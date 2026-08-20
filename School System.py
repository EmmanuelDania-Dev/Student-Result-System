from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "46-$)29!$!$fhsldbf463"

students = []

def get_grade(score):
    if score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"

@app.route('/', methods=["GET", "POST"])
def home():

    if request.method == "POST":

        name = request.form.get("name")
        selected_class = request.form.get("class")
        score = int(request.form.get("score"))
        if score > 100 or score < 0:
            flash("Score must be between 0 and 100", "danger")
            return redirect(url_for("home"))
        grade = get_grade(score)

        if len(students) == 0:
            get_id = 1
        else:
            get_id = max(student['id'] for student in students) + 1

        students.append({
            "id": get_id,
            "name": name,
            "class": selected_class,
            "score": score,
            "grade": grade
        })


        return redirect(url_for("view_students"))

    return render_template("home.html", students=students)


@app.route('/view_students')
def view_students():

    return render_template("view.html", students=students)


@app.route('/del_student/<int:student_id>', methods=["POST"])
def delete_student(student_id):

    for student in students:

        if student['id'] == student_id:

            student_name = student['name']

            students.remove(student)

            flash(
                "Student" + ' ' + student["name"] + ' ' +  "was deleted successfully.",
                "success"
            )

            break

    else:
        flash("Student not found.", "danger")

    return redirect(url_for("view_students"))


@app.route('/edit_student/<int:student_id>', methods=["GET", "POST"])
def edit(student_id):

    student = next(
        (s for s in students if s['id'] == student_id),
        None
    )

    if student is None:
        flash("Student not found.", "danger")
        return redirect(url_for("view_students"))

    if request.method == "POST":

        student['name'] = request.form.get('name')
        student['class'] = request.form.get('class')

        score = int(request.form.get('score'))

        # Validate score BEFORE updating the student
        if score > 100 or score < 0:
            flash("Score must be between 0 and 100", "warning")
            return redirect(url_for('edit', student_id=student_id))

        student['score'] = score

        # Automatically calculate the grade
        student['grade'] = get_grade(score)

        flash(
            "Student " + student["name"] + " was updated successfully.",
            "success"
        )

        return redirect(url_for('view_students'))

    return render_template("edit.html", student=student)

if __name__ == '__main__':
    app.run(debug=True)