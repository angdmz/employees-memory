import json

import requests
from flask import request

class OfficeRepository:

    offices_list = []
    offices_dict = dict()

    def __init__(self, offices):
        self.offices_list = offices

        for o in self.offices_list:
            self.offices_dict[o['id']] = o

    def retrieve(self, officeid):
        return self.offices_dict[officeid]

    def list(self):
        return self.offices_list

    def page(self, limit, offset):
        return self.offices_list[offset:offset + limit]

    @staticmethod
    def create_repository_from_file(file_name):
        with open(file_name) as f:
            offices = json.load(f)
            return OfficeRepository(offices)


class DepartmentRepository:

    department_list = []
    department_dict = dict()

    def __init__(self, offices):
        self.department_list = offices

        for o in self.department_list:
            self.department_dict[o['id']] = o

    def retrieve(self, officeid):
        return self.department_dict[officeid]

    def list(self):
        return self.department_list

    def page(self, limit, offset):
        return self.department_list[offset:offset + limit]

    @staticmethod
    def create_repository_from_file(file_name):
        with open(file_name) as f:
            department = json.load(f)
            return DepartmentRepository(department)


class EmployeeRepository:

    employee_list = []
    employee_dict = dict()

    def __init__(self, offices):
        self.employee_list = offices

        for o in self.employee_list:
            self.employee_dict[o['id']] = o

    def retrieve(self, officeid):
        return self.employee_dict[officeid]

    def list(self):
        return self.employee_list

    def page(self, limit, offset):
        return self.employee_list[offset:offset + limit]

    @staticmethod
    def create_repository_from_url(url):
        res = requests.get(url)
        if res.status_code == 200:
            employees = json.loads(res.content.decode())
            return EmployeeRepository(employees)


class LimitOffsetPaginator:
    def get_limit_offset(self):
        data = request.args
        limit = 10
        offset = 10
        if 'limit' in data:
            limit = int(data['limit'])
        if 'offset' in data:
            offset = int(data['limit'])
        return limit, offset

    def get_limit(self):
        data = request.args
        if 'limit' in data:
            return int(data['limit'])

    def get_offset(self):
        data = request.args
        if 'offset' in data:
            return int(data['limit'])


class Expander:

    repository_models = {}

    def __init__(self, repository_models):
        self.repository_models = repository_models

    def solve_expandables(self, elements):
        if request.args.getlist('expand'):
            result = []
            expand = request.args.getlist('expand')
            for q in elements:
                d = q.copy()
                for expandable in expand:
                    exp_list = expandable.split('.')
                    self.expand(q, exp_list, d)
                result.append(d)
            return result
        return elements

    def expand(self, model, expansion_list, d):
        if len(expansion_list) == 0:
            return
        else:
            expandable = expansion_list[0]
            expandable_relation = model[expandable]
            if expandable_relation is not None:
                manager = self.repository_models[expandable]
                new_model = manager.retrieve(expandable_relation)
                d[expandable] = new_model.copy()
                self.expand(new_model, expansion_list[1:], d[expandable])
        return
