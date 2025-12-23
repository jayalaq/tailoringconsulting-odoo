/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Order } from "@point_of_sale/app/store/models";

patch(PosStore.prototype, {
    /**
     * @override
     */
    push_single_order(order) {
        if (order.fake_invoice) {
            order.to_invoice = false;
        }
        return super.push_single_order(order);
    },
});

patch(Order.prototype, {
    /**
     * @override
     */
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.fake_invoice = false;
        const defaultPartner = this.pos.config.ticket_partner_id;
        if (defaultPartner) {
            const partner = this.pos.db.get_partner_by_id(defaultPartner[0]);
            if (options.json) {
                if (!options.json.partner_id) {
                    this.set_partner(partner);
                }
            } else {
                this.set_partner(partner);
            }
        }
    },
    is_fake_invoice() {
        return this.fake_invoice;
    },
});
