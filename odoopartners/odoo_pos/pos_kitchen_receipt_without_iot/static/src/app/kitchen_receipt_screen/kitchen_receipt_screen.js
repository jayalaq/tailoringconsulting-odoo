/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { useErrorHandlers } from "@point_of_sale/app/utils/hooks";
import { registry } from "@web/core/registry";
import { onMounted, Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { ConfirmPopup } from "@point_of_sale/app/utils/confirm_popup/confirm_popup";
import { useService } from "@web/core/utils/hooks";

export class KitchenReceiptScreen extends Component {
    static template = "pos_kitchen_receipt_without_iot.KitchenReceiptScreen";

    setup() {
        this.pos = usePos();
        this.hardwareProxy = useService("hardware_proxy");
        this.popup = useService("popup");
        useErrorHandlers();
        onMounted(this.onMounted);
    }

    onMounted() {
        const receiptList = this.props.receiptList || [];
        let contentHtml = "";
        const containerCenteredContent = document.querySelector('div[name="centered_content"]');
        if (this.pos.config.use_multi_printer){
            receiptList.forEach((receipt, index) => {
                const id = `ticket_container_${index}`;
                contentHtml += `
                    <button class="button print btn btn-lg btn-primary" data-receipt-id="${id}">
                        <i class="fa fa-print ms-2"></i> Print
                    </button>
                    <div id="${id}" class="pos-receipt-container mt-2 bg-200 text-center">
                        <div class="d-inline-block m-3 p-3 border rounded bg-view text-start overflow-hidden" style="width: 240px;">
                            ${receipt.outerHTML}
                        </div>
                    </div>
                    <br/>
                `;
            });
        } else {
            const id = 'ticket_container';
            contentHtml += `
            <button class="button print btn btn-lg btn-primary" data-receipt-id="${id}">
                <i class="fa fa-print ms-2"></i> Print
            </button>
            <div id="${id}" class="pos-receipt-container mt-2 bg-200 text-center" style="display: grid;">
                ${receiptList.map(receipt => `
                    <div class="d-inline-block m-3 p-3 border rounded bg-view text-start overflow-hidden" style="width: 240px;">
                        ${receipt.outerHTML}
                    </div>
                `).join('')}
            </div>`;
        }
        
        containerCenteredContent.innerHTML = contentHtml;

        // Add event listeners to the print buttons
        containerCenteredContent.querySelectorAll(".print").forEach(button => {
            button.addEventListener("click", async (event) => {
                const receiptId = event.currentTarget.dataset.receiptId;
                await this.printReceipt(receiptId);
            });
        });
    }

    confirm() {
        this.props.resolve({ confirmed: true, payload: null });
        this.pos.closeTempScreen();
    }

    async printReceipt(receiptId) {
        const printOptions = {
            printable: receiptId,
            type: "html",
            css: '/pos_kitchen_receipt_without_iot/static/src/css/pos_receipts.css',
            scanStyles: false,
            targetStyles: ["*"],
            documentTitle: _t("Print"),
        };
        if (this.hardwareProxy.printer) {
            const receiptElement = document.getElementById(receiptId);
            const htmlDataList = this.pos.config.use_multi_printer
                ? [receiptElement.innerHTML]
                : Array.from(receiptElement.querySelectorAll('.pos-receipt-container > .d-inline-block')).map(el => el.innerHTML);
    
            for (const html_data of htmlDataList) {
                const { successful, message } = await this.hardwareProxy.printer.printReceipt(html_data);
                if (!successful) {
                    await this.popup.add(ErrorPopup, {
                        title: message.title,
                        body: message.body,
                    });
                    const { confirmed } = await this.popup.add(ConfirmPopup, {
                        title: message.title,
                        body: _t('Do you want to print using the web printer?'),
                    });
                    if (confirmed) {
                        this.printWithWebPrinter(printOptions);
                    }
                    break;
                }
            }
        } else {
            this.printWithWebPrinter(printOptions);
        }
    }

    printWithWebPrinter(printOptions) {
        try {
            printJS(printOptions);
        } catch (error) {
            this.popup.add(ErrorPopup, {
                title: _t("Printing is not supported on some browsers"),
                body: _t("It is possible to print your tickets by making use of an IoT Box."),
            });
        }
    }
}

registry.category("pos_screens").add("KitchenReceiptScreen", KitchenReceiptScreen);
