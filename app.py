from flask import Flask, render_template, redirect, request, flash
from surveys import satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def home_page():
    return render_template('home.html', survey=satisfaction_survey)


@app.route('/start', methods=["POST"])
def start():
    """Start the survey with the first question"""

    return redirect("/questions/0")

@app.route('/questions/<question_id>')
def question_page(question_id):
    # Check and correct question id
    id = int(question_id)
    valid_id = len(responses)
    if id != valid_id:
        flash('You are trying to access invalid question page')

    if valid_id < len(satisfaction_survey.questions):
        question = satisfaction_survey.questions[valid_id]
        return render_template('question.html', question=question, question_id = valid_id)
    else:
        return redirect('/thankyou')
    


@app.route('/answer', methods=["POST"])
def answer():
    """Save response and redirect to next question"""

    # get response choice
    ans = request.form["answer"]

    # add response to the list
    responses.append(ans)

    # Go to thanks page if survey completed
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thankyou')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')