import flask

from services import *
from flask import Flask, jsonify

offices_repository = OfficeRepository.create_repository_from_file('offices.json')
departments_repository = DepartmentRepository.create_repository_from_file('departments.json')
employees_repository = EmployeeRepository.create_repository_from_url('https://rfy56yfcwk.execute-api.us-west-1.amazonaws.com/bigcorp/employees')
app = Flask(__name__)
paginator = LimitOffsetPaginator()
expander = Expander({
    'manager': employees_repository,
    'superdepartment': departments_repository,
    'office':offices_repository
})


@app.route('/')
def index():
    return 'Server Works!'

@app.route('/offices')
def list_offices():
    limit = paginator.get_limit() if paginator.get_limit() is not None else 10
    offset = paginator.get_offset() if paginator.get_offset() is not None else 0
    response = expander.solve_expandables(offices_repository.page(limit, offset))
    return jsonify(response)

@app.route('/departments')
def list_departments():
    limit = paginator.get_limit() if paginator.get_limit() is not None else 10
    offset = paginator.get_offset() if paginator.get_offset() is not None else 0
    response = expander.solve_expandables(departments_repository.page(limit, offset))
    return jsonify(response)

@app.route('/employees')
def list_employees():
    limit = paginator.get_limit() if paginator.get_limit() is not None else 10
    offset = paginator.get_offset() if paginator.get_offset() is not None else 0
    response = expander.solve_expandables(employees_repository.page(limit, offset))
    return jsonify(response)
