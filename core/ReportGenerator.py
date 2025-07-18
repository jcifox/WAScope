import base64

from lib import Utils as Utility
from core.ControllerRequestRecord import ControllerRequestRecord

html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Host:{host} - Analysis Report</title>
    <meta content="text/html; charset=utf-8" http-equiv="content-type" />
    <style>
    body{{font-size:14px;font-family:"Times New Roman","SimSun";}}
    th{{background:rgb(245,245,220);font-size:14px;font-weight:bold;}}
    td{{text-align:center;white-space:normal;word-break:break-all;vertical-align:text-top;}}
    hr{{margin:20px 0;border:1px dashed #000;width:1200px;margin:10px auto;}}
    h1{{font-size:30px;font-family:"Times";font-weight:bold;text-align:center;}}
    .t1{{line-height:20px;width:1200px;margin:10px auto;}}
    </style>
</head>
<body>
    <h1>Host:{host} - Analysis Report</h1>
    {reportContents}
</body>
</html>
"""


def create_report(_host):
    path = './report_output/'
    file_path = _host + '_' + '_report.html'

    content = ''
    CtrlReqRecd = ControllerRequestRecord()
    rs = CtrlReqRecd.query_record_second_analysis(_host=_host)
    for item in rs:
        for pageItem in item['page']:
            riskFlag = len(pageItem['taint_analysis']) > 0
            if riskFlag:
                content = content + "<div class=\"t1\">Referer:【{referer}】".format(referer=Utility.disable_sign_escape(item['referer']))
                content = content + "<br>Method:【{method}】, &nbsp; &nbsp;API:【{api}】</div>".format(
                    api=Utility.disable_sign_escape(pageItem['api']), method=str.upper(pageItem['method'])
                )
                content = content + ("<table width=1200 align=center border=1 cellspacing=0 cellpadding=0>"
                                     "<tr>"
                                     "<th width=80>Generate params</td>"
                                     "<th width=120>Path</td>"
                                     "<th width=200>Sink</td>"
                                     "<th width=635>Source</td>"
                                     "<th width=165>Number of sensitive<br>privacy fields in Source</td>"
                                     "</tr>")
                for analysisItem in pageItem['taint_analysis']:
                    content = content + "<tr>"
                    content = content + "<td>" + Utility.disable_sign_escape(analysisItem['gen_params']) + "</td>"
                    content = content + "<td>" + Utility.disable_sign_escape(analysisItem['path']) + "</td>"
                    content = content + "<td>" + Utility.disable_sign_escape(analysisItem['sink']) + "</td>"
                    content = content + "<td>" + Utility.disable_sign_escape(analysisItem['source']) + "</td>"
                    content = content + "<td>" + str(analysisItem['source_sensitives_nums']) + "</td>"
                    content = content + "</tr>"
                content = content + "</table>"
                content = content + "<hr/>"

    with open(path + file_path, "w", encoding="utf-8") as f:
        f.write(html_content.format(reportContents=content, host=_host))
    encode_file = base64.urlsafe_b64encode(file_path.encode('utf-8')).decode('utf-8')
    return encode_file
