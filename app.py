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
    return render_template("showPOLL.html" , poll=poll)


@app.route("/polls",methods=["GET","POST"])
def create():
    if request.method =="GET":
        return render_template("newPOLL.html")
    elif request.method =="POST":
        poll = request.form['poll']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        pollsDf.loc[max(pollsDf.index.values)+1] = [poll , option1 , option2 , option3 , option4 , 0 , 0 , 0 , 0]
        pollsDf.to_csv("polls.csv")
        return redirect(url_for('index'))


@app.route("/vote/<pid>/<option>")
def vote(pid , option):
    if request.cookies.get(f"vote_{pid}_cookie") is None:
        pollsDf.at[int(pid),"votes"+str(option)]+= 1
        response = make_response(redirect(url_for('pollsfunc' , pid = pid)))
        response.set_cookie(f"vote_{pid}_cookie",str(option))
        return response
    else:
        return "cannot vote more than once"

if __name__ == "__main__":
    app.run(host="localhost",debug=True)