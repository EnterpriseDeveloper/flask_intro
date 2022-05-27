from flask import Flask, render_template, request, redirect
from helpers.dynamodb import DynamoDB
from datetime import datetime
import sys
import logging

app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        table = DynamoDB()

        try:
            table.addItem(task_content)
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        table = DynamoDB()
        tasks = table.getListItem()
        if len(tasks) > 1:
            tasks = sorted(
                tasks,
                key=lambda x: datetime.strptime(x['date_created'], "%d-%b-%Y (%H:%M:%S)"), reverse=False
            )
        return render_template('index.html', tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    try:
        DynamoDB().delteItem(id)
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = DynamoDB().getItem(id)

    if request.method == 'POST':
        content = request.form['content']

        try:
            DynamoDB().updateItem(id, content)
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
