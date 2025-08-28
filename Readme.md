# WAScope: Detecting Privacy Data Leakage with Web Application-Specific API Confusion
<a href="https://doi.org/10.1016/j.aej.2025.08.006"><img src="https://img.shields.io/badge/DOI-10.1016/j.aej.2025.08.006-blue" target="_blank"></a>
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)


## Overview
WAScope is an open-source **dynamic analysis tool** tailored to detect privacy data leakage in web applications, with a focus on **web application-specific APIs**—a critical but understudied attack surface. Existing tools mostly target system APIs for data exfiltration detection, while WAScope fills the gap by combining **API confusion techniques** and a **customized privacy dictionary** to identify unauthorized access to sensitive user data (e.g., PII, financial records).

### Key Experimental Results
- Tested on 100 real-world web applications; identified 15,593 privacy-aware API data flows across 76 apps.
- Manually confirmed 2,757 APIs with sensitive data exposure due to improper access controls.
- Achieved a low false positive rate of 9%.
- Discovered 10 vulnerabilities officially recognized by the China National Vulnerability Database (CNVD).


## Prerequisites
Before using WAScope, ensure the following environments/tools are installed:
1. **Operating System**: Ubuntu 20.04+/Windows 10+/macOS 12+ (tested on Ubuntu 20.04 and Windows 11).
2. **Python Version**: 3.10+ (lower versions may cause dependency conflicts).
3. **Database**: MySQL 8.0+ (for storing intercepted requests and detection results).
4. **Proxy Tool**: MITMproxy 10.0+ (for HTTP/HTTPS traffic interception; included in `requirements.txt`).
5. **Browser**: Chrome/Edge/Firefox (for configuring proxy and testing web applications).


## Installation Guide
### 1. Clone the Repository
First, clone the WAScope repository to your local machine:
```bash
git clone https://github.com/jcifox/WAScope.git
cd WAScope
```

### 2. Install Python Dependencies
Install all required Python packages via `requirements.txt`:
```bash
# For pip (ensure pip is linked to Python 3.10+)
pip install -r requirements.txt

# If using a virtual environment (recommended to avoid dependency conflicts)
python -m venv wascope-venv
# Activate virtual environment (Linux/macOS)
source wascope-venv/bin/activate
# Activate virtual environment (Windows)
wascope-venv\Scripts\activate
# Install dependencies in virtual environment
pip install -r requirements.txt
```

### 3. Configure MySQL Database
WAScope uses MySQL to store intercepted requests and detection results. Follow these steps to set up the database:
1. Start your MySQL service (ensure it runs on the default port `3306`, or modify the port in `lib/DB.py`).
2. Create a database (e.g., named `wascope_db`):
   ```sql
   CREATE DATABASE IF NOT EXISTS wascope_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. Import the database schema from the `sql/` directory:
   ```bash
   # Replace <your-mysql-username> and <your-mysql-password> with your actual credentials
   mysql -u <your-mysql-username> -p wascope_db < sql/wascope_schema.sql
   ```
4. Update database configuration in `lib/DB.py` to match your MySQL setup:
   ```python
   # In lib/DB.py, modify the following lines
   DB_CONFIG = {
       "host": "localhost",    # Default: localhost; change if MySQL is remote
       "port": 3306,           # Default port; adjust if needed
       "user": "your-username",# Your MySQL username
       "password": "your-password", # Your MySQL password
       "db": "wascope_db"      # Database name (created in step 2)
   }
   ```

### 4. Configure Browser Proxy
To intercept web application traffic, configure your browser to use WAScope’s MITMproxy:
1. **Chrome/Edge**:
    - Open browser settings → Search for "Proxy" → Select "Open your computer’s proxy settings".
    - For Windows: Enable "Use a proxy server" → Set "Address" to `127.0.0.1` and "Port" to `8080`.
    - For Linux/macOS: Set "HTTP Proxy" and "HTTPS Proxy" to `127.0.0.1:8080`.
2. **Add Browser Launch Parameter** (to ignore MITMproxy certificate errors):
    - For Windows (Chrome): Create a shortcut → Right-click → "Properties" → Add ` --proxy-server=127.0.0.1:8080 --ignore-certificate-errors` to the end of the "Target" field.
    - For Linux (Chrome): Launch via terminal:
      ```bash
      google-chrome --proxy-server=127.0.0.1:8080 --ignore-certificate-errors
      ```
3. **Install MITMproxy CA Certificate** (optional but recommended for HTTPS):
    - Run `mitmdump` once to generate the CA certificate (stored in `~/.mitmproxy/` on Linux/macOS, or `C:\Users\<Your-User>\.mitmproxy\` on Windows).
    - Import the `mitmproxy-ca-cert.pem` file into your browser’s "Trusted Root Certification Authorities" (avoids HTTPS "unsafe" warnings).


## Usage Guide
WAScope has two core workflows: **traffic interception** (collect API data) and **request replay** (retest suspicious APIs). Below are the detailed commands and steps.

### 1. Traffic Interception (Main Workflow)
This step starts MITMproxy to intercept web application traffic, analyze APIs, and detect privacy leakage.  
**Command**:
```bash
# Clear terminal logs (optional) and start interception
clear && mitmdump -q -s ./Interception.py
```
- `-q`: Quiet mode (reduces redundant MITMproxy logs).
- `-s ./Interception.py`: Load WAScope’s core interception script (entry point for analysis).

**How to Use**:
1. Run the above command in the WAScope root directory.
2. Open the configured browser (with proxy settings) and access the target web application (e.g., `https://example.com`).
3. WAScope will automatically:
    - Intercept HTTP/HTTPS requests/responses.
    - Match APIs against the privacy dictionary (identify privacy-aware APIs).
    - Check for unauthorized access via API confusion.
    - Store results in the MySQL database and log to `mitmproxy/` directory.
