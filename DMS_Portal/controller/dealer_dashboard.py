import base64
from datetime import timedelta, date

from odoo import http, fields
from odoo.http import request


class DealerDashBoard(http.Controller):
    @http.route('/dealer/dashboard', type='http', auth="user", website=True, methods=['GET'])
    def dealer_dashboard(self, **kwargs):
        dealership_applications = []
        approved_applications = []
        pending_applications = []
        all_dealers = []
        request_type = kwargs.get('request_type', 'dealer_applications')
        selected_month = None

        if kwargs.get('require_month') and kwargs.get('require_month') != 'Select Month':
            require_date = fields.Date.from_string(kwargs.get('require_month'))
            selected_month = require_date.strftime("%B %Y")
            month_start = date(require_date.year, require_date.month, 1)
            month_end = date(require_date.year, require_date.month + 1, 1) - timedelta(
                days=1) if require_date.month < 12 else date(require_date.year + 1, 1, 1) - timedelta(days=1)

            if request_type == 'dealer_applications':
                dealer_recs = request.env['dms.portal'].search(
                    [('request_month', '>=', month_start), ('request_month', '<=', month_end),
                     ('state', 'in', ['draft'])])
                for x in dealer_recs:
                    dealer_image = x.image_1920
                    if dealer_image and isinstance(dealer_image, bytes):
                        dealer_image = dealer_image.decode('utf-8')
                    elif not dealer_image:
                        dealer_image = None
                    dealership_applications.append({
                        'Application_ID': x.id,
                        'Applicant_Name': f"{x.first_name} {x.last_name}",
                        'Country': x.country_id.name,
                        'Image': dealer_image,
                        'company_name': x.company_name,
                        'business_type': x.business_type,
                    })

            if request_type == 'approve_applications':
                approved_recs = request.env['dms.portal'].search([
                    ('approved_month', '>=', month_start),
                    ('approved_month', '<=', month_end),
                    ('state', '=', 'approved')
                ])
                for x in approved_recs:
                    dealer_image = x.image_1920
                    if dealer_image and isinstance(dealer_image, bytes):
                        dealer_image = dealer_image.decode('utf-8')
                    elif not dealer_image:
                        dealer_image = None
                    approved_applications.append({
                        'Application_ID': x.id,
                        'Applicant_Name': f"{x.first_name} {x.last_name}",
                        'Country': x.country_id.name,
                        'Image': dealer_image,
                        'company_name': x.company_name,
                        'business_type': x.business_type,
                    })

            if request_type == 'waiting_applications':
                pending_recs = request.env['dms.portal'].search([
                    ('approved_month', '>=', month_start),
                    ('approved_month', '<=', month_end),
                    ('state', '=', 'under_review')
                ])
                for x in pending_recs:
                    dealer_image = x.image_1920
                    if dealer_image and isinstance(dealer_image, bytes):
                        dealer_image = dealer_image.decode('utf-8')
                    elif not dealer_image:
                        dealer_image = None
                    pending_applications.append({
                        'Application_ID': x.id,
                        'Applicant_Name': f"{x.first_name} {x.last_name}",
                        'Country': x.country_id.name,
                        'Image': dealer_image,
                        'company_name': x.company_name,
                        'business_type': x.business_type,
                    })

            if request_type == 'all_dealer_applications':
                all_dealer_recs = request.env['dms.portal'].search([('state', '=', 'approved')])
                for x in all_dealer_recs:
                    dealer_image = x.image_1920
                    if dealer_image and isinstance(dealer_image, bytes):
                        dealer_image = dealer_image.decode('utf-8')
                    elif not dealer_image:
                        dealer_image = None
                    all_dealers.append({
                        'Application_ID': x.id,
                        'Applicant_Name': f"{x.first_name} {x.last_name}",
                        'Country': x.country_id.name,
                        'Image': dealer_image,
                        'company_name': x.company_name,
                        'business_type': x.business_type,
                    })

        return request.render('DMS_Portal.dealer_ship_admin_dashboard', {
            'dealership_applications': dealership_applications or [],
            'approved_applications': approved_applications or [],
            'pending_applications': pending_applications or [],
            'all_dealers': all_dealers or [],
            'request_type': request_type,
            'selected_month': selected_month,
            'kwargs': kwargs,
        })
