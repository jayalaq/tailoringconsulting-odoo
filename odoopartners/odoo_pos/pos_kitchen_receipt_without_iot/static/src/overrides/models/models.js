/** @odoo-module */

import { renderToElement } from "@web/core/utils/render";
import { patch } from "@web/core/utils/patch";
import { Order } from "@point_of_sale/app/store/models";

patch(Order.prototype, {
    /**
     * @override
     */
    async printChanges(cancelled) {
        if (!this.pos.config.allow_kitchens_receipt){
            return false;
        }

        const orderChange = this.changesToOrder(cancelled);
        let isPrintSuccessful = true;
        let isPrintBrowser = false;
        let receiptList = [];
        const d = new Date();
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, "0");
        const day = String(d.getDate()).padStart(2, "0");
        const formattedDate = `${day}/${month}/${year}`;
        const hours = d.getHours().toString().padStart(2, '0');
        const minutes = d.getMinutes().toString().padStart(2, '0');
        const seconds = d.getSeconds().toString().padStart(2, '0');

        for (const printer of this.pos.unwatched.printers) {
            const changes = this._getPrintingCategoriesChanges(
                printer.config.product_categories_ids,
                orderChange
            );
            if (changes["new"].length > 0 || changes["cancelled"].length > 0) {
                const printingChanges = {
                    new: changes["new"],
                    cancelled: changes["cancelled"],
                    table_name: this.pos.config.module_pos_restaurant
                        ? this.getTable().name
                        : false,
                    floor_name: this.pos.config.module_pos_restaurant
                        ? this.getTable().floor.name
                        : false,
                    name: this.name || "unknown order",
                    date: formattedDate,
                    time: {
                        hours,
                        minutes,
                        seconds,
                    },
                    cashier_name: this.pos.get_cashier().name,
                };

                const orderChangeReceipt = renderToElement("pos_kitchen_receipt_without_iot.KitchenOrderChangeReceipt", {
                    changes: printingChanges,
                });

                if (printer.config.printer_type === "web_printer") {
                    isPrintBrowser = true;
                    receiptList.push(orderChangeReceipt);
                } else {
                    const result = await printer.printReceipt(orderChangeReceipt);
                    if (!result.successful) {
                        isPrintSuccessful = false;
                        await this.env.services.popup.add(ErrorPopup, {
                            title: _t("Printer connection failed"),
                            body: _t(`Please check if the printer is connected and properly configured. Error with printer: ${printer.config.name}`),
                        });
                        const { confirmed } = await this.env.services.popup.add(ConfirmPopup, {
                            title: _t("Using the web printer"),
                            body: _t("Do you want to print using the web printer?"),
                        });
                        if (confirmed) {
                            isPrintSuccessful = true;
                            isPrintBrowser = true;
                            receiptList.push(orderChangeReceipt);
                        }
                    }
                }
            }
        }
        if (isPrintBrowser && !this.finalized) {
            await this.pos.showTempScreen("KitchenReceiptScreen", {
                receiptList: receiptList
            });
        }
        return isPrintSuccessful;
    }
});
