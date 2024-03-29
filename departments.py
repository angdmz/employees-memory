from flask import request
from flask_restful import abort

from services import KwargsAssigner


class SingleDepartment(KwargsAssigner):
    def get(self, department_id):
        return self.repository.retrieve(department_id)


class DepartmentList(KwargsAssigner):
    def get(self):
        try:
            page = self.repository.page(int(request.args.get('limit', self.default_limit)),int(request.args.get('offset', self.default_offset)))
            return self.expander.solve_expandables(page, request.args.getlist('expand'))
        except KeyError as ke:
            abort(412, message="{} is not a valid key to expand".format(str(ke)))