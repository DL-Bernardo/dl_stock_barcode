# -*- coding: utf-8 -*-
{
    'name': 'Stock Barcode Integration (Scanner de Inventário)',
    'version': '17.0.1.0.1',
    'summary': 'Gestão e leitura avançada de códigos de barras para picking, transferências e inventário',
    'description': """
        Módulo desenvolvido pela DIGITALUB para otimização de leitura de códigos de barras no Odoo 17 Community & Enterprise.
        - Interface moderna e veloz desenvolvida em OWL.
        - Leitura contínua rápida com incremento automático (+1 Qty).
        - Comandos de ação rápida por código de barras (Validar, Cancelar, Imprimir).
        - Alertas sonoros com feedback instantâneo (Beep/Buzzer).
        - Nomenclaturas personalizadas e busca inteligente de transferências.
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