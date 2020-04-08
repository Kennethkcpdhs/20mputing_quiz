from flask import *
from flask_mail import Mail, Message
import sqlite3
import os
import bcrypt

app = Flask(__name__)

'''configs'''
app.config['MAIL_SERVER']='smtp.gmail.com'
#default mail port is 25
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get("SECRET_MAIL","")
app.config['MAIL_PASSWORD'] = os.environ.get("SECRETPASS","")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
#os.urandom(12).hex()
app.config['SECRET_KEY'] = 'f3cfe9ed8fae309f02079dbf'

mail = Mail(app) #start Mail class

#home page
@app.route("/index")
def index():
    try:
        curr_user = session['curr_user_email']
    except:
        return redirect(url_for("unauthorised"))
    return render_template('index.html')

#default login page
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == 'POST':
        e = sqlite3.connect('data1.db')
        c = e.cursor()
        email_link = str(request.form.get('email'))
        pwd = str(request.form.get('pwd'))

        if not pwd: #user forgets to enter password
            return render_template_string('''
                <html>
                    <head>
                        <meta http-equiv="refresh" content="2;url=/" />
                    </head>
                    <body>
                    <style>
                        .alert {
                          padding: 20px;
                          background-color: #383486;
                          color: white;
                          font-family: sans-serif;
                        }
                    </style>
                    <div class="alert">
                        <h1>You did not enter your password! Please try again.</h1>
                        <h2>Redirecting in 2 seconds...</h2>
                    </div>
                    </body>
                </html>
            ''')

        check = c.execute('''SELECT UserID,Email From User WHERE UserID=? AND Email=?''',(pwd,email_link,))
        check = check.fetchall()
        e.commit()
        c.close()
        print(check)
        if check != []: #user enters correct password
            session['curr_user_email'] = email_link
            session['pwd'] = pwd
            return render_template_string("""
                <html>
                    <head>
                        <meta http-equiv="refresh" content="2;url=/index" />
                    </head>
                    <body>
                        <style>
                            .alert {
                              padding: 20px;
                              background-color: #00b966;
                              color: white;
                              font-family: sans-serif;
                            }
                        </style>
                        <div class="alert">
                            <h1>Logged in successfully with {{ email_link }}! Redirecting in 2 seconds...</h1>
                        </div>
                    </body>
                </html>
            """, email_link=email_link)
        else: #user enters wrong password
            return render_template_string('''
                <html>
                    <head>
                        <meta http-equiv="refresh" content="2;url=/" />
                    </head>
                    <body>
                        <style>
                            .alert {
                              padding: 20px;
                              background-color: #d05e00;
                              color: white;
                              font-family: sans-serif;
                            }
                        </style>
                        <div class="alert">
                            <h1>You entered your password wrongly! Please try again.</h1>
                            <h2>Redirecting in 2 seconds...</h2>
                        </div>
                    </body>
                </html>
            ''')

    else:
        return render_template('login.html')

#new user registering, re-routed from login
@app.route("/register", methods=["GET","POST"])
def register():
    e = sqlite3.connect('data1.db')
    c = e.cursor()
    if request.method == "POST":
        email_link = str(request.form.get('email'))
        print("Email",email_link)

        #check for existing user
        instr = c.execute('''SELECT UserID From User WHERE Email=?''',(email_link,))
        codedata = instr.fetchall()
        print(codedata)

        if codedata == []: #if new user registering
            c.execute('''INSERT INTO User(Email) VALUES(?)''',(email_link,))
            instr = c.execute('''SELECT UserID,Email From User WHERE Email=?''',(email_link,))
            codedata = instr.fetchall()
            e.commit()

        #Sending of emails to the selected user accounts
        msg = Message('MCQ App Login',
                    sender='dante.mossfield@gmail.com')
        msg.recipients=[email_link]
        print("data",codedata[0][0])
        msg.body = 'Here is your password, \n'+str(codedata[0][0])+'\nThe password is deliberately made insecure, take care of it.'
        mail.send(msg)
        return render_template_string('''
            <html>
                <head>
                    <meta http-equiv="refresh" content="3;url=/" />
                </head>
                <body>
                    <style>
                        .alert {
                          padding: 20px;
                          background-color: #00a8a3;
                          color: white;
                          font-family: sans-serif;
                        }
                    </style>
                    <div class="alert">
                        <h1>Your password has been sent successfully via email to {{ email_link }}</h1>
                        <h2>Check your email</h2>
                        <h2>Redirecting in 3 seconds...</h2>
                    </div>
                </body>
            </html>
        ''', email_link = email_link)

    else:
        c.close()
        return render_template('register.html')


@app.route("/cyber")
def cyber():
    try:
        curr_user = session['curr_user_email']
    except:
        return redirect(url_for("unauthorised"))
    return render_template('cyber.html')

#prevent users who are not logged in from accessing
@app.route("/unauthorised")
def unauthorised():
    return render_template_string('''
        <html>
            <head>
                <meta http-equiv="refresh" content="3;url=/" />
            </head>
            <body>
                <style>
                    .alert {
                      padding: 20px;
                      background-color: #b34507;
                      color: white;
                      font-family: sans-serif;
                    }
                </style>
                <div class="alert">
                    <h1>Unauthorised user. You have yet to log in</h1>
                    <h2>We will be redirecting you to the log-in page in 3 seconds...</h2>
                </div>
            </body>
        </html>
    ''')

