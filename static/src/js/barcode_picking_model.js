/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onMounted, onWillUnmount } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class BarcodeScannerAction extends Component {
    static template = "dl_stock_barcode.ScannerTemplate";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        
        this.state = useState({
            picking_id: false,
            location_id: false,
            picking_name: "Nenhuma operação iniciada",
            message: "Pronto para escanear...",
            messageType: "info",
            lines:[]
        });

        this.barcodeBuffer = "";
        this.barcodeTimeout = null;
        this.audioCtx = null;

        onMounted(() => {
            this.onKeydownBound = this.onKeydown.bind(this);
            window.addEventListener("keydown", this.onKeydownBound);
        });
        
        onWillUnmount(() => {
            window.removeEventListener("keydown", this.onKeydownBound);
        });
    }

    initAudioCtx() {
        if (!this.audioCtx) {
            this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        if (this.audioCtx.state === 'suspended') {
            this.audioCtx.resume();
        }
    }

    onKeydown(ev) {
        if (ev.target.tagName === "INPUT" || ev.target.tagName === "TEXTAREA") return;
        
        this.initAudioCtx();

        if (ev.key === "Enter") {
            if (this.barcodeBuffer.length > 2) {
                this.processBarcode(this.barcodeBuffer);
            }
            this.barcodeBuffer = "";
            clearTimeout(this.barcodeTimeout);
            return;
        }
        
        if (ev.key.length === 1) {
            this.barcodeBuffer += ev.key;
        }

        clearTimeout(this.barcodeTimeout);
        this.barcodeTimeout = setTimeout(() => {
            this.barcodeBuffer = "";
        }, 500); 
    }

    async processBarcode(barcode) {
        try {
            const result = await this.orm.call(
                "stock.picking",
                "dl_process_barcode",[barcode, this.state.picking_id, this.state.location_id]
            );
            this.handleResult(result);
        } catch (error) {
            this.playSound("error");
            let errorMsg = "Erro de conexão com o servidor.";
            if (error && error.data && error.data.message) {
                errorMsg = error.data.message;
            }
            this.showFeedback(errorMsg, "error");
        }
    }

    handleResult(result) {
        if (result.action === 'error') {
            this.playSound("error");
            this.showFeedback(result.message, "error");
        } else {
            this.playSound("success");
            this.showFeedback(result.message, "success");
            
            if (result.action === 'open_picking' || result.action === 'new_picking') {
                this.state.picking_id = result.picking_id || result.picking_type_id;
                this.state.location_id = false;
                this.state.picking_name = result.message;
                this.state.lines = result.lines || []; // Carrega as linhas existentes ou zera
            } 
            else if (result.action === 'set_location') {
                this.state.picking_id = false;
                this.state.location_id = result.location_id;
                this.state.picking_name = result.message;
                this.state.lines = result.lines || [];
            }
            else if (result.action === 'print_report') {
                this.action.doAction({
                    type: "ir.actions.report",
                    report_name: "stock.report_deliveryslip",
                    report_type: "qweb-pdf",
                    context: { active_ids: [this.state.picking_id] }
                });
            }
            else if (result.action === 'product_added') {
                let existingLine = this.state.lines.find(l => l.product_id === result.product_id);
                if (existingLine) {
                    existingLine.qty += 1;
                } else {
                    this.state.lines.push({
                        product_id: result.product_id,
                        name: result.product_name,
                        qty: 1
                    });
                }
            } 
            else if (result.action === 'validated' || result.action === 'cancelled') {
                this.state.picking_id = false;
                this.state.location_id = false;
                this.state.picking_name = "Nenhuma operação iniciada";
                this.state.lines =[]; // Zera a lista
            }
        }
    }

    // Função para mostrar a mensagem e escondê-la após 3 segundos
    showFeedback(message, type) {
        this.state.message = message;
        this.state.messageType = type;
        
        setTimeout(() => {
            if (this.state.message === message) {
                this.state.message = "Pronto para escanear...";
                this.state.messageType = "info";
            }
        }, 3000);
    }

    // Função que gera som sem precisar de arquivos MP3 (API nativa do navegador)
    playSound(type) {
        if (!this.audioCtx) return;
        
        const ctx = this.audioCtx;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        
        osc.connect(gain);
        gain.connect(ctx.destination);
        
        if (type === "success") {
            osc.frequency.value = 800; // Som agudo (Beep)
            osc.type = "sine";
            gain.gain.setValueAtTime(0.1, ctx.currentTime);
            osc.start();
            osc.stop(ctx.currentTime + 0.15);
        } else {
            osc.frequency.value = 150; // Som grave e distorcido (Erro)
            osc.type = "sawtooth";
            gain.gain.setValueAtTime(0.2, ctx.currentTime);
            osc.start();
            osc.stop(ctx.currentTime + 0.4);
        }
    }

    // Clique manual nos botões do ecrã
    onCommandBtn(command, ev) {
        // Remove foco do botão para evitar que leituras futuras (que enviam Enter) 
        // disparem este botão indevidamente.
        if (ev && ev.target) {
            ev.target.blur();
        }
        this.processBarcode(command);
    }
}

// Regista a ação do cliente no Odoo para o XML conseguir abri-la
registry.category("actions").add("dl_stock_barcode_action", BarcodeScannerAction);