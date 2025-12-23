/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";

patch(TicketScreen.prototype, {
    /**
     * @override
     */
    async onDoRefund() {
        await super.onDoRefund();
        const selectedOrder = this.getSelectedOrder();
        const order = this.pos.get_order();
        if (selectedOrder && order) {
            order["account_move_rel_name"] = selectedOrder["account_move_rel_name"];
            order["account_move_rel_document_type"] = selectedOrder["account_move_rel_document_type"];
            order["account_move_rel_invoice_date"] = selectedOrder["account_move_rel_invoice_date"];
        }
    },
    /**
     * @override
     */
    _getSearchFields() {
        return Object.assign({}, super._getSearchFields(...arguments), {
            ACCOUNT_MOVE_DOCUMENT_TYPE: {
                repr: (order) => order.account_move_rel_document_type,
                displayName: _t("Document Type"),
                modelField: "account_move_rel_document_type",
            },
            ACCOUNT_MOVE_NAME: {
                repr: (order) => order.account_move_rel_name,
                displayName: _t("Invoice Number"),
                modelField: "account_move_rel_name",
            },
        });
    },
});
