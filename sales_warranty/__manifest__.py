{
    'name': 'sales_warranty',  # Module name
    'author': 'M.Ahsan',  # Author name
    'maintainer': 'M.Rizwan',
    'category': 'BSS',  # Category displayed in info
    'website': 'https://www.bssuniversal.com',  # Website displayed in info
    'depends': ['base', 'sale', 'stock','website','portal'],  # Dependencies
    'installable': True,
    'application': True,
    "license": "LGPL-3",
    'data': [
        'security/ir.model.access.csv',
        'reports/sales_warranty_report.xml',
        'wizard/sales_warranty_wizard.xml',
        'views/menu_items.xml',
        'views/sales_warranty.xml',
        'views/sale_order_line_inherit.xml',
        'views/product_template_inherit.xml',
        'views/sale_warranty_portal.xml',

    ],
    'images': ['static/description/icon.png'],

}
