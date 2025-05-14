import base64
from odoo import http, fields, _
from odoo.exceptions import ValidationError
from odoo.http import request
from datetime import date


class WarrantyPortal(http.Controller):
    @http.route('/warranty/check', type='http', auth='public', website=True, methods=['GET'])
    def warranty_check(self, **kwargs):
        data = []
        warranty_to_check = kwargs.get('warranty_id')
        if warranty_to_check and isinstance(warranty_to_check, str):
            res = request.env['sales.warranty'].sudo().search([('name', '=', warranty_to_check)], limit=1)
            if res:
                for x in res:
                    remaining_months = x.remaining_months if x.remaining_months else 0
                    data.append({
                        'name': x.name,
                        'status': x.state,
                        'date_of_purchase': x.date_of_purchase,
                        'warranty_end_date': x.warranty_end_date,
                        'remaining_months': f'{remaining_months} Months',
                        'remaining_months_numeric': int(remaining_months),
                    })
                print(data)
        return request.render('sales_warranty.WarrantyCheckTemplate', {'data': data})
