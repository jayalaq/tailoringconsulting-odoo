/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { Chrome } from "@point_of_sale/app/pos_app";

patch(Chrome.prototype, {
    /**
     * @override
     */
    get showCashMoveButton() {
        const cashier = this.pos.get_cashier();
        return cashier.pos_access_cash_in_out;
    },
});
