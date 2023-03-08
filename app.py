from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "toasty"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# responses = []

# *****************************************************************************

@app.route('/')
def survey_home():
    # also pass satisfaction_survey as survey (survey=survey) with the rendered template to use in html 
    return render_template('survey_home.html', survey=survey)

# *****************************************************************************

@app.route('/begin', methods=['POST'])
def set_session():
    session["responses"] = []
    return redirect('/questions/0')

# *****************************************************************************

@app.route('/questions/<int:qid>')
def show_question(qid):
    
    responses = session.get("responses")
    
    if (qid != len(responses)):
        flash(f"You're trying to access an invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")
    
    if (responses is None):
        return redirect("/")
    
    question = survey.questions[qid]
    
    return render_template("/question.html", question_num=qid, question=question)

# *****************************************************************************

@app.route('/answer', methods=["POST"])
def handle_answer():
    
    responses = session["responses"]
    
    choice = request.form['answer']
    responses.append(choice)
    session["responses"] = responses
    
    if (len(responses) == len(survey.questions)):
        return render_template("/thankyou.html")
    
    else:
        return redirect(f"/questions/{len(responses)}")
    
    