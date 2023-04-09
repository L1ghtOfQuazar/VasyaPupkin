from os import abort
from flask import Flask, render_template, redirect, request
from data import db_session
from data.users import User
from data.blogs import Blog
from data.musics import Music
from forms.user import RegisterForm
from forms.login import LoginForm
from forms.blog import BlogForm
from forms.music import MusForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
stra = ''
sh = 0


def main():
    db_session.global_init("db/mainu.db")
    app.run(port=8080, host='127.0.0.1')


@app.route('/index', methods=['GET', 'POST'])
def index():
    global stra
    stra = '/index'
    return render_template('index.html', title='Главная')


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    global stra
    stra = '/blog'
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(Blog).filter(
            (Blog.user == current_user) | (Blog.is_private != True)).order_by(Blog.id.desc())
    else:
        news = db_sess.query(Blog).filter((Blog.is_private != True)).order_by(Blog.id.desc())
    return render_template('blog.html', news=news, title='Блог')


@app.route('/blogn',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = BlogForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        f = Blog()
        f.title = form.title.data
        f.content = form.content.data
        f.is_private = form.is_private.data
        current_user.blog.append(f)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/blog')
    return render_template('blogn.html', title='Добавление новости',
                           form=form)


@app.route('/blogn/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = BlogForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(Blog).filter(Blog.id == id,
                                          Blog.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(Blog).filter(Blog.id == id,
                                          Blog.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return render_template('blogn.html',
                                   title='Редактирование новости', message="Успешно изменено!",
                                   form=form
                                   )
            return redirect('/blog')
        else:
            abort(404)
    return render_template('blogn.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/blogd/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    global sh
    db_sess = db_session.create_session()
    news = db_sess.query(Blog).filter(Blog.id == id,
                                      Blog.user == current_user
                                      ).first()
    if news and sh < 1:
        sh = sh + 1
    elif news and sh == 1:
        db_sess.delete(news)
        db_sess.commit()
        sh = 0
    else:
        abort(404)
        sh = 0
    return redirect('/blog')


@app.route('/eu', methods=['GET', 'POST'])
def eu():
    global stra
    stra = '/eu'
    return render_template('eu.html', title='Оборудование')


@app.route('/pioneercdj3000', methods=['GET', 'POST'])
def page1():
    global stra
    stra = '/pioneercdj3000'
    return render_template('pioneercdj3000.html', title='Pioneer-CDJ3000')


@app.route('/pioneerdjm900nxs2', methods=['GET', 'POST'])
def page2():
    global stra
    stra = '/pioneerdjm900nxs2'
    return render_template('pioneerdjm900nxs2.html', title='Pioneer DJM-900NXS2')


@app.route('/novationlaunchpadmk2', methods=['GET', 'POST'])
def page3():
    global stra
    stra = '/novationlaunchpadmk2'
    return render_template('novationlaunchpadmk2.html', title='Novation Launchpad MK2')


@app.route('/sennheiserhd25', methods=['GET', 'POST'])
def page4():
    global stra
    stra = '/sennheiserhd25'
    return render_template('sennheiserhd25.html', title='Sennheiser HD-25')


@app.route('/music', methods=['GET', 'POST'])
def music():
    global stra
    stra = '/music'
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        mus = db_sess.query(Music)
    else:
        mus = db_sess.query(Music)
    return render_template('music.html', music=mus, title='Музыка')


@app.route('/musicn',  methods=['GET', 'POST'])
@login_required
def add_music():
    form = MusForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        f = Music()
        f.name = form.name.data
        f.link = form.link.data
        f.genre = form.genre.data
        current_user.music.append(f)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/music')
    return render_template('musicn.html', title='Добавление трека',
                           form=form)


@app.route('/musicn/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_music(id):
    form = MusForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        mus = db_sess.query(Music).filter(Music.id == id,
                                          Music.user == current_user
                                          ).first()
        if mus:
            form.name.data = mus.name
            form.link.data = mus.link
            form.genre.data = mus.genre
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        music = db_sess.query(Music).filter(Music.id == id,
                                          Music.user == current_user
                                          ).first()
        if music:
            music.name = form.name.data
            music.link = form.link.data
            music.genre = form.genre.data
            db_sess.commit()
            return render_template('musicn.html',
                                   title='Редактирование трека', message="Успешно изменено!",
                                   form=form
                                   )
            return redirect('/music')
        else:
            abort(404)
    return render_template('musicn.html',
                           title='Редактирование трека',
                           form=form
                           )


@app.route('/musicd/<int:id>', methods=['GET', 'POST'])
@login_required
def music_delete(id):
    global sh
    db_sess = db_session.create_session()
    mus = db_sess.query(Music).filter(Music.id == id,
                                      Music.user == current_user
                                      ).first()
    if mus and sh < 1:
        sh = sh + 1
    elif mus and sh == 1:
        db_sess.delete(mus)
        db_sess.commit()
        sh = 0
    else:
        abort(404)
        sh = 0
    return redirect('/music')


@app.route('/music/<id>', methods=['GET', 'POST'])
def music_c(id):
    global stra
    stra = '/music'
    db_sess = db_session.create_session()
    if id.isdigit():
        mus = db_sess.query(Music).order_by(Music.id.desc())
    else:
        mus = db_sess.query(Music).filter(Music.genre == id).order_by(Music.id.desc())
    return render_template('music.html', music=mus, title='Музыка')


@app.route('/social', methods=['GET', 'POST'])
def social():
    global stra
    stra = '/social'
    return render_template('social.html', title='Соцсети')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    global stra
    stra = '/register'
    db_session.global_init("db/mainu.db")
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Подать заявку',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first() or db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('register.html', title='Подать заявку',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return render_template('register.html', title='Подать заявку', form=form, message="Успешно отправлено!")
    return render_template('register.html', title='Подать заявку', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global stra
    stra = '/login'
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data) and user.c == 1:
            login_user(user, remember=form.remember_me.data)
            return redirect("/index")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    global stra
    logout_user()
    return redirect(stra)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    main()
