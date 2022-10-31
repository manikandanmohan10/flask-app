import imp
from flask.views import MethodView
from flask import request, Response, jsonify, render_template, redirect, url_for
from http import HTTPStatus as status
from src.models.todo_model import ToDo
from src.models import db


class ToDoAPI(MethodView):
    def post(self):
        task = request.form.get('value')
        todo = ToDo(content=task)
        try:
            db.session.add(todo)
            db.session.commit()

            return redirect('/todo/')
        except Exception as e:
            return Response(str(e)), status.BAD_REQUEST
        # redirect('/todo/')

    def get(self):
        tasks = ToDo.query.all()
        return render_template('index.html', tasks=tasks)

    def delete(self):
        try:
            id = request.args.get('id')
            task_to_delete = ToDo.query.get_or_404(id)
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect('/todo/')
        except Exception as e:
            return Response(str(e)), status.BAD_REQUEST

    def patch(self):
        try:
            id = request.args.get('id')
            task_to_update = ToDo.query.get_or_404(id)
            task_to_update = request.form.get('value')
            db.session.commit()

            return redirect('/todo/')
        except Exception as e:
            return Response(str(e)), status.BAD_REQUEST

