# verifico a pasta do meu projeto, verifico se está no meu github
# git remote -v
# executar
# git pull origin master(main)

# quero clonar omeu projeto em uma pasta vazia
# git clone https://caminho_do_projeto

# instalo a extensão do python
# abro o terminal e verifico se abre no venv, caso não abra no venv devoexecitar:
# ctrl shift p
# e digitar environment e pedir para criar um ambiente virtual 


# pip install flask
# pip install flas-SQLAlchemy
# pip install flask-Migrate
# pip install flask-Script
# pip install pymysql
# flask db init:
# executo quando não tenho a pasta migrations

# flask db migrate -m "Migração Inicial"
# executo quando não tenho o arquivo python na pasta versions

# flask db upgrade
# executo quando minhas tabelas não estão criadas no meu banco de dados

from flask import Flask, render_template, request, flash, redirect
from database import db
from flask_migrate import Migrate
from models import Usuario
app = Flask(__name__)
app.config['SECRET_KEY'] = 'J083H8bs88HSKJI9s886g'

# drive://usuario:senha@servidor/banco_dados
conexao = "mysql+pymysql://alunos:cefetmg@127.0.0.1/lucca"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aula')
@app.route('/aula/<nome>')
@app.route('/aula/<nome>/<curso>')
@app.route('/aula/<nome>/<curso>/<int:ano>')
def aula(nome = 'Maria', curso = 'Informática', ano = 1):
    dados = {'nome': nome, 'curso': curso, 'ano': ano}
    return render_template('aula.html',dados_html=dados)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/dados', methods=['POST'])
def dados():
    dados = request.form
    return render_template('dados.html', dados = dados)

@app.route('/usuario')
def usuario():
    u = Usuario.query.all()
    return render_template('usuario_lista.html', dados = u)

@app.route('/usuario/add')
def usuario_add():
    return render_template('usuario_add.html')

@app.route('/usuario/save', methods=['POST'])
def usuario_save():
    nome = request.form.get('nome')
    email = request.form.get('email')
    idade = request.form.get('idade')
    if nome and email and idade:
        usuario = Usuario(nome, email, idade)
        db.session.add(usuario)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!!!')
        return redirect('/usuario')
    else:
        flash('Preencha todos os campos')
        return redirect('/usuario/add')


@app.route('/usuario/remove/<int:id>')
def usuario_remove(id):
    if id > 0:
        usuario = usuario.query.get(id)
        db.session.remove(usuario)
        db.session.commit()
        flash('Usuario removido com sucesso!!!')
        return redirect('/usuario')
    else:
        flash('Caminho Incorreto!!!')
        return redirect('/usuario')


if __name__ == '__main__':
    app.run()