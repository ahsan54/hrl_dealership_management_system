import base64
from odoo import http, fields, _
from odoo.exceptions import ValidationError
from odoo.http import request
from datetime import date


class WarrantyPortal(http.Controller):
    @http.route('/warranty/check', type='http', auth='public', website=True, methods=['GET'])
    def warranty_check(self, **kwargs):
        remaining_value = 0
        data = []
        warranty_to_check = kwargs.get('warranty_id')
        if warranty_to_check and isinstance(warranty_to_check, str):
            res = request.env['sales.warranty'].sudo().search([('name', '=', warranty_to_check)], limit=1)
            if res:
                for x in res:
                    remaining_months = x.remaining_months if x.remaining_months else 0
                    # calculating remaining warranty a percetnage from 1 to 100 scale.
                    if x.warranty_end_date and x.date_of_purchase:
                        today_date = fields.Date.today()
                        total_duration = (x.warranty_end_date - x.date_of_purchase).days
                        remaining_duration = (x.warranty_end_date - today_date).days
                        if total_duration > 0:
                            remaining_value = max(1, min(100, (remaining_duration * 100) // total_duration))
                        else:
                            remaining_value = 100  # Default to 100 if duration is zero or negative

                    data.append({
                        'name': x.name,
                        'status': x.state,
                        'date_of_purchase': x.date_of_purchase,
                        'warranty_end_date': x.warranty_end_date,
                        'remaining_months': f'{remaining_months} Months',
                        'remaining_value': int(remaining_value),
                    })
                print(data)
            else:
                return """
                        <div style="text-align:center; margin-top:50px;">
                            <h2 style="color:#c00;">Warranty not found</h2>
                            <p>The requested tracking id <strong>{}</strong> does not exist or is invalid.</p>
                            <a href="/request/status" style="text-decoration:none; padding:10px 20px; background-color:#007bff; color:white; border-radius:5px;">
                                Go Back
                            </a>
                        </div>
                        """.format(warranty_to_check)
        return request.render('sales_warranty.WarrantyCheckTemplate', {'data': data})
