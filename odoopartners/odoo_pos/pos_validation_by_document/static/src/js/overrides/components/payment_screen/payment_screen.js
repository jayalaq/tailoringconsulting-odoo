/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { ConfirmPopup } from "@point_of_sale/app/utils/confirm_popup/confirm_popup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";

patch(PaymentScreen.prototype, {
    /**
     * @override
     */
    async validateOrder(isForceValidate) {
        const currentOrder = this.pos.get_order();
        const currentPartner = currentOrder.get_partner();
        const invoiceDiv = $("#invoice_l10n_latam_document_type_ids_div");
        const ticketDiv = $("#ticket_l10n_latam_document_type_ids_div");
        const documentTypeInvoice = invoiceDiv.length === 0;
        const documentTypeTicket = ticketDiv.length === 0;
        const parameters = {
            currentOrder: currentOrder,
            currentPartner: currentPartner,
            invoiceDiv: invoiceDiv,
            ticketDiv: ticketDiv,
            documentTypeInvoice: documentTypeInvoice,
            documentTypeTicket: documentTypeTicket
        }

        if (await this._requiresClientIdentification(parameters)) {
            return;
        }

        if (await this._requiresAlternativeDocument(parameters)) {
            return;
        }

        if (currentPartner !== null) {
            if (await this._validatePartnerIdentification(currentPartner)) {
                return;
            }
        }

        await super.validateOrder(isForceValidate);
    },
    async _requiresClientIdentification(parameters) {
        const { currentOrder, currentPartner, documentTypeInvoice, documentTypeTicket } = parameters;
        if (currentOrder.get_total_with_tax() > this.pos.config.identify_client && (!documentTypeInvoice || !documentTypeTicket)) {
            if (currentPartner !== null) {
                const identificationIsVat = this._findIdentificationTypeById(currentPartner.l10n_latam_identification_type_id[0]).is_vat;
                if (currentPartner.id === this.pos.config.ticket_partner_id[0]) {
                    await this.popup.add(ErrorPopup, {
                        title: _t("Validation Error"),
                        body: _t("The amount of the sale is greater than " + this.pos.config.identify_client + " so you must identify a client.")
                    });
                    return true;
                }
                if (!identificationIsVat) {
                    await this.popup.add(ErrorPopup, {
                        title: _t("Validation Error"),
                        body: _t("Choose a client who has a fiscal identification document.")
                    });
                    return true;
                }
            } else {
                const { confirmed } = await this.popup.add(ConfirmPopup, {
                    title: _t("Customer Required"),
                    body: _t("You must select a customer.")
                });
                if (confirmed) {
                    this.selectPartner();
                }
                return true;
            }
        }
        return false;
    },
    async _requiresAlternativeDocument(parameters) {
        const { currentOrder, currentPartner, invoiceDiv, ticketDiv, documentTypeInvoice, documentTypeTicket } = parameters;
        if (!documentTypeInvoice || !documentTypeTicket) {
            if (currentPartner !== null) {
                const documentId = !documentTypeInvoice ? parseInt(invoiceDiv[0].children[1].value) : parseInt(ticketDiv[0].children[1].value);
                const arrayDocumentIds = this._findIdentificationTypeById(currentPartner.l10n_latam_identification_type_id[0]).invoice_validation_document;
                if (!arrayDocumentIds?.includes(documentId) && currentOrder.get_orderlines().length !== 0) {
                    await this.popup.add(ErrorPopup, {
                        title: _t("Validation Error"),
                        body: _t("It is suggested to use another sales document or change the client's identification type.")
                    });
                    return true;
                }
            } else {
                const { confirmed } = await this.popup.add(ConfirmPopup, {
                    title: _t("Customer Required"),
                    body: _t("You must select a customer.")
                });
                if (confirmed) {
                    this.selectPartner();
                }
                return true;
            }
        }
        return false;
    },
    async _validatePartnerIdentification(currentPartner) {
        const partnerVat = currentPartner.vat;
        if (!partnerVat) {
            await this.popup.add(ErrorPopup, {
                title: _t("Validation Error"),
                body: _t("The customer must have an identification number."),
            });
            return true;
        }

        const partnerIdentificationTypeData = this._findIdentificationTypeById(currentPartner.l10n_latam_identification_type_id[0]);

        if (await this._validateLengthVAT(partnerVat, partnerIdentificationTypeData.doc_length, partnerIdentificationTypeData.exact_length)) {
            return true;
        }

        if (await this._validateStructureVAT(partnerVat, partnerIdentificationTypeData.doc_type)) {
            return true;
        }
        return false;
    },
    async _validateLengthVAT(vat, docLength, exactLength) {
        if (exactLength === "exact") {
            if (vat.length !== docLength) {
                await this.popup.add(ErrorPopup, {
                    title: _t("Validation Error"),
                    body: _t(`- The number of characters for the identification number must be: ${docLength}.`)
                });
                return true;
            }
        } else if (exactLength === 'maximum') {
            if (vat.length > docLength) {
                await this.popup.add(ErrorPopup, {
                    title: _t("Validation Error"),
                    body: _t(`- The number of characters for the identification number must be at most: ${docLength}.`)
                });
                return true;
            }
        }
        return false;
    },
    async _validateStructureVAT(vat, docType) {
        if (docType === "other") {
            return false;
        } else if (docType === "numeric") {
            if (!(/^\d+$/.test(vat))) {
                await this.popup.add(ErrorPopup, {
                    title: _t("Validation Error"),
                    body: _t("- The identification number must contain only numbers.")
                });
                return true;
            }
            const digitSum = vat.split("").reduce((sum, digit) => sum + parseInt(digit), 0);
            if (digitSum === 0) {
                await this.popup.add(ErrorPopup, {
                    title: _t("Validation Error"),
                    body: _t("- The identification number cannot contain only zeros.")
                });
                return true;
            }
        } else if (docType === "alphanumeric") {
            const specialCharacters = '-°%&=~\\+?*^$()[]{}|@%#"/¡¿!:.,;';
            if ([...vat].some(char => specialCharacters.includes(char))) {
                await this.popup.add(ErrorPopup, {
                    title: _t("Validation Error"),
                    body: _t("- The identification number contains not allowed characters.")
                });
                return true;
            }
        }
        return false;
    },
    _findIdentificationTypeById(identificationTypeId) {
        const identificationTypes = this.pos.l10n_latam_identification_types;
        return Object.values(identificationTypes).find(type => type.id === identificationTypeId) || false;
    },
});
