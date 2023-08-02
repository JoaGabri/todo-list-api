from flask import Flask,render_template,request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)


#aqui eu crio a tabela para a minha API
class Todo(db.Model):
    task_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    done=db.Column(db.Boolean)


#a rota principal da minha API
@app.route('/')
def home():
    ## Primeiro eu crio a variavel todo_list atribuo ela a tabela Todo
    todo_list=Todo.query.all()
    #aqui eu renderizo o base.html e de parametro eu passo a variavel todo_list para o meu código HTML, com isso meu código consegue entender python dentro do HTML
    return render_template('base.html', todo_list=todo_list)


# a rota para adicionar uma tarefa
@app.route('/add', methods=['POST'])
def add():
    #a variavel name se atribui ao método POst a onde se entrega o Name
    name = request.form.get("name")
    new_task=Todo(name=name,done=False)
    #aqui ele adiciona a variavel new_task e sobe ao DB
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.get(todo_id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("home"))


@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

if __name__=='__main__':
    app.run()
    

    

