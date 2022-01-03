from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:postgres@localhost/height_collector"
db = SQLAlchemy(app)

"""
Call the 'db' from venv terminal.

> from app import db
> db.create_all()  # To make the table + columns
"""


class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    email_ = db.Column(db.String(120), unique=True)
    height_ = db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_ = email_
        self.height_ = height_


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/success", methods=["POST"])  # The default is GET method
def success():
    if request.method == "POST":
        email = request.form["email_name"]
        height = request.form["height_name"]

        if db.session.query(Data).filter(Data.email_ == email).count() == 0:
            data = Data(email, height)
            db.session.add(data)  # The data is the obj instance above
            db.session.commit()
            avg_height = db.session.query(func.avg(Data.height_)).scalar()
            avg_height = round(avg_height, 1)
            count = db.session.query(Data.height_).count()
            send_email(email, height, avg_height, count)
            return render_template("success.html")

        return render_template(
            "index.html", text="That email address had been added previously!"
        )


if __name__ == "__main__":
    app.debug = True
    app.run()
