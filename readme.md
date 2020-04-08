# 2020 A'Level Computing Revision Quiz (beta)
#### a save the world X project

## Features
#### Login
1. Not Secure Login Feature using email(Flask-mail Library). Wanted to try this out as an alternative method to login in w/o passwords.

2. Preventing random users from joining unauthorised app routes. Poses a problem when users who are not logged in try the questionaire. UserID (Primary Key) is used to identify users, thus this was implemented

#### Questionaires
(Every expected feature seems like an obstacle to implement)
1. Random retrieving of questions

2. Collection of scores and displaying them on a leaderboard, sorted by scores and attempts

3. Notifying user the questions which went wrong and displaying them after the user submits


9. Bugs are features too

## Learning Points
1. [Using Flask session!](https://flask.palletsprojects.com/en/1.1.x/api/#flask.session). Tried not to use other libraries such as Flask-Login, but instead stored current user variables using the session.

Benefit: Like a **global variable**, it can be accessed across functions, but applies to different sessions (eg. multiple user using the application).

2. "kinda" dynamic form generation

Here is an example form table from algo.html:
![image](https://user-images.githubusercontent.com/47784720/78775616-14a58280-79c9-11ea-8a29-41941cd34b68.png)

Other than jinja to send info to a form, in order for one to retrieve a value from a form, one can make use of the method below:
``` python
request.form.get('algo_answer1') #use a name identifier
```

The problem arises when one wants to access the values of multiple dynamic forms. JS? JQuery array?

A while loop can suffice too

```python
for i in range(len(form)):
        chosen = 'algo_answer'+str(i)
        something = request.form.get(chosen)
```

## Maybe..hmm
1. Extracting of questions from computing google sheet automatically with apps script
2. Cyber Security Questions
