# utf-8


class ReportInvBalTxt(object):

    def __init__(self, obj, data):
        self.obj = obj
        self.data = data

    def get_content(self):
        raw = ""
        template = "{period}|{stock_catalog}|{stock_type}|{default_code}|{code_catalog_used}|{unspsc_code}|{product_description}|{product_udm}|{property_cost_method}|{quantity_product_hand}|{standard_price}|{total}|1|\r\n"

        for value in self.data:
            raw += template.format(
                period=value["period"],
                stock_catalog=value["stock_catalog"],
                stock_type=value["stock_type"],
                default_code=value["default_code"],
                code_catalog_used=value["code_catalog_used"],
                unspsc_code=value["unspsc_code"],
                product_description=value["product_description"],
                product_udm=value["product_udm"],
                property_cost_method=value["property_cost_method"],
                quantity_product_hand="{:.2f}".format(value["quantity_product_hand"]),
                standard_price="{:.2f}".format(value["standard_price"]),
                total="{:.2f}".format(value["total"]),
            )
        return raw

    def get_filename(self):
        year, month, day = self.obj.date_end.strftime("%Y/%m/%d").split("/")
        return "LE{vat}{period_year}{period_month}{period_day}030700{eeff_oportunity}{state_send}{has_info}11.txt".format(
            vat=self.obj.company_id.vat,
            period_year=year,
            period_month=month,
            period_day=day,
            eeff_oportunity=self.obj.eeff_presentation_opportunity,
            state_send=self.obj.state_send or "",
            has_info=int(bool(self.data)),
        )
