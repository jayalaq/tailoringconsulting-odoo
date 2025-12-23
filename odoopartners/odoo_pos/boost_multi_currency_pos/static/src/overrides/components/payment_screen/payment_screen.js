/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { CurrencyRateUpdatePopup } from "@boost_multi_currency_pos/app/currency_rate_update_popup/currency_rate_update_popup";
import { roundDecimals as round_di } from "@web/core/utils/numbers";
import { _t } from "@web/core/l10n/translation";

patch(PaymentScreen.prototype, {
    /**
     * @override
     */
    selectPaymentLine(event) {
        super.selectPaymentLine(event);
        self.$("#curr_input").val("");
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
    set_foreign_values(currency_id) {
        const currentOrder = this.pos.get_order();
        const currency = this.pos.dict_curr_list[currency_id];
        if (currency) {
            const decimals = currency.decimals;
            const currency_total = currentOrder.get_total_with_tax() * currency.rate;
            const total_in = _t("Total in");
            const paid_in = _t("Paid in");
            const receipt_in = _t("Receipt in");
            if (this.pos.config.display_conversion)
                self.$("#conversion_rate").html("1 " + this.pos.currency.name + " = " + currency.rate + " " + currency.name);
            self.$("#currency_value_label").html(total_in + " " + currency.name + ":");
            self.$("#currency_value").html(currency.symbol + " " + currency_total);
            self.$("#foreign_input_label").html(paid_in + " " + currency.name + ":");
            self.$("#receipt_currency_label").html(receipt_in + " " + currency.name + ":");
        }
    },
    value_input(event) {
        // this event will call each one write values in curr_input , set payment
        const currentOrder = this.pos.get_order();
        const curr_input = self.$("#curr_input").val();
        const line = currentOrder.selected_paymentline;
        if (line == undefined) {
            this.popup.add(ErrorPopup, {
                title: _t("Error"),
                body: _t("No Payment Line selected !."),
            });
            self.$("#curr_input").val("");
            return false;
        }
        const curr_id = self.$("#currency_selection").val();
        const currency = this.pos.dict_curr_list[curr_id];
        if (currency) {
            const converted_value = curr_input / currency.rate;
            line.set_amount(converted_value);
        }
    },
    switch_change(event) {
        // add section for multi currency
        const currentOrder = this.pos.get_order();
        currentOrder.set_currency_mode(true);
        currentOrder.set_currency_receipt_mode(false);
        const toggle_multi_currency = self.$("#toggle_multi_currency").prop("checked");
        const line = currentOrder.selected_paymentline;
        if (toggle_multi_currency) {
            if (self.$(".multi_currency_pos").hasClass("display-none")) {
                self.$(".multi_currency_pos").removeClass("display-none");
            }
            if (self.$(".div_currency_inputs").hasClass("display-none")) {
                self.$(".div_currency_inputs").removeClass("display-none");
            }
            self.$(".multi_currency_pos").show();
            self.$(".div_currency_inputs").show();
            const curr_id = parseInt(self.$("#currency_selection").val());
            this.set_foreign_values(curr_id);
            self.$("#curr_input").focus();
            if (self.$("#curr_input").val() !== "")
                self.$("#curr_input").select();
        } else {
            self.$(".multi_currency_pos").hide();
            self.$(".div_currency_inputs").hide();
            if (!self.$(".multi_currency_pos").hasClass("display-none")) {
                self.$(".multi_currency_pos").addClass("display-none");
            }
            if (!self.$(".div_currency_inputs").hasClass("display-none")) {
                self.$(".div_currency_inputs").addClass("display-none");
            }
            currentOrder.set_currency_mode(false);
            if (line === undefined || line === "") {
                self.$(".paymentline input").val(0);
                return false;
            }
            self.$("#curr_input").val("");
            line.set_amount(0);
        }
    },
    receipt_change() {
        const currentOrder = this.pos.get_order();
        if (self.$("#curr_receipt").prop("checked") == true) {
            currentOrder.set_currency_receipt_mode(true);
        } else {
            currentOrder.set_currency_receipt_mode(false);
        }
    },
    currency_selection() {
        return this.pos.currency_list[0];
    },
    select_change(event) {
        // set values for selection currency
        const currentOrder = this.pos.get_order();
        const line = currentOrder.selected_paymentline;
        if (line) {
            line.set_amount(0);
        }
        self.$("#curr_input").focus();
        const curr_id = parseInt(self.$("#currency_selection").val());
        this.set_foreign_values(curr_id);
        self.$("#curr_input").val("");
    },
    update_rate() {
        // update rate in screen with the helped popup
        const curr_id = self.$("#currency_selection").val();
        const currency = this.pos.dict_curr_list[curr_id];
        this.popup.add(CurrencyRateUpdatePopup, {
            title: _t("Update Rate"),
            confirmText: _t("Exit"),
            currency: currency
        });
    },
    /**
     * @override
     */
    async validateOrder(isForceValidate) {
        const order = this.pos.get_order();
        const value = self.$("#curr_input").val();
        order.set_currency_id(false);

        if (order.get_currency_mode() && Number(value) > 0) {
            const selected_currency = parseInt(self.$("#currency_selection").val());
            const currency = this.pos.dict_curr_list[selected_currency];
            order.set_currency_id(selected_currency);
            order.set_amount_currency(value);
            const orderlines = order.get_orderlines();
            if (orderlines) {
                orderlines.forEach((line) => {
                    const line_amount_currency = round_di(line.get_price_with_tax() * currency.rate, currency.decimals).toFixed(currency.decimals);
                    line.set_line_amount_currency(line_amount_currency);
                });
            }
        }

        if (this.pos.config.cash_rounding) {
            if (!this.pos.get_order().check_paymentlines_rounding()) {
                this.popup.add(ErrorPopup, {
                    title: _t("Rounding error in payment lines"),
                    body: _t("The amount of your payment lines must be rounded to validate the transaction."),
                });
                return;
            }
        }

        return super.validateOrder(...arguments);
    },
});
