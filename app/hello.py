import os
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
from flask_sqlalchemy import SQLAlchemy
from flask_script import Shell
from flask_migrate import Migrate,MigrateCommand
from flask_mail import Mail
from flask_mail import Message
from threading import Thread

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/flask'
app.config['QLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#mail
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'cylcc006@gmail.com'
app.config['FLASKY_ADMIN'] = 'cylcc06@126.com'

mail=Mail(app)
db = SQLAlchemy(app)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
from flask_script import Shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=app))
migrate=Migrate(app,db)
manager.add_command('db',MigrateCommand)

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

# def send_email(to, subject, template, **kwargs):
#     msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
#     msg.body = render_template(template + '.txt', **kwargs)
#     msg.html = render_template(template + '.html', **kwargs)
#     mail.send(msg)
def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # 在关系的另一个模型中添加反向引用
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' % self.username

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

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm()
#     if form.validate_on_submit():
#         old_name = session.get('name')
#         if old_name is not None and old_name != form.name.data:
#             flash('Looks like you have changed your name!')
#         session['name'] = form.name.data
#         return redirect(url_for('index'))
#     return render_template('index.html',form=form, name=session.get('name'))

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.name.data).first()
#         if user is None:
#             user = User(username=form.name.data)
#             db.session.add(user)
#             session['known'] = False
#         else:
#             session['known'] = True
#         session['name'] = form.name.data
#         form.name.data = ''
#         return redirect(url_for('index'))
#     return render_template('index.html',
#                        form=form, name=session.get('name'),
#                        known=session.get('known', False))
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User','mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data

        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),known=session.get('known', False))

# if __name__ == '__main__':

#     manager.run()
