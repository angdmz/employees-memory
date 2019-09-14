from flask import request
from services import KwargsAssigner


class SingleOffice(KwargsAssigner):
    def get(self, office_id):
        return self.repository.retrieve(office_id)

class OfficesList(KwargsAssigner):
    def get(self):
        page = self.repository.page(int(request.args.get('limit', 10)),int(request.args.get('offset', 0)))
        return self.expander.solve_expandables(page, request.args.getlist('expand'))
