from flask import Flask, render_template, request
from flaskwebgui import FlaskUI  #get the FlaskUI class
from estoque import Bloco
from user import User

app = Flask(__name__)

# Feed it the flask app instance
ui = FlaskUI(app, app_mode=False)

# do your logic as usual in Flask


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User().login(request.form.get("email"), request.form.get("password"))
        if user:
            return render_template("inicial.html")
    return render_template("login.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        senha = request.form.get("password")
        confsenha = request.form.get("confpassword")
        user = User(request.form.get("name"), request.form.get("email"), senha)
        if senha == confsenha:
            if user.cadastrar():
                return login()
        else:
            print("Senhas diferentes")
    return render_template("cadastro.html")

@app.route("/recuperação", methods=["GET", "POST"])
def recuperacao():
    if request.method == "POST":
        user = User().recuperarPass(request.form.get("email"))
        if user:
            print("Email Enviado!")
            return index()
        else:
            print("Email Inválido!")
    return render_template("recuperacao.html")


ui.run()
