# DL Stock Barcode (Scanner de Inventário)

Este módulo introduz uma interface dedicada e otimizada para a leitura de códigos de barras nas operações de armazém no Odoo 17 Community Edition.

## 🌟 Funcionalidades Principais
* **Interface Otimizada (OWL):** Tela limpa projetada para tablets e telemóveis, facilitando o trabalho do operador de armazém.
* **Leitura Rápida:** Adicione produtos e incremente quantidades (+1) rapidamente com qualquer leitor de código de barras USB/Bluetooth.
* **Comandos de Ação:** Valide ou cancele documentos sem tocar no rato/teclado, usando códigos de barras de comando (`O-CMD-VALIDATE`).
* **Feedback Sonoro:** O navegador emite sons dinâmicos nativos (Beep para sucesso, Buzzer para erro).
* **Pesquisa Inteligente:** Faça scan do número da guia (ex: `WH/IN/0001`) para abrir a transferência automaticamente.

## ⚙️ Instalação
1. Coloque a pasta `dl_stock_barcode` no diretório de `addons` do seu Odoo 17.
2. Reinicie o serviço do Odoo.
3. Ative o "Modo de Desenvolvedor" (Developer Mode).
4. Vá a Aplicações > Atualizar Lista de Aplicações.
5. Procure por "DL Stock Barcode" e instale.

## 🚀 Como Usar (Regra de Ouro)
Para garantir o bom funcionamento do leitor, a sua janela deve estar sempre ativa. Siga estes passos práticos para o armazém:
1. Aceda ao módulo **Gest. de Stock**. No menu principal, clique em **Barcode Scanner**.
2. Dê um **clique na zona cinzenta/branca do ecrã** (para garantir que a janela não perdeu o "foco").
3. Aponte o leitor para o número do documento/guia primeiro (ex: `WH/IN/0001`). O sistema abrirá o documento.
4. De seguida, leia os seus **Produtos**. A quantidade vai subindo automaticamente e aparecerá uma mensagem a verde. *(Nota: O sistema converte automaticamente traços `-` em barras `/` caso o seu leitor de código de barras esteja em formato de teclado Americano).*
5. Leia o código mágico `O-CMD-VALIDATE` na parede para fechar e concluir.

## 🛠️ Comandos Suportados & Etiquetas
Abra o ficheiro **`etiquetas_comandos.html`** incluído neste módulo num navegador web (ex: Google Chrome) e imprima a folha numa folha A4. Cole-a ao lado da secretária do armazém.
* `O-CMD-VALIDATE` -> Valida/Confirma a transferência atual.
* `O-CMD-CANCEL` -> Cancela a transferência.
* `O-CMD-PRINT` -> Imprime o PDF.

## Autor
* DIGITALUB ANGOLA