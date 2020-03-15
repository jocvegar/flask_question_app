from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from flask_qa.extensions import db
from flask_qa.models import Question, User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    questions = Question.query.filter(Question.answer != None).all()
    
    context = {
        'questions': questions
    }
    return render_template('home.html', **context)

@main.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':
        question = request.form['question']
        expert   = request.form['expert']

        question = Question(
            question=question, 
            expert_id=expert,
            asked_by_id=current_user.id
        )
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))

    experts = db.session.query(User).filter(User.expert == True).all()

    context = {
        'experts': experts
    }
    return render_template('ask.html', **context) 

@main.route('/answer/<int:question_id>', methods=['POST', 'GET'])
def answer(question_id):
    if not current_user.expert:
        return redirect(url_for('main.index'))

    question = Question.query.get_or_404(question_id)

    if request.method == 'POST':
        question.answer = request.form['answer']
        db.session.commit()

        return redirect(url_for('main.unanswered'))
    
    context = {
        "question": question
    }

    return render_template('answer.html', **context) 

@main.route('/question/<int:question_id>')
def question(question_id):
    question = Question.query.get_or_404(question_id)

    context = {
        'question': question
    }
    return render_template('question.html', **context)  
  
@main.route('/unanswered')
@login_required
def unanswered():
    if not current_user.expert:
        return redirect(url_for('main.index'))

    unanswered_questions = Question.query.filter_by(expert_id=current_user.id).filter(Question.answer == None).all()
    context = {
        'unanswered_questions': unanswered_questions
    }

    return render_template('unanswered.html', **context)

@main.route('/users')
def users():
    if not current_user.admin:
        return redirect(url_for('main.index'))

    users = User.query.filter_by(admin=False).all()

    context = {
        'users': users
    } 
    return render_template('users.html', **context)    

@main.route('/promote/<int:user_id>')
def promote(user_id):
    if not current_user.admin:
        return redirect(url_for('main.index'))

    user = User.query.get_or_404(user_id)

    if user.expert:
        user.expert = False
    else:
        user.expert = True

    db.session.commit()    

    return redirect(url_for('main.users'))
