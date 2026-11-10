# -*- coding: utf-8 -*-
{
    'name': 'Mobile Stock Barcode Scanner for Community',
    'version': '20.0.1.0.9',
    'summary': 'Zero Hardware Lock-in Mobile Barcode Scanning, Real-time Inventory & Fast Picking Automation',
    'description': """
        Professional Barcode Scanner & Picking Management for Odoo 15, 16, 17, 18, 19 & 20 (Community & Enterprise).
        - High-speed reactive OWL scanning console.
        - Real-time continuous scanning with automatic quantity increment (+1 Qty).
        - Hands-free Action Command Barcodes (Validate, Cancel, Print).
        - Acoustic audio feedback with distinct success/warning sound frequencies.
        - Custom barcode nomenclature support and instant transfer lookup.
        - 100% Community & Odoo.sh ready with zero server dependencies.
    """,
    'author': 'DIGITALUB ANGOLA, LDA',
    'website': 'https://www.digitalub.ao',
    'support': 'suporte@digitalub.ao',
    'category': 'Inventory/Inventory',
    'license': 'OPL-1',
    'price': 49.0,
    'currency': 'USD',
    'depends': [
        'base',
        'stock',
        'barcodes',
    ],
    'data': [
        'data/barcode_nomenclature_data.xml',
        'views/barcode_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'dl_stock_barcode/static/src/css/barcode_styles.css',
            'dl_stock_barcode/static/src/js/barcode_picking_model.js',
            'dl_stock_barcode/static/src/xml/barcode_templates.xml',
        ],
    },
    'images': [
        'static/description/banner.png',
        'static/description/step1_barcode_config.png',
        'static/description/step2_barcode_scan.png',
        'static/description/step3_barcode_validate.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
