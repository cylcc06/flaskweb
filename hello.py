from flask import Flask
from flask import make_response
from flask import request
from flask import redirect
from flask import abort
from datetime import datetime
from flask import render_template
from flask import session
from flask import url_for
from flask import flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from wtforms.validators import DataRequired
# from flask.ext.script import Manager
from flask_script import Manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('submit')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name='<h5>Haha</h5>')


# @app.route('/')
# def index():
#     user_agent=request.headers.get('User-Agent')
#     return 'Your browser is %s' % user_agent

# @app.route('/')
# def index():
#     return 'Bad request!!!',400

# @app.route('/')
# def index():
#     response=make_response('this document caries a cookie!')
#     response.set_cookie('answer','42')
#     return response

# @app.route('/')
# def index():
#     return redirect('http://baidu.com')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internam_server_error(e):
    return render_template('500.html'), 500


# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/')
# def index():
#     return render_template('index.html',current_time=datetime.utcnow())

# @app.route('/',methods=['GET','POST'])
# def index():
#
#     form =NameForm()
#     if form.validate_on_submit():
#         session['name']=form.name.data
#         # 重定向的URL发起GET请求
#         return redirect(url_for('index'))
#     return render_template('index.html',form=form,name=session.get('name'))

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html',form=form, name=session.get('name'))

if __name__ == '__main__':
    manager.run()
