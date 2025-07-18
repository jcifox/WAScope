# Deprecated
import base64
import time
from reportlab.lib.pagesizes import A1 as paper_size
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, PageBreak, LongTable
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from lib import Utils as Utility
from core.ControllerRequestRecord import ControllerRequestRecord


def handler_table_data(_data, _fontStyle):
    table_data = []
    for row in _data:
        table_row = []
        for cell in row:
            table_row.append(Paragraph(cell, _fontStyle))
        table_data.append(table_row)

    col_widths = [160, 200, 200, 400, 160]
    table = LongTable(table_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ("FONTNAME", (0, 0), (-1, -1), 'ChineseFont'),
        ("FONTSIZE", (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.beige),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black), 
        ("VALIGN", (0, 0), (-1, 0), 'MIDDLE'),
    ]))
    return table


def create_pdf(_host):
    pdfmetrics.registerFont(TTFont('ChineseFont', './font/msyh.ttc'))
    path = './report_output/'
    file = _host + '_' + str(time.time()) + '_report.pdf'
    content = []
    pdf = SimpleDocTemplate(path + file, pagesize=paper_size)
    pdf.allowSplitting = 0
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    normal_style = ParagraphStyle(name='CustomColor', textColor=colors.black, fontSize=12, leading=18, fontName='ChineseFont', escape=False)

    content.append(Paragraph("Analysis Report", title_style))

    CtrlReqRecd = ControllerRequestRecord()
    rs = CtrlReqRecd.query_record_second_analysis(_host=_host)
    for item in rs:
        for pageItem in item['page']:
            riskFlag = len(pageItem['taint_analysis']) > 0
            if riskFlag:
                content.append(
                    Paragraph("Referer:{referer}".format(referer=Utility.disable_sign_escape(item['referer'])), normal_style))
                content.append(Paragraph(
                    " Method:{method}, &nbsp; &nbsp;API:{api}".format(
                        api=Utility.disable_sign_escape(pageItem['api']), method=str.upper(pageItem['method'])
                    ), normal_style))
                analysisTable = [['Generate params', 'Path', 'Sink', 'Source', 'Number of sensitive\nprivacy fields in Source']]
                for analysisItem in pageItem['taint_analysis']:
                    analysisTable.append([Utility.disable_sign_escape(analysisItem['gen_params']),
                                          Utility.disable_sign_escape(analysisItem['path']),
                                          Utility.disable_sign_escape(analysisItem['sink']),
                                          Utility.handler_source(analysisItem['source']),
                                          str(analysisItem['source_sensitives_nums'])])
                content.append(handler_table_data(analysisTable, normal_style))
                content.append(PageBreak())
    pdf.build(content)
    encode_file = base64.urlsafe_b64encode(file.encode('utf-8')).decode('utf-8')
    return encode_file