import base64
from odoo import http, fields, _
from odoo.exceptions import ValidationError
from odoo.http import request
from datetime import date


class PortalBase(http.Controller):

    @http.route('/portal/base', type='http', auth='user', website=True)
    def Create_Dealership_Request(self, **post):
        available_country = []
        country_ids = request.env['res.country'].search([])
        for x in country_ids:
            available_country.append({'id': x.id, 'name': x.name})

        if post:
            image_file = request.httprequest.files.get('image_1920')
            image_base64 = False

            if image_file:
                image_base64 = base64.b64encode(image_file.read())

            get_first_name = post.get('first_name')
            get_last_name = post.get('last_name')
            get_email = post.get('email_id')

            get_date_of_birth = fields.Date.from_string(post.get('date_of_birth'))
            if get_date_of_birth and get_date_of_birth >= date.today():
                raise ValidationError("Date of Birth must be in the past.")

            get_date_from = fields.Date.from_string(post.get('date_from')) if post.get('date_from') else False
            get_date_to = fields.Date.from_string(post.get('date_to')) if post.get('date_to') else False

            if not get_first_name or not get_last_name or not get_email:
                raise ValidationError("First Name, Last Name, and Email are required.")

            # Handle file uploads and create ir.attachment records
            def create_attachments(field_name):
                attachments = []
                if field_name in request.httprequest.files:
                    files = request.httprequest.files.getlist(field_name)
                    for file in files:
                        if file and file.filename:
                            attachment = request.env['ir.attachment'].sudo().create({
                                'name': file.filename,
                                'datas': base64.b64encode(file.read()),
                                'res_model': 'dms.portal',
                                'res_field': field_name,
                                'type': 'binary',
                            })
                            attachments.append(attachment.id)
                return [(6, 0, attachments)] if attachments else False

            dealership_request_id = request.env['dms.portal'].sudo().create({
                # 1st page
                'image_1920': image_base64,
                'first_name': get_first_name,
                'last_name': get_last_name,
                'email_id': get_email,
                'date_of_birth': get_date_of_birth,
                'phone_no': post.get('phone_no'),
                'mobile_no': post.get('mobile_no'),
                'location': post.get('location'),
                'location2': post.get('second_location'),
                'city': post.get('city'),
                'pincode': post.get('pincode'),
                'country_id': int(post.get('country')) if post.get('country') else False,
                'province': post.get('province'),
                'qualification': post.get('qualification'),
                'current_occupation': post.get('current_occupation'),
                'dealer_vacancy_known_through': post.get('dealer_vacancy_known_through'),
                'advertisement_boolean': post.get('advertisement_boolean'),
                'code': post.get('code'),
                # 2nd Page
                'not_available_site_location': post.get('not_available_site_location'),
                'available_site_location': post.get('available_site_location'),
                'total_area': float(post.get('total_area') or 0),
                'query': post.get('query'),
                'investment_from': float(post.get('investment_from') or 0),
                'investment_to': float(post.get('investment_to') or 0),
                # 3rd page
                'company_name': post.get('company_name'),
                'business_type': post.get('business_type'),
                'contact_person_name': post.get('contact_person_name'),
                'business_email': post.get('business_email'),
                'business_phone': post.get('business_phone'),
                'business_address': post.get('business_address'),
                'existing_dealership': bool(post.get('existing_dealership')),
                'infrastructure_detail': post.get('infrastructure_detail'),
                'business_staff_count': float(post.get('business_staff_count') or 0),
                'licence_upload': create_attachments('licence_upload'),
                'registration_upload': create_attachments('registration_upload'),
                'ownership_proof': create_attachments('ownership_proof'),
                'tax_legal_registration': bool(post.get('tax_legal_registration')),
                'tax_ntn_number': post.get('tax_ntn_number'),
                'tax_cnic': post.get('tax_cnic'),
                'secp_certificate_number': create_attachments('secp_certificate_number'),
            })

            return request.render('DMS_Portal.form_submission_success', {
                'record_id': dealership_request_id.reference_no
            })

        return request.render('DMS_Portal.dealer_ship_request_creation_form', {
            'available_country': available_country,
        })


class CustomerPortal(http.Controller):
    @http.route('/request/status', type='http', auth='public', website=True, methods=['GET'])
    def Retrive_Customer_Data(self, *args, **kwargs):
        Data = []
        application_id = kwargs.get('application_id')

        if application_id and str(application_id).isdigit():
            Obj = request.env['dms.portal'].search([('reference_no', '=', application_id)])
            if Obj:
                for rec in Obj:
                    Data.append({
                        'id': rec.id,
                        'first_name': rec.first_name,
                        'last_name': rec.last_name,
                        'email_id': rec.email_id,
                        'date_of_birth': rec.date_of_birth,
                        'phone_no': rec.phone_no,
                        'mobile_no': rec.mobile_no,
                        'location': rec.location,
                        'location2': rec.location2,
                        'city': rec.city,
                        'pincode': rec.pincode,
                        'country_id': rec.country_id.name if rec.country_id else '',
                        'province': rec.province,
                        'qualification': rec.qualification,
                        'current_occupation': rec.current_occupation,
                        'dealer_vacancy_known_through': rec.dealer_vacancy_known_through,
                        'code': rec.code,
                        'advertisement_boolean': rec.advertisement_boolean,
                        'image_1920': rec.image_1920,
                        'company_name': rec.company_name,
                        'business_type': rec.business_type,
                        'contact_person_name': rec.contact_person_name,
                        'business_email': rec.business_email,
                        'business_phone': rec.business_phone,
                        'business_address': rec.business_address,
                        'existing_dealership': rec.existing_dealership,
                        'infrastructure_detail': rec.infrastructure_detail,
                        'business_staff_count': rec.business_staff_count,
                        'state': rec.state,
                    })
                    print(f'Data: {Data}')
            else:
                return """
                        <div style="text-align:center; margin-top:50px;">
                            <h2 style="color:#c00;">Application not found</h2>
                            <p>The requested application <strong>{}</strong> does not exist or is invalid.</p>
                            <a href="/request/status" style="text-decoration:none; padding:10px 20px; background-color:#007bff; color:white; border-radius:5px;">
                                Go Back
                            </a>
                        </div>
                        """.format(application_id)

        return request.render('DMS_Portal.dms_portal_request_status', {'data': Data})