4. To stop interception: Press `Ctrl + C` in the terminal.


### 2. Request Replay (Retest Suspicious APIs)
After interception, use this step to replay specific suspicious API requests (e.g., to verify leakage or retest after fixing vulnerabilities).  
**Command**:
```bash
# Clear logs (optional) and start replay; replace <target-host> with the web app's domain
clear && python ./Replay.py --host=<target-host>
```
- `--host=<target-host>`: Required parameter; specifies the target web application’s domain (e.g., `example.com`, `api.example.com`).
- **Optional Parameters** (add to the command if needed):
    - `--port=<port>`: Specify the target port (default: `443` for HTTPS, `80` for HTTP).
    - `--log=<log-path>`: Use a custom MITMproxy log file (default: uses the latest log in `mitmproxy/`).

**Example**:
```bash
# Replay APIs for the target host "test-app.com" (HTTPS, port 443)
clear && python ./Replay.py --host=test-app.com
```


### 3. View Detection Results
**Report Files**: After interception/replay, `ReportGenerator.py` auto-generates reports in `report_output/` .


## Troubleshooting
| Common Issue                                  | Solution                                                                 |
|-----------------------------------------------|--------------------------------------------------------------------------|
| "MITMproxy error: No module named 'xxx'"      | Ensure you installed dependencies via `pip install -r requirements.txt`; if using a virtual environment, confirm it’s activated. |
| "MySQL connection failed"                     | Check if MySQL is running; verify `lib/DB.py` has the correct username/password/host. |
| Browser cannot access the internet            | Confirm proxy settings (address: `127.0.0.1`, port: `8080`); ensure WAScope’s interception command is running. |
| HTTPS "unsafe" warnings                       | Install the MITMproxy CA certificate in your browser (see "Install MITMproxy CA Certificate" in Step 4 of Installation). |


## Citation
If you use WAScope in your research or projects, please cite our paper:
```bibtex
@article{NIE20251145,
title = {WAScope: Detecting privacy data leakage with web application-specific API confusion},
journal = {Alexandria Engineering Journal},
volume = {128},
pages = {1145-1158},
year = {2025},
issn = {1110-0168},
doi = {https://doi.org/10.1016/j.aej.2025.08.006},
url = {https://www.sciencedirect.com/science/article/pii/S1110016825008774},
author = {Yu Nie and Jianming Fu and Xinghang Lv and Chao Li and Shixiong Yang and Guojun Peng},
keywords = {Web application-specific API, Privacy leakage, API confusion, Defense},
abstract = {The number of web applications deployed on the internet has exceeded one billion, accumulating vast amounts of user privacy data. The compromise of such data may lead to severe consequences. While existing research has primarily focused on data exfiltration through system APIs, the security risks posed by application-specific APIs have been largely overlooked. These APIs directly manage the collection, processing, and transmission of sensitive user data, making them critical attack surfaces. This study systematically investigates privacy data leakage caused by unauthorized access through web application-specific APIs. We presented WAScope (Web Application-specific API Scope), a dynamic analysis tool that detects privacy leakage by combining API confusion techniques with a customized privacy dictionary. We conducted experiments on 100 real-world web applications using WAScope. The tool identified 15,593 privacy-aware API data flows across 76 applications, among which 2,757 APIs were manually confirmed to expose sensitive data due to improper access controls. Manual validation further validated the findings, revealing a 9% false positive rate. We reported these vulnerabilities to the China National Vulnerability Database (CNVD), receiving 10 official CNVD-IDs that demonstrate the effectiveness of WAScope.}
}
```
or 
``` GB/T 7714-2015
[1] NIE Y, FU J, LV X, et al. WAScope: Detecting privacy data leakage with web application-specific API confusion[J/OL]. Alexandria Engineering Journal, 2025, 128: 1145-1158. DOI:https://doi.org/10.1016/j.aej.2025.08.006.
```

## Contact & Support
For bug reports, feature requests, or technical questions:
1. Open an issue on GitHub (preferred): [https://github.com/jcifox/WAScope/issues](https://github.com/jcifox/WAScope/issues).