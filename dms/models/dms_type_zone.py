from odoo import api, fields, models, _


class DmsType(models.Model):
    _name = 'dms.type'

    name = fields.Char('Type Name', required=True)
    dealer_type = fields.Selection(
        [('sale_only', 'Sale Only'), ('service_only', 'Service Only'), ('spare_parts_only', 'Spare Parts Only'),
         ('sale_service', 'Sales & Service'), ('full_service', 'Full Service Dealer')],
        default='', string='Dealer Type')


class DmsZone(models.Model):
    _name = 'dms.zone'
    _rec_name = 'dealer_zone'

    dealer_record = fields.Many2one('dms.base', string='Dealer Record')

    dealer_zone = fields.Selection([('zone_a', 'Zone A'), ('zone_b', 'Zone B'), ('urban', 'Urban'), ('rural', 'Rural')],
                                   'Zone', required=True)




