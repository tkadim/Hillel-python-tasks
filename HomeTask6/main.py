from flask import Flask, jsonify
from flask import render_template, request


app = Flask(__name__)

@app.route("/")
def index():
    # Рендеримо шаблон index.html
    return render_template("index.html")


@app.route("/contacts")
def contacts():
    return render_template("contacts.html")


@app.route("/submit", methods=["POST"])
def submit():
    message = request.form.get("message")
    return render_template("contacts.html", msg=message)


@app.route("/api/get_user_info/<int:user_id>", methods=["GET"])
def get_user(user_id):
    return jsonify({
        "id": user_id,
        "name": "Tom",
        "is_active": False
    })


app.run(debug=True)