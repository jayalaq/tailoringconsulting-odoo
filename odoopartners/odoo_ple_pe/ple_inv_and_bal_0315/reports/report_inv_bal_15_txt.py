import re


class ReportInvBal15Txt(object):

    def __init__(self, obj, data_1):
        self.obj = obj
        self.data_1 = data_1

    def get_content(self):
        raw = ''
        template = '{name}|{accounting_seat}|{correlative}|{type_l10n_latam_identification}|{serial_number_payment}|' \
                   '{related_payment_voucher}|{code}|{ref}|{outstanding_balance}|{additions}|{deductions}|' \
                   '{account_status}|\r\n'

        data = []
        for i in range(len(self.data_1)):
            join = {**self.data_1[i]}
            data.append(join)

        adi = '0.00'
        sub = '0.00'
        for value in data:
            name_document_string = ''.join(char for char in value['document_name'] if char.isalnum())

            raw += template.format(
                name = value['name'],
                accounting_seat = name_document_string,
                correlative = value['correlative'],
                type_l10n_latam_identification = value['type_l10n_latam_identification'],
                serial_number_payment = value['serial_number_payment'],
                related_payment_voucher = value['related_payment_voucher'],
                code = re.sub(r"[^a-zA-Z0-9]", "", value['code']),
                ref = value['ref'][:40] if len(value['ref']) > 40 else value['ref'],
                outstanding_balance= "{:.2f}".format(float(value['outstanding_balance'])),
                additions=adi,
                deductions=sub,
                account_status="1"
            )
        return raw

    def get_filename(self):
        year, month, day = self.obj.date_end.strftime('%Y/%m/%d').split('/')
        return 'LE{vat}{period_year}{period_month}{period_day}031500{eeff_oportunity}{state_send}{has_info}11.txt'.format(
            vat=self.obj.company_id.vat,
            period_year=year,
            period_month=month,
            period_day=day,
            eeff_oportunity=self.obj.eeff_presentation_opportunity,
            state_send=self.obj.state_send or '',
            has_info=int(bool(self.data_1))
        )
