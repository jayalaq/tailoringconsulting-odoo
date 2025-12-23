/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Order, Orderline } from "@point_of_sale/app/store/models";

// Helper function to calculate the number of decimals
function calculateDecimals(rounding) {
    return rounding > 0 ? Math.ceil(Math.log10(1.0 / rounding)) : 0;
}

function loadMultiCurrency(currencyList) {
    for (const [key, currency] of Object.entries(currencyList)) {
        currency.decimals = calculateDecimals(currency.rounding);
    }
}

patch(PosStore.prototype, {
    /**
     * @override
     */
    async _processData(loadedData) {
        this.currency_list = loadedData["currency_list"];
        this.dict_curr_list = loadedData["dict_curr_list"];
        loadMultiCurrency(this.currency_list);
        loadMultiCurrency(this.dict_curr_list);
        await super._processData(loadedData);
    },
});

patch(Order.prototype, {
    set_currency_mode(mode) {
        this.currency_mode = mode;
    },
    get_currency_mode() {
        return this.currency_mode;
    },
    set_currency_id(currency) {
        this.order_currency_id = currency;
    },
    get_currency_id() {
        return this.order_currency_id;
    },
    set_amount_currency(amount) {
        this.amount_currency = amount;
    },
    get_amount_currency() {
        return this.amount_currency;
    },
    set_currency_receipt_mode(curr_receipt_mode) {
        this.curr_receipt_mode = curr_receipt_mode;
    },
    get_currency_receipt_mode() {
        return this.curr_receipt_mode;
    },
    /**
     * @override
     */
    export_as_JSON() {
        return {
            ...super.export_as_JSON(),
            order_currency_id: this.get_currency_id() || false,
            amount_currency: this.get_amount_currency() || false,
        };
    },
    /**
     * @override
     */
    export_for_printing() {
        return {
            ...super.export_for_printing(),
            order_currency_id: this.get_currency_id() || false,
            amount_currency: this.get_amount_currency() || false,
            curr_receipt_mode: this.get_currency_receipt_mode() || false,
            dict_curr_list: this.pos.dict_curr_list || {},
            headerData: {
                ...super.export_for_printing().headerData,
                order_currency_id: this.get_currency_id() || false,
                curr_receipt_mode: this.get_currency_receipt_mode() || false,
                dict_curr_list: this.pos.dict_curr_list || {},
            },
        };
    },
});

patch(Orderline.prototype, {
    set_line_amount_currency(line_amount_currency) {
        this.line_amount_currency = line_amount_currency;
    },
    get_line_amount_currency() {
        return this.line_amount_currency;
    },
    /**
     * @override
     */
    export_as_JSON() {
        return {
            ...super.export_as_JSON(),
            line_amount_currency: this.get_line_amount_currency() || false,
        };
    },
    /**
     * @override
     */
    export_for_printing() {
        return {
            ...super.export_for_printing(),
            line_amount_currency: this.get_line_amount_currency() || false,
        };
    },
});
