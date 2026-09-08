# -*- coding: utf-8 -*-
{
    'name': 'Stock Barcode Scanner & Picking Automation',
    'version': '17.0.1.0.2',
    'summary': 'Fast barcode scanning, picking automation, inventory transfers & physical counting with acoustic feedback',
    'description': """
        Professional Barcode Scanner & Picking Management for Odoo 17 Community & Enterprise.
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

    # Preço atualizado
    'price': 60.00,
    'currency': 'EUR',
    
    # Dependências do módulo
    'depends': [
        'base',
        'stock',
        'barcodes',
    ],

    # Ficheiros XML carregados no arranque
    'data': [
        'data/barcode_nomenclature_data.xml',
        'views/barcode_menu_views.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'dl_stock_barcode/static/src/css/barcode_styles.css',
            'dl_stock_barcode/static/src/js/barcode_picking_model.js',
        ],
        'web.assets_qweb': [
            'dl_stock_barcode/static/src/xml/barcode_templates.xml',
        ],
    },

    'images': [
        'static/description/banner.png',
        'static/description/main_screenshot.png'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
