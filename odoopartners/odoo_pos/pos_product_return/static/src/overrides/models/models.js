/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { Order } from "@point_of_sale/app/store/models";

patch(Order.prototype, {
    /**
     * @override
     */
    init_from_JSON(json) {
        super.init_from_JSON(json);
        this.account_move_rel_name = json.account_move_rel_name || "-";
        this.account_move_rel_document_type = json.account_move_rel_document_type || "-";
        this.account_move_rel_invoice_date = json.account_move_rel_invoice_date || false;
    },
    /**
     * @override
     */
    export_as_JSON() {
        const json = super.export_as_JSON();
        json.account_move_rel_name = this.account_move_rel_name;
        json.account_move_rel_document_type = this.account_move_rel_document_type;
        json.account_move_rel_invoice_date = this.account_move_rel_invoice_date;
        return json;
    },
});
