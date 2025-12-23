from io import BytesIO

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class ReportInvBalExcel(object):

    def __init__(self, obj, data):
        self.obj = obj
        self.data = data

    def get_content(self):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})

        style1 = workbook.add_format(
            {
                "align": "center",
                "valign": "vcenter",
                "size": 10,
                "bold": True,
                "font_name": "Arial",
            }
        )
        style_number = workbook.add_format(
            {
                "size": 11,
                "num_format": "0.00",
            }
        )

        ws = workbook.add_worksheet("Merca y Prod Term")
        ws.set_column("A:H", 15)

        ws.set_row(0, 50)

        headers = [
            "Periodo",
            "Código del catálogo utilizado",
            "Tipo de existencia",
            "Código propio de la existencia",
            "Código del catálogo utilizado",
            "Código de Existencia",
            "Descripción de la existencia",
            "Código de la Unidad de medida de la existencia",
            "Código del método de valuación utilizado",
            "Cantidad de la existencia",
            "Costo unitario de la existencia",
            "Costo Total",
            "Estado de Operación/codeprefix",
        ]

        for col, header in enumerate(headers):
            ws.write(0, col, header, style1)

        for i, value in enumerate(self.data, start=1):
            ws.write(i, 0, value["period"])
            ws.write(i, 1, value["stock_catalog"])
            ws.write(i, 2, value["stock_type"])
            ws.write(i, 3, value["default_code"])
            ws.write(i, 4, value["code_catalog_used"])
            ws.write(i, 5, value["unspsc_code"])
            ws.write(i, 6, value["product_description"])
            ws.write(i, 7, value["product_udm"])
            ws.write(i, 8, value["property_cost_method"])
            ws.write(i, 9, value["quantity_product_hand"], style_number)
            ws.write(i, 10, value["standard_price"], style_number)
            ws.write(i, 11, value["total"], style_number)
            ws.write(i, 12, 1)

        workbook.close()
        output.seek(0)
        return output.read()

    def get_filename(self):
        year_month = self.obj.date_end.strftime("%Y%m")
        return "Libro_Mercaderías y Productos Terminados_{}.xlsx".format(year_month)
