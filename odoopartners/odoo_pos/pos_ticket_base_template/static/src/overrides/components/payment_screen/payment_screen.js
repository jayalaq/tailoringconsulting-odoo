/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { ConnectionLostError } from "@web/core/network/rpc_service";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";

patch(PaymentScreen.prototype, {
    /**
     * @override
     */
    async _finalizeValidation() {
        var self = this;

        if (this.currentOrder.is_paid_with_cash() || this.currentOrder.get_change()) {
            this.hardwareProxy.openCashbox();
        }

        const domain = [['pos_reference', '=', this.currentOrder['name']]]
        const fields = ['account_move'];
        this.currentOrder.date_order = luxon.DateTime.now();
        for (const line of this.paymentLines) {
            if (!line.amount === 0) {
                this.currentOrder.remove_paymentline(line);
            }
        }
        this.currentOrder.finalized = true;

        // 1. Save order to server.
        this.env.services.ui.block();
        const syncOrderResult = await this.pos.push_single_order(this.currentOrder);
        this.env.services.ui.unblock();

        if (syncOrderResult instanceof ConnectionLostError) {
            this.pos.showScreen(this.nextScreen);
            return;
        } else if (!syncOrderResult) {
            return;
        }

        try {
            // 2. Invoice.
            // start override
            if (this.shouldDownloadInvoice() && (this.currentOrder.is_to_invoice() || this.currentOrder.fake_invoice) && this.pos.config.automatic_download_electronic_invoice) {
                if (syncOrderResult[0]?.account_move) {
                    const reportActionRef = this.pos.getReportActionRef();
                    await this.report.doAction(reportActionRef, [
                        syncOrderResult[0].account_move,
                    ]);
                } else {
                    throw {
                        code: 401,
                        message: "Backend Invoice",
                        data: { order: this.currentOrder },
                    };
                }
            }
            // end override
        } catch (error) {
            if (error instanceof ConnectionLostError) {
                Promise.reject(error);
                return error;
            } else {
                throw error;
            }
        }

        if(this.pos.config?.invoice_number){
            if (this.currentOrder.is_to_invoice() || this.currentOrder.fake_invoice) {
                await this.orm.call(
                    "pos.order",
                    "search_read",
                    [domain, fields],
                ).then(function (output) {
                    const inv_print = output[0]['account_move'][1].split(" (")[0];
                    self.currentOrder.set_invoice_number(inv_print);
                })
            }
        }

        // 3. Post process.
        if (
            syncOrderResult &&
            syncOrderResult.length > 0 &&
            this.currentOrder.wait_for_push_order()
        ) {
            await this.postPushOrderResolve(syncOrderResult.map((res) => res.id));
        }

        await this.afterOrderValidation(!!syncOrderResult && syncOrderResult.length > 0);

        // start override
        if ((this.currentOrder.is_to_invoice() || this.currentOrder.fake_invoice) && this.pos.config.automatic_print_electronic_invoice) {
            if (syncOrderResult[0]?.account_move) {
                await this.pos.reportActionPrint(syncOrderResult[0].account_move);
            } else {
                throw {
                    code: 401,
                    message: "Backend Invoice",
                    data: { order: this.currentOrder },
                };
            }
        }
        // end override
    },
});
