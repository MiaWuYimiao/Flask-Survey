from flask import Flask, render_template, redirect, request, flash, session, make_response
from surveys import satisfaction_survey, surveys
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    """Home page display survey options to chose"""
    return render_template('home.html', surveys=surveys)


@app.route('/survey', methods=["POST"])
def start_page():
    code = request.form.get('survey_code')
    survey = surveys.get(code)

    # check cookie to see if this survey has been completed
    if request.cookies.get(f"complete_{code}"):
        return render_template("complete_survey.html")

    # Reinitialize new survey session
    session['responses'] = []
    session['no_questions'] = len(survey.questions)
    session['code'] = code

    return render_template('start.html', survey=survey)


@app.route('/start')
def start():
    """Start the survey with the first question"""

    return redirect("/questions/0")


@app.route('/questions/<question_id>')
def question_page(question_id):
    """Render question page"""

    # Check question id
    id = int(question_id)
    responses = session['responses']
    valid_id = len(responses)
    no_questions = session['no_questions']
    survey = surveys.get(session['code'])

    if id != valid_id:
        flash('You are trying to access invalid question page')

    if valid_id < no_questions:
        question = survey.questions[valid_id]
        return render_template('question.html', question=question, question_id = valid_id)
    else:
        return redirect('/thankyou')
    


@app.route('/answer', methods=["POST"])
def answer():
    """Save response and redirect to next question"""

    # get response choice
    answer = request.form["answer"]
    comment = request.form.get("comments", "")

    ans = {
        'answer' : answer,
        'comment': comment
    }

    # add response to the list
    responses = session['responses']
    responses.append(ans)
    session['responses'] = responses

    # Go to thanks page if survey completed
    if len(responses) == session['no_questions']:
        return redirect('/thankyou')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/thankyou')
def thank_you():
    """Say thank you and show all responses"""

    responses = session['responses']
    survey = surveys.get(session['code'])
    questions = survey.questions
    html = render_template('thankyou.html', responses = responses, questions = questions)
    response = make_response(html)

    # set cookie to prevent resubmit until cookie expired
    response.set_cookie(f"complete_{session['code']}", "yes",max_age = 60)
    return response