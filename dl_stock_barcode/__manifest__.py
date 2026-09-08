# -*- coding: utf-8 -*-
{
    'name': 'Mobile Stock Barcode Scanner for Community',
    'version': '16.0.1.0.2',
    'summary': 'Zero Hardware Lock-in Mobile Barcode Scanning, Real-time Inventory & Fast Picking Automation',
        'description': """
        Professional Barcode Scanner & Picking Management for Odoo Community & Enterprise.
        - High-speed reactive OWL scanning console.
        - Real-time continuous scanning with automatic quantity increment (+1 Qty).
        - Hands-free Action Command Barcodes (Validate, Cancel, Print).
        - Acoustic audio feedback with distinct success/warning sound frequencies.
        - Custom barcode nomenclature support and instant transfer lookup.
        - 100% Community & Odoo.sh ready with zero server dependencies.
    """,
    'author': 'DIGITALUB ANGOLA, LDA',
    'website': 'https://www.digitalub.ao',
    'category': 'Inventory/Inventory',
    'license': 'OPL-1',

    # Preço atualizado
    'price': 45.0,
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

    # CORREÇÃO AQUI: Apontar para o ficheiro de imagem correto que está no seu servidor
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
