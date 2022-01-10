from flask import request, jsonify, current_app
from flask_restful import Resource, Api, fields, marshal_with
from .. import db

from ..worker.models import Worker

worker_template = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'surname': fields.String,
    'address': fields.String,
    'email': fields.String,
    'mobile': fields.String,
    'salary': fields.Integer,
    'hired_at': fields.DateTime,
    'grade_id': fields.Integer
}


class WorkersHandlerApi(Resource):
    @marshal_with(worker_template)
    def get(self, id):
        return Worker.query.get_or_404(id)

    @marshal_with(worker_template)
    def post(self, id):
        data = request.get_json()['worker']
        worker_new = Worker(
            first_name=data['first_name'],
            last_name=data['last_name'],
            surname=data['surname'],
            address=data['address'],
            email=data['email'],
            mobile=data['mobile'],
            salary=data['salary'],
            hired_at=db.func.now(),
            grade_id=data['grade_id']
        )

        db.session.add(worker_new)
        db.session.commit()
        return worker_new

    @marshal_with(worker_template)
    def put(self, id):
        data = request.get_json()['worker']
        worker_old = Worker.query.get_or_404(id)
        worker_new = Worker(
            first_name=data['first_name'],
            last_name=data['last_name'],
            surname=data['surname'],
            address=data['address'],
            email=data['email'],
            mobile=data['mobile'],
            salary=data['salary'],
            hired_at=db.func.now(),
            grade_id=data['grade_id']
        )

        worker_old.first_name = worker_new.first_name
        worker_old.last_name = worker_new.last_name
        worker_old.surname = worker_new.surname
        worker_old.address = worker_new.address
        worker_old.email = worker_new.email
        worker_old.mobile = worker_new.mobile
        worker_old.salary = worker_new.salary
        worker_old.hired_at = worker_new.hired_at
        worker_old.grade_id = worker_new.grade_id

        db.session.commit()
        return worker_old

    def delete(self, id):
        worker = Worker.query.get(id)
        db.session.delete(worker)
        db.session.commit()
        return jsonify({'message': 'The worker has been deleted!'})


class WorkersAllHandlerApi(Resource):
    @marshal_with(worker_template)
    def get(self):
        print(Worker.query.all())
        return Worker.query.all()


api = Api(current_app)
api.add_resource(WorkersHandlerApi, "/api/ivanochko/worker/<int:id>")
api.add_resource(WorkersAllHandlerApi, "/api/ivanochko/workers/")
