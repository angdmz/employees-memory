from flask import request
from services import KwargsAssigner


class SingleEmployee(KwargsAssigner):
    def get(self, employee_list):
        return self.repository.retrieve(employee_list)


class EmployeeList(KwargsAssigner):
    def get(self):
        page = self.repository.page(int(request.args.get('limit', 10)),int(request.args.get('offset', 0)))
        return self.expander.solve_expandables(page, request.args.getlist('expand'))
