from flask import Flask, render_template, request, redirect, url_for, abort
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
import os

from forms import ContactForm, SignupForm, PostForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pi:lusho@186.80.128.29:5432/pi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = "./static/img/entradas"

login_manager = LoginManager(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)

from models import Contact, User, Post


@app.route("/", methods=["GET", "POST"])
def index():
    posts = Post.get_all()
    form = ContactForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        correo = form.correo.data
        asunto = form.asunto.data
        mensaje = form.mensaje.data
        contact = Contact(nombre=nombre, correo=correo, asunto=asunto, mensaje=mensaje)
        contact.save()

    return render_template("index.html", posts=posts, form=form)

@app.route("/search")
def search():
    dato = request.args.get('busqueda')
    if dato:
        post = Post.get_search(dato)
    return render_template("search.html", post=post)


@app.route("/p/<string:asign>")
def category(asign):
    posts = Post.get_by_asign(asign)
    return render_template("asignatura.html", posts=posts)

@app.route("/p/<string:asign>/<string:autor>")
def autor(asign, autor):
    posts = Post.get_by_autor(autor, asign)
    return render_template("autor.html", posts=posts)

@app.route("/p/<string:asign>/<string:autor>/<string:tema>")
def tema(asign, autor, tema):
    posts = Post.get_by_tema(autor, asign, tema)
    return render_template("tema.html", posts=posts)

@app.route("/p/<string:asign>/<string:autor>/<string:tema>/<string:slug>/")
def show_post(slug, asign, tema, autor):
    post = Post.get_by_slug(slug)
    if post is None:
        abort(404)
    return render_template("post_view.html", post=post)


@app.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@app.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
@login_required
def post_form(post_id):
    form = PostForm()
    isAdmin = current_user.is_admin
    if isAdmin == False:
        abort(404)
    elif form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        asignatura = form.asignatura.data
        tema = form.tema.data
        autor = form.autor.data
        url = form.url.data

        post = Post(user_id=current_user.id, title=title, content=content, asignatura=asignatura, tema=tema, autor=autor, url=url)
        post.save()

        return redirect(url_for('upload'))
    return render_template("admin/post_form.html", form=form)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    return render_template("admin/upload.html")

@app.route("/uploader", methods=['POST'])
def uploader():
    post = Post.get_last()
    ide = str(post.id)
    if request.method == 'POST':
        f = request.files['archivo']
        filename = secure_filename(ide)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))       


@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        nickname = form.nickname.data
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese email y nickname
        user = User.get_by_email(email)
        user2 = User.get_by_nick(nickname)
        if user is not None:
            error = f'El email {email} ya está siendo utilizado por otro usuario'
        elif user2 is not None:
            error = f'El usuario {nickname} ya está siendo usado por otra persona'
        else:
            # Creamos el usuario y lo guardamos
            user = User(name=name, email=email, nickname=nickname)
            user.set_password(password)
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template("signup_form.html", form=form, error=error)


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login_form.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
