from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, URL, Regexp


class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email(message="El correo debe ser de la forma ejemplo@ejemplo.com")])
    nickname = StringField('Usuario', validators=[DataRequired(), Regexp('^\w+$',message="No se permiten carácteres especiales"), Length(max=64)])
    submit = SubmitField('Registrar')


class LoginForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar sesión')


class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])
    title_slug = StringField('Título slug', validators=[Length(max=128)])
    asignatura = StringField('Asignatura', validators=[DataRequired(), Length(max=128)])
    tema = StringField('Tema', validators=[DataRequired(), Length(max=128)])
    autor = StringField('Autor/a', validators=[DataRequired(), Length(max=128)])
    content = TextAreaField('Contenido')
    url = StringField('Dirección web', validators=[URL(require_tld=True)])
    submit = SubmitField('Enviar')


class ContactForm(FlaskForm):
    nombre = StringField('Tu nombre', validators=[DataRequired(), Length(max=64)])
    correo = StringField('Tu correo', validators=[DataRequired(), Email(message="El correo debe ser de la forma ejemplo@ejemplo.com")])
    asunto = StringField('Asunto', validators=[DataRequired(), Length(max=128)])
    mensaje = TextAreaField('Mensaje')
    submit = SubmitField('Enviar')
