from flask_restful import Api

from departments import SingleDepartment, DepartmentList
from employees import SingleEmployee, EmployeeList
from offices import SingleOffice, OfficesList
from services import *
from flask import Flask
import os
from dotenv import load_dotenv

# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

# some global settings
OFFICES_JSON_FILE_PATH = os.getenv('OFFICES_JSON_FILE_PATH', 'offices.json')
DEPARTMENTS_JSON_FILE_PATH = os.getenv('DEPARTMENTS_JSON_FILE_PATH', 'departments.json')
EMPLOYEES_URL = os.getenv('EMPLOYEES_URL', 'https://rfy56yfcwk.execute-api.us-west-1.amazonaws.com/bigcorp/employees')

# the dependencies to be injected
offices_repository = OfficeRepository.create_repository_from_file('offices.json')
departments_repository = DepartmentRepository.create_repository_from_file('departments.json')
employees_repository = EmployeeRepository.create_repository_from_url('https://rfy56yfcwk.execute-api.us-west-1.amazonaws.com/bigcorp/employees')
expander = Expander({
    'manager': employees_repository,
    'superdepartment': departments_repository,
    'department': departments_repository,
    'office': offices_repository
})

app = Flask(__name__)
api = Api(app)

api.add_resource(SingleOffice, '/offices/<int:office_id>', resource_class_kwargs={'repository': offices_repository})
api.add_resource(OfficesList, '/offices', resource_class_kwargs={'repository': offices_repository,'expander': expander,})
api.add_resource(SingleDepartment, '/departments/<int:department_id>', resource_class_kwargs={'repository': departments_repository})
api.add_resource(DepartmentList, '/departments', resource_class_kwargs={'repository': departments_repository,'expander': expander,})
api.add_resource(SingleEmployee, '/employees/<int:employee_id>', resource_class_kwargs={'repository': employees_repository})
api.add_resource(EmployeeList, '/employees', resource_class_kwargs={'repository': employees_repository,'expander': expander,})

@app.route('/')
def index():
    return 'Server Works!'
