/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { roundDecimals as round_di } from "@web/core/utils/numbers";

patch(OrderReceipt.prototype, {
    /**
     * @override
     */
    setup() {
        super.setup();
        this.pos = usePos();
    },
    convert_currency(currency_id, amount) {
        if (!currency_id && !amount) {
            return;
        }

        const numericAmount = typeof amount === 'string'
            ? parseFloat(amount.replace(/[^\d.-]/g, ''))
            : amount;

        if (isNaN(numericAmount)) {
            return false;
        }

        const currency = this.pos.dict_curr_list[currency_id];
        if (currency) {
            const decimals = currency.decimals;
            const currency_total = round_di(numericAmount * currency.rate, decimals).toFixed(decimals);
            return currency_total;
        } else {
            return false;
        }
    },
    format_foreign(amount, currency, precision) {
        if (!amount && !currency) {
            return;
        }
        const decimals = currency.decimals;
        if (precision && (typeof this.pos.dp[precision]) !== undefined) {
            decimals = this.pos.dp[precision];
        }
        if (typeof amount === "number") {
            amount = round_di(amount, decimals).toFixed(decimals);
        }
        if (currency.position === "after") {
            return amount + " " + (currency.symbol || "");
        } else {
            return (currency.symbol || "") + " " + amount;
        }
    },
});