@app.route("/algo", methods=["GET","POST"])
def algo():

    #extracting current user details
    if request.method == "POST":
        #open database only when authorised
        e = sqlite3.connect('data1.db')
        c = e.cursor()

        response = []
        #correction = dict() #dict to store the user and actual answer
        for i in range(4):
            chosen = 'algo_answer'+str(i)
            print("algoans",str(request.form.get(chosen)))
            response.append(str(request.form.get(chosen)))
        total = 5*int(len(response))
        score = 0
        count = 0

        #retrieving intended answers
        answer = session['answer']
        curr_user = session['curr_user_email']

        #calculation of scores
        while count<len(response):
            if response[count] == answer[count]:
                score+=5
            count+=1

        #storing of answers for display
        session['response'] = response
        session['score'] = score

        id = session['pwd']

        #storing of highest scores in the database
        ins = c.execute('''SELECT NumAttempts, HighestScore FROM Attempt WHERE USERID=?''',(id,))
        vals = ins.fetchall()
        print("oof",vals)

        if vals != []: #user had multiple attempts
            numattempts = vals[0][0]
            numattempts+=1

            highestscore = vals[0][1]

            #highest score lower than current score
            if highestscore < score:
                highestscore = score
                c.execute('''UPDATE Attempt SET HighestScore=?, NumAttempts=? WHERE UserID=?''',(highestscore,numattempts,id,))
            else: #current score lower than highest score
                c.execute('''UPDATE Attempt SET NumAttempts=? WHERE UserID=?''',(numattempts,id,))

        else: #no previous attempt
            highestscore = score
            numattempts = 1
            c.execute('''INSERT INTO Attempt(UserID,HighestScore,NumAttempts,Email) VALUES(?,?,?,?)''',(id,highestscore,numattempts,curr_user,))


        e.commit()
        c.close()
        return redirect(url_for("score"))

    else:
        try:
            curr_user = session['curr_user_email']
        except:
            return redirect(url_for("unauthorised"))

        e = sqlite3.connect('data1.db')
        c = e.cursor()
        name = curr_user.split("@")[0].split(".")[1].upper() #extracting name

        #getting questions
        instr = c.execute('''SELECT QuestionText,Option1,Option2,Answer From Question ORDER BY RANDOM() LIMIT 4''')
        codedata = instr.fetchall()
        questions = []
        options1 = []
        options2 = []
        answer = []
        for k in range(len(codedata)):
            questions.append(codedata[k][0])
            options1.append(codedata[k][1])
            options2.append(codedata[k][2])
            answer.append(codedata[k][3])

        #store options for mcq questions
        session['answer'] = answer
        session['questions'] = questions
        session['options1'] = options1
        session['options2'] = options2

        e.commit()
        c.close()
        return render_template('algo.html',curr_user=curr_user, name=name,questions=questions, options1=options1, options2=options2,answer = answer)

@app.route("/score")
def score():
    try:
        curr_user = session['curr_user_email']
    except:
        return redirect(url_for("unauthorised"))

    #getting current user stats
    curr_score = session['score']
    curr_user = session['curr_user_email']
    name = curr_user.split("@")[0].split(".")[1].upper() #extracting name
    answer = session['answer']
    questions = session['questions']
    response = session['response']
    options1 = session['options1']
    options2 = session['options2']

    wrong = []
    correct = []
    #extracting wrong answers
    for k in range(len(response)):
        if answer[k] != response[k]:
            if answer[k] == "Option1": #adding corresponding answers
                wrong.append([questions[k],options2[k],options1[k]])
            else:
                wrong.append([questions[k],options1[k],options2[k]])
        else:
            correct.append([questions[k],response[k],answer[k]])

    return render_template('score.html', curr_score = curr_score, curr_user = curr_user, name=name, wrong=wrong)

@app.route("/leaderboard")
def leaderboard():
    try:
        curr_user = session['curr_user_email']
    except:
        return redirect(url_for("unauthorised"))

    e = sqlite3.connect('data1.db')
    c = e.cursor()
    instr = c.execute('''SELECT Email, HighestScore, NumAttempts FROM Attempt ORDER BY HighestScore DESC,NumAttempts ASC LIMIT 2''')
    winners = instr.fetchall()
    #changing all tuples to a list
    print(winners[0])
    finwinners = []
    try: #nested array
        for m in range(len(winners)):
            finwinners.append([winners[m][0],winners[m][1],winners[m][2]])
    except: #not nested array
        for m in range(3):
            finwinners.append([winners[m],winners[m],winners[m]])

    print(finwinners)
    for k in finwinners:
        new = k[0]
        k[0] = new.split("@")[0].split(".")[1].upper()
    numppl = len(finwinners)
    return render_template('leaderboard.html',winners=finwinners, numppl=numppl)

if __name__ == "__main__":
    app.run(debug="True")
