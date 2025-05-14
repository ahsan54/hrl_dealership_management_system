from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.tools.safe_eval import datetime


class SalesWarranty(models.Model):
    _name = 'sales.warranty'

    name = fields.Char('Name', readonly=True, default=lambda self: _('New'))
    sale_order_id = fields.Many2one('sale.order', 'Sales Order')
    active = fields.Boolean('Active', default=True)

    state = fields.Selection([('in_warranty', 'In Warranty'), ('expired', 'Expired')], string='State', readonly=True,
                             default='in_warranty')

    customer_id = fields.Many2one('res.partner', 'Customer')
    product_id = fields.Many2one('product.template', 'Order Product')
    date_of_purchase = fields.Date('Date of Purchase')
    warranty_end_date = fields.Date('Warrenty End Date')
    warranty_period = fields.Float('Warranty Period')
    notes = fields.Text('Notes', readonly=True)
    sale_order_count = fields.Integer('Sales Order Count', compute='_compute_sale_order_count')
    remaining_months = fields.Integer('Remaining Months', compute='_compute_remaining_months')

    terms_condition_id = fields.Many2one('warranty.terms', 'Terms & Conditions')
    warranty_include_id = fields.Many2one('warranty.includes', 'Warranty Includes')
    warranty_exclude_id = fields.Many2one('warranty.excludes', 'Warranty Excludes')

    @api.depends('warranty_end_date')
    def _compute_remaining_months(self):
        today = fields.Date.today()
        for record in self:
            if record.warranty_end_date and record.warranty_end_date > today:
                delta = relativedelta(record.warranty_end_date, today)
                record.remaining_months = (delta.years * 12) + delta.months
            else:
                record.remaining_months = 0

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sales.warranty.sequence') or _('New')
        return super(SalesWarranty, self).create(vals)

    def force_expire(self):
        self.write({'state': 'expired', 'active': False})

    def action_view_related_sale_order(self):
        return {
            'name': 'Related Sale Orders',
            'res_model': 'sale.order',
            'view_mode': 'list,form',
            'domain': [('sale_warranty_id', '=', self.id)],
            'context': {'create': False, 'delete': False},
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

    @api.depends('sale_order_id')
    def _compute_sale_order_count(self):
        for x in self:
            if x.sale_order_id:
                x.sale_order_count = len(x.sale_order_id)

    def cron_job_change_warranty(self):
        today_date = fields.Date.today()
        warranties_to_expire = self.env['sales.warranty'].search([
            ('state', '=', 'in_warranty'),
            ('warranty_end_date', '!=', False),
            ('warranty_end_date', '<=', today_date),
        ])
        print(f"Found {len(warranties_to_expire)} warranties to expire on {today_date}")
        for record in warranties_to_expire:
            print(f"Processing warranty {record.name}: End Date {record.warranty_end_date}")
            record.write({
                'state': 'expired',
                'active': False,
            })
            print(f"Updated warranty {record.name} to expired")


class WarrantyTerms(models.Model):
    _name = 'warranty.terms'
    _rec_name = 'terms_conditions'


    terms_conditions = fields.Text('Terms & Conditions', sanitize=True, tracking=True,
                                   default=lambda self: self._get_default_terms_conditions())

    @api.model
    def _get_default_terms_conditions(self):
        return """
                Add here warranty terms and conditions.
               """


class WarrantyIncludes(models.Model):
    _name = 'warranty.includes'
    _rec_name = 'warranty_includes'


    warranty_includes = fields.Text('Warranty Includes', sanitize=True, tracking=True,
                                    default=lambda self: self._get_default_warranty_includes())

    @api.model
    def _get_default_warranty_includes(self):
        return """
                     Add here warranty inclusions.
                   """


class WarrantyExcludes(models.Model):
    _name = 'warranty.excludes'
    _rec_name = 'warranty_excludes'

    warranty_excludes = fields.Text('Warranty Excludes', sanitize=True, tracking=True,
                                    default=lambda self: self._get_default_warranty_excludes())

    @api.model
    def _get_default_warranty_excludes(self):
        return """
                     Add here warranty exclusions.
                   """
