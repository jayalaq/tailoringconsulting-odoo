/** @odoo-module **/

import { loadJS } from "@web/core/assets";
import paymentForm from '@payment/js/payment_form';

paymentForm.include({
    init: function () {
        this._super(...arguments);
        this._boundCulqiEventHandler = this._onCulqiEvent.bind(this);
        this.culqiTransactionId = null;
        this.culqiInstance = null;
    },

    // #=== DOM MANIPULATION ===#

    _prepareInlineForm: function (providerId, providerCode, paymentOptionId, paymentMethodCode, flow) {
        if (providerCode !== 'culqi') {
            this._super(...arguments);
            return;
        }
        this._setPaymentFlow('direct');
    },

    // #=== PAYMENT FLOW ===#

    async _processDirectFlow(providerCode, paymentOptionId, paymentMethodCode, processingValues) {
        if (providerCode !== 'culqi') {
            this._super(...arguments);
            return;
        }
        await this._processCulqiPayment(processingValues);
    },

    // #=== PAYMENT FLOW ===#

    async _processCulqiPayment(processingValues) {
        const {
            culqi_public_key: publicKey,
            culqi_config: config,
            transaction_id: transactionId
        } = processingValues;

        this.culqiTransactionId = transactionId;

        try {
            await loadJS('https://js.culqi.com/checkout-js');
            this.culqiInstance = new CulqiCheckout(publicKey, config);
            window.addEventListener('message', this._boundCulqiEventHandler, false);
            this.culqiInstance.open();
            if (!this.culqiInstance.culqiConfig.publicKey) {
                this._enableButton();
                this._displayErrorDialog('Error', 'No ha ingresado la llave pública del comercio o no es válida.');
            }
        } catch (error) {
            console.error('Error al inicializar Culqi:', error);
            this._enableButton();
            this._displayErrorDialog('Error', 'No se pudo inicializar el formulario de pago.');
        }
    },

    _onCulqiEvent: function ({ data }) {
        if (typeof data !== "object" || !data.object) return;
        const { object } = data;
        switch (object) {
            case "token":
                if (this.culqiInstance) {
                    this.culqiInstance.close();
                }
                this._culqiHandleToken(data.id);
                break;
            case "error":
                if (this.culqiInstance) {
                    this.culqiInstance.close();
                }
                this._enableButton();
                this._displayErrorDialog('Error', data.user_message || 'No se pudo procesar el pago.');
                break;
            case "closeCheckout":
                if (this.culqiInstance) {
                    this.culqiInstance.close();
                }
                this._enableButton();
                break;
        }
    },

    async _culqiHandleToken(tokenId) {
        try {
            const result = await this.rpc('/payment/culqi/return', {
                'token_id': tokenId,
                'transaction_id': this.culqiTransactionId,
            });
            if (result?.success) {
                window.location = '/payment/status';
            } else {
                this._enableButton();
                this._displayErrorDialog('Error', result?.error || 'No se pudo procesar el pago.');
            }
        } catch (error) {
            console.error('Error al procesar el token:', error);
            this._enableButton();
            this._displayErrorDialog('Error', 'No se pudo procesar el pago.');
        }
    },

    willDestroy: function () {
        window.removeEventListener('message', this._boundCulqiEventHandler);
        if (this.culqiInstance) {
            try {
                this.culqiInstance.close();
            } catch (error) {
                console.error('Error al cerrar Culqi:', error);
            }
        }
        this.culqiInstance = null;
        this._enableButton();
        this._super.apply(this, arguments);
    },

});
