from flask import request
from flask_restful import abort

from services import KwargsAssigner


class SingleEmployee(KwargsAssigner):
    def get(self, employee_list):
        return self.repository.retrieve(employee_list)


class EmployeeList(KwargsAssigner):
    def get(self):
        try:
            page = self.repository.page(int(request.args.get('limit', self.default_limit)),int(request.args.get('offset', self.default_offset)))
            return self.expander.solve_expandables(page, request.args.getlist('expand'))
        except KeyError as ke:
            abort(412, message="{} is not a valid key to expand".format(str(ke)))