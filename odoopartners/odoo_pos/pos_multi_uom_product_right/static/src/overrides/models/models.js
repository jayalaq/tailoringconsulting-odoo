/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { Order, Orderline } from "@point_of_sale/app/store/models";

patch(Order.prototype, {
    /**
     * @override
     */
    set_pricelist(pricelist) {
        this.pricelist = pricelist;
        const lines_to_recompute = this.get_orderlines().filter(line => !line.price_manually_set);
        lines_to_recompute.forEach(line => {
            if (line.product_uom === '') {
                line.set_unit_price(line.product.get_price(this.pricelist, line.get_quantity()));
                this.fix_tax_included_price(line);
            }
        });
    }
});

patch(Orderline.prototype, {
    /**
     * @override
     */
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.has_multi_uom = json.has_multi_uom;
        this.allow_uoms = json.allow_uoms;
        this.product_uom = json.product_uom;
    },
    /**
     * @override
     */
    export_as_JSON() {
        const json = super.export_as_JSON();
        json.has_multi_uom = this.get_has_multi_uoms();
        json.allow_uoms = this.get_allow_uoms();
        json.product_uom = this.get_product_uom();
        return json;
    },
    /**
     * @override
     */
    export_for_printing() {
        const receipt = super.export_for_printing();
        receipt.has_multi_uom = this.get_product().has_multi_uom;
        receipt.allow_uoms = this.get_product().allow_uoms;
        return receipt;
    },
    export_own_data(data) {
        const own_data = [];
        if (this.own_data) {
            Object.keys(data).forEach(rec => {
                own_data.push({
                    'product_uom': this.own_data[rec]['product_uom']
                });
            });
        }
        return own_data;
    },
    set_product_uom(uom_id) {
        this.product_uom = this.pos.units_by_id[uom_id];
    },
    get_has_multi_uoms() {
        if (this['has_multi_uom'] === undefined) {
            return this.product.has_multi_uom;
        }
        return this.has_multi_uom;
    },
    get_allow_uoms() {
        if (this['allow_uoms'] === undefined) {
            return this.product.allow_uoms;
        }
        return this.allow_uoms;
    },
    get_product_uom() {
        if (this['product_uom'] === undefined) {
            const uom_id = this.product.uom_id[0];
            return this.pos.units_by_id[uom_id];
        }
        return this.product_uom;
    },
    get_unit() {
        if (!this.product_uom) {
            return this.product.get_unit();
        }
        if (this.pos.units_by_id[this.product_uom['id']]) {
            return this.pos.units_by_id[this.product_uom['id']];
        }
        return this.product.get_unit();
    },
    /**
     * @override
     */
    getDisplayData() {
        return {
            ...super.getDisplayData(),
            has_multi_uom: this.get_product().has_multi_uom,
        };
    },
});
