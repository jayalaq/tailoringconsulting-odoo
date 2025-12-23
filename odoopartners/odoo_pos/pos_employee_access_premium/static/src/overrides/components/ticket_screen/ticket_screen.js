/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

patch(TicketScreen.prototype, {
    /**
     * @override
     */
    async onDeleteOrder(order) {
        const cashier = this.pos.get_cashier();
        if (!cashier.pos_access_delete_orders) {
            await this.popup.add(ErrorPopup, {
                title: _t("Access Denied"),
                body: _t("You do not have access to delete orders."),
            });
        } else {
            await super.onDeleteOrder(order);
        }
    },
    /**
     * @override
     */
    async onDoRefund() {
        const cashier = this.pos.get_cashier();
        if (!cashier.pos_access_make_refunds) {
            this.popup.add(ErrorPopup, {
                title: _t("Access Denied"),
                body: _t("You do not have access to make refunds."),
            });
        } else {
            await super.onDoRefund();
        }
    },
});
