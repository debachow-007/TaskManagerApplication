from flask import Blueprint, render_template, request, redirect
from todoapp import db
from todoapp.models import MyTask

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form.get('content')
        new_task = MyTask(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
        
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template('index.html', tasks=tasks)
    
    return render_template('index.html')

@main.route('/delete/<int:id>')
def delete(id):
    task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"

@main.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = MyTask.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form.get('content')
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    else:
        return render_template('update.html', task=task)