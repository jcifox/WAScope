# WAScoop Core Module

+ WAScope: Detecting Privacy Data Leakage with Web Application-Specific API Confusion

## Python dependency

`/requirments.txt`

`pip install -r requirments.txt`

## Browser configuration

`--proxy-server=127.0.0.1:8080 --ignore-certificate-errors`

## Directory

### core

> Analyzer: Analyzer.py
>
> Config: Config.py
>
> Controller: ControllerRequestRecord.py
>
> Filter: Filter.py
>
> ReportGenerator: ReportGenerator.py
>
> RequestConstructor: RequestConstructor.py

### lib

> MySQL Database Config:DB.py
>
> Source Download: Download.py
>
> Json 2 excel: Json2xlsx.py
>
> Tool lib: utils.py

### Other directory

> MITM log directory: mitmproxy
>
> Report output directory: report_output
>
> Sql files directory: sql
>
> Static files directory: static
>
> Test code files directory: test

### Root directory

> Main file: Interception.py
>
> Replay file: Replay.py
>
> Web API: Web_API.py

## Commands

### init run (Interception the request)

`clear && mitmdump -q -s .\Interception.py`

### replay

`clear && python .\Replay.py --host=xxx`