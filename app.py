from services import *
from flask import Flask, jsonify
import os
from dotenv import load_dotenv

# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

OFFICES_JSON_FILE_PATH = os.getenv('OFFICES_JSON_FILE_PATH', 'offices.json')
DEPARTMENTS_JSON_FILE_PATH = os.getenv('DEPARTMENTS_JSON_FILE_PATH', 'departments.json')
EMPLOYEES_URL = os.getenv('EMPLOYEES_URL', 'https://rfy56yfcwk.execute-api.us-west-1.amazonaws.com/bigcorp/employees')

offices_repository = OfficeRepository.create_repository_from_file('offices.json')
departments_repository = DepartmentRepository.create_repository_from_file('departments.json')
employees_repository = EmployeeRepository.create_repository_from_url('https://rfy56yfcwk.execute-api.us-west-1.amazonaws.com/bigcorp/employees')

app = Flask(__name__)

paginator = LimitOffsetPaginator()
expander = Expander({
    'manager': employees_repository,
    'superdepartment': departments_repository,
    'department': departments_repository,
    'office': offices_repository
})

@app.route('/')
def index():
    return 'Server Works!'

@app.route('/offices', methods=['GET'])
def list_offices():
    limit = paginator.get_limit() if paginator.get_limit() is not None else 10
    offset = paginator.get_offset() if paginator.get_offset() is not None else 0
    response = expander.solve_expandables(offices_repository.page(limit, offset))
    return jsonify(response)

@app.route('/departments', methods=['GET'])
def list_departments():
    limit = paginator.get_limit() if paginator.get_limit() is not None else 10
    offset = paginator.get_offset() if paginator.get_offset() is not None else 0
    response = expander.solve_expandables(departments_repository.page(limit, offset))
    return jsonify(response)

@app.route('/employees', methods=['GET'])
def list_employees():
    limit = paginator.get_limit() if paginator.get_limit() is not None else 10
    offset = paginator.get_offset() if paginator.get_offset() is not None else 0
    response = expander.solve_expandables(employees_repository.page(limit, offset))
    return jsonify(response)
