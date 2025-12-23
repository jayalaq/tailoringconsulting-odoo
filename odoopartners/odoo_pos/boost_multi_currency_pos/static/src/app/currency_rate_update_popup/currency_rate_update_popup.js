/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { parseFloat } from "@web/views/fields/parsers";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { roundDecimals as round_di } from "@web/core/utils/numbers";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";

export class CurrencyRateUpdatePopup extends AbstractAwaitablePopup {
    static template = "boost_multi_currency_pos.CurrencyRateUpdatePopup";
    static defaultProps = {
        cancelText: _t("Cancel"),
        title: _t("Update Rate"),
        body: "",
    };

    setup() {
        super.setup();
        this.popup = useService("popup");
        this.orm = useService("orm");
        this.pos = usePos();
    }

    format_foreign(amount, currency, precision) {
        if (!amount && !currency) {
            return
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
    }

    async _update_rate(event) {
        const currentOrder = this.pos.get_order();
        const currency_id = parseInt(self.$("#currency_selection").val());
        const new_rate = parseFloat(self.$("#new_rate").val());
        if (new_rate && new_rate > 0) {
            try {
                const new_currency = await this.orm.call(
                    "res.currency.rate",
                    "currency_rate_update",
                    [currency_id, new_rate]
                );
                if (new_currency) {
                    const all_currencies = this.pos.dict_curr_list;
                    for (const [currency, key] of Object.entries(all_currencies)) {
                        if (new_currency.currency_id[0] === parseInt(currency)) {
                            key.rate = new_currency.rate;
                            const update_currency = this.pos.dict_curr_list[key.id];
                            const currency_total = currentOrder.get_total_with_tax() * update_currency.rate;
                            const total_in = _t("Total in");
                            self.$("#conversion_rate").html(`1 ${update_currency.name} = ${update_currency.rate} ${update_currency.name}`);
                            self.$("#currency_value_label").html(`${total_in} ${update_currency.name}:`);
                            self.$("#currency_value").html(`${update_currency.symbol} ${currency_total}`);
                        }
                    }
                }
            } catch (error) {
                console.error(error);
            }
            this.cancel();
        } else {
            this.popup.add(ErrorPopup, {
                title: _t("Error"),
                body: _t("Please enter new rate of currency in proper format"),
            });
            self.$("#new_rate").focus();
        }
    }
};
