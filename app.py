import os.path
import pandas as pd
from flask import Flask, render_template, redirect, request, url_for, make_response

app = Flask(__name__, template_folder="templates")

if not os.path.exists("polls.csv"):
    structure = {
        "pid": [],
        "poll": [],
        "option1": [],
        "option2": [],
        "option3": [],
        "option4": [],
        "votes1": [],
        "votes2": [],
        "votes3": [],
        "votes4": []
    }

    pd.DataFrame(structure).set_index("pid").to_csv("polls.csv")

pollsDf = pd.read_csv("polls.csv").set_index("pid")


@app.route("/")
def index():
    return render_template("index.html" , polls=pollsDf)


@app.route("/polls/<pid>")
def pollsfunc(pid):
    # Convert pid to integer
    pid = int(pid)

    # Access the row using .loc[] with the index (pid)
    poll = pollsDf.loc[pid]

    # Return the poll data as a string
    return str(poll)


@app.route("/polls",methods=["GET","POST"])
def create():
    if request.method =="GET":
        pass
    elif request.method =="POST":
        pass

@app.route("/vote/<pid>/<option>")
def vote(pid , option):
    pass

if __name__ == "__main__":
    app.run(host="localhost",debug=True)