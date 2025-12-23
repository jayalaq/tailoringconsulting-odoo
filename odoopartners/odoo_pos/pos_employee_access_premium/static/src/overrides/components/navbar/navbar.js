/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { Navbar } from "@point_of_sale/app/navbar/navbar";

patch(Navbar.prototype, {
    /**
     * @override
     */
    get showCashMoveButton() {
        const cashier = this.pos.get_cashier();
        return cashier.pos_access_cash_in_out;
    },
});
