# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def dl_process_barcode(self, barcode, picking_id=False, location_id=False):
        """
        Método chamado pelo Frontend (JS/OWL) sempre que um código de barras é lido.
        Retorna um dicionário (JSON) instruindo o Frontend sobre o que atualizar no ecrã.
        """
        # 1. VERIFICAR SE É UM TIPO DE OPERAÇÃO
        picking_type = self.env['stock.picking.type'].search([('barcode', '=', barcode)], limit=1)
        if not picking_type and '-' in barcode:
            picking_type = self.env['stock.picking.type'].search([('barcode', '=', barcode.replace('-', '/'))], limit=1)

        if picking_type:
            new_picking = self.create({
                'picking_type_id': picking_type.id,
                'location_id': picking_type.default_location_src_id.id,
                'location_dest_id': picking_type.default_location_dest_id.id,
            })
            return {
                'action': 'new_picking',
                'picking_id': new_picking.id,
                'message': f'Nova {picking_type.name} iniciada ({new_picking.name})'
            }

        # 2. VERIFICAR SE É UMA TRANSFERÊNCIA EXISTENTE
        picking = self.search([('name', '=', barcode)], limit=1)
        if not picking and '-' in barcode:
            picking = self.search([('name', '=', barcode.replace('-', '/'))], limit=1)

        if not picking:
            res = self.name_search(name=barcode, operator='ilike', limit=1)
            if res:
                picking = self.browse(res[0][0])
        if picking:
            lines_data = []
            for ml in picking.move_line_ids:
                qty_val = getattr(ml, 'quantity', getattr(ml, 'qty_done', 0.0))
                lines_data.append({
                    'product_id': f"{ml.product_id.id}_{ml.lot_id.id if ml.lot_id else 'False'}",
                    'name': ml.product_id.name + (f" (Lote: {ml.lot_id.name})" if ml.lot_id else ""),
                    'qty': qty_val,
                })
            grouped_lines = {}
            for line in lines_data:
                pid = line['product_id']
                if pid in grouped_lines:
                    grouped_lines[pid]['qty'] += line['qty']
                else:
                    grouped_lines[pid] = line
            return {
                'action': 'open_picking',
                'picking_id': picking.id,
                'message': f'Documento {picking.name} encontrado.',
                'lines': list(grouped_lines.values())
            }

        # 3. VERIFICAR SE É LOCALIZAÇÃO
        location = self.env['stock.location'].search([('barcode', '=', barcode)], limit=1)
        if not location and '-' in barcode:
            location = self.env['stock.location'].search([('barcode', '=', barcode.replace('-', '/'))], limit=1)

        if location:
            quants = self.env['stock.quant'].search([('location_id', '=', location.id)])
            lines_data = []
            for q in quants:
                name = q.product_id.name + (f" (Lote: {q.lot_id.name})" if q.lot_id else "")
                qty = q.inventory_quantity if getattr(q, 'inventory_quantity_set', False) else q.quantity
                if qty > 0:
                    lines_data.append({
                        'product_id': f"{q.product_id.id}_{q.lot_id.id if q.lot_id else 'False'}",
                        'name': name,
                        'qty': qty
                    })
            return {
                'action': 'set_location',
                'location_id': location.id,
                'message': f'Inventário no Local: {location.name}',
                'lines': lines_data
            }

        # 4. VERIFICAR COMANDOS DE AÇÃO
        if picking_id:
            picking_record = self.browse(picking_id)
            if barcode == 'O-CMD-VALIDATE':
                picking_record.button_validate()
                return {'action': 'validated', 'message': 'Operação Validada com Sucesso!'}
            if barcode == 'O-CMD-CANCEL':
                picking_record.action_cancel()
                return {'action': 'cancelled', 'message': 'Operação Cancelada.'}
            if barcode == 'O-CMD-PRINT':
                report = self.env.ref('stock.action_report_delivery', raise_if_not_found=False)
                if report:
                    return {'action': 'print_report', 'message': 'Impressão Iniciada...'}

        if location_id and barcode == 'O-CMD-VALIDATE':
            quants = self.env['stock.quant'].search([('location_id', '=', location_id), ('inventory_quantity_set', '=', True)])
            quants.action_apply_inventory()
            return {'action': 'validated', 'message': 'Inventário Aplicado!'}

        # 5. VERIFICAR SE É UM PRODUTO OU LOTE PARA ADICIONAR QUANTIDADE
        if picking_id or location_id:
            lot_model = 'stock.lot' if 'stock.lot' in self.env else 'stock.production.lot'
            lot = self.env[lot_model].search([('name', '=', barcode)], limit=1)
            product = lot.product_id if lot else self.env['product.product'].search([('barcode', '=', barcode)], limit=1)

            if product:
                if picking_id:
                    self._dl_add_product_line(self.browse(picking_id), product, lot)
                elif location_id:
                    self._dl_add_quant(location_id, product, lot)

                pname = product.name + (f" (Lote: {lot.name})" if lot else "")
                return {
                    'action': 'product_added',
                    'product_id': f"{product.id}_{lot.id if lot else 'False'}",
                    'product_name': pname,
                    'message': f'{pname} adicionado (+1)'
                }

        return {
            'action': 'error',
            'message': f'Código de barras "{barcode}" não reconhecido ou inválido neste contexto.'
        }

    def _dl_add_product_line(self, picking, product, lot=None, qty=1):
        """Incrementa a quantidade da linha do produto ou cria uma nova se não existir"""
        domain = lambda l: l.product_id.id == product.id and (l.lot_id.id == lot.id if lot else not l.lot_id)
        move_line = picking.move_line_ids.filtered(domain)
        sml_fields = self.env['stock.move.line']._fields

        if move_line:
            if 'quantity' in sml_fields:
                move_line[0].quantity += qty
            else:
                move_line[0].qty_done += qty
        else:
            moves = getattr(picking, 'move_ids', getattr(picking, 'move_ids_without_package', self.env['stock.move']))
            move = moves.filtered(lambda m: m.product_id.id == product.id)
            vals = {
                'picking_id': picking.id,
                'move_id': move[0].id if move else False,
                'product_id': product.id,
                'location_id': picking.location_id.id,
                'location_dest_id': picking.location_dest_id.id,
                'lot_id': lot.id if lot else False,
            }
            if 'product_uom_id' in sml_fields:
                vals['product_uom_id'] = product.uom_id.id
            if 'quantity' in sml_fields:
                vals['quantity'] = qty
            else:
                vals['qty_done'] = qty
            self.env['stock.move.line'].create(vals)

    def _dl_add_quant(self, location_id, product, lot=None):
        """Incrementa a quantidade contada no inventário (stock.quant)"""
        quant = self.env['stock.quant'].search([
            ('location_id', '=', location_id),
            ('product_id', '=', product.id),
            ('lot_id', '=', lot.id if lot else False)
        ], limit=1)

        if quant:
            if not getattr(quant, 'inventory_quantity_set', False):
                quant.inventory_quantity = quant.quantity + 1
            else:
                quant.inventory_quantity += 1
        else:
            self.env['stock.quant'].create({
                'location_id': location_id,
                'product_id': product.id,
                'lot_id': lot.id if lot else False,
                'inventory_quantity': 1,
            })
