{
    'name': 'DL Stock Barcode',
    'version': '1.0',
    'category': 'Inventory/Inventory',
    'summary': 'Operações de Armazém e Inventário via Código de Barras (OWL)',
    'description': """
        Este módulo adiciona uma interface dedicada para leitura de códigos de barras,
        permitindo:
        - Pesquisa rápida de transferências.
        - Leitura de produtos para adicionar quantidades (+1 por scan).
        - Comandos de ação via código de barras (Ex: Validar, Cancelar).
        - Feedback sonoro (Sucesso/Erro).
    """,
    'author': 'Digitalub Angola',
    'depends': ['stock', 'barcodes', 'web'],
    'data':[
        'data/barcode_nomenclature_data.xml',
        'views/barcode_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend':[
            # Aqui carregaremos o nosso Frontend em OWL
            'dl_stock_barcode/static/src/css/barcode_styles.css',
            'dl_stock_barcode/static/src/js/barcode_picking_model.js',
            'dl_stock_barcode/static/src/xml/barcode_templates.xml',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}