# -*- coding: utf-8 -*-
{
    'name': 'Stock Barcode Integration',
    'version': '17.0.1.0.0',
    'summary': 'Gestão e leitura avançada de códigos de barras para picking e stock',
    'description': """
        Módulo desenvolvido pela DIGITALUB para otimização de leitura de códigos de barras no Odoo 17.
        - Suporte a nomenclaturas personalizadas.
        - Interface otimizada para picking.
        - Estilos e templates customizados.
    """,
    'author': 'DIGITALUB ANGOLA, LDA',
    'website': 'https://www.digitalub.ao',
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

    # CORREÇÃO AQUI: Apontar para o ficheiro de imagem correto que está no seu servidor
    'images': [
        'static/description/main_screenshot.png'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}