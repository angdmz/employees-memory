from flask import request
from services import KwargsAssigner


class SingleDepartment(KwargsAssigner):
    def get(self, department_id):
        return self.repository.retrieve(department_id)


class DepartmentList(KwargsAssigner):
    def get(self):
        page = self.repository.page(int(request.args.get('limit', 10)),int(request.args.get('offset', 0)))
        return self.expander.solve_expandables(page, request.args.getlist('expand'))
