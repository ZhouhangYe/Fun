import requests
import os
import pandas as pd
import time
import re
import logging
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(filename='error_log.txt', level=logging.ERROR)

BASE_URL = "https://www.sec.gov"
EXCEL_PATH = 'C:/Users/bichi/Downloads/Book2.xlsx'
DOWNLOAD_FOLDER = "E:/sec_table"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def sanitize_filename(filename):
    return re.sub(r'[\\/:"*?<>|]', '_', filename)

def fetch_directory_page(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"Error: URL not found {url}")
        elif response.status_code >= 500:
            print(f"Server error encountered for URL: {url}. Status code: {response.status_code}")
        else:
            print(f"Error fetching directory page for URL: {url}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed for URL: {url}. Error: {e}")
    return None

def download_file(url, folder, filename):
    filename = sanitize_filename(filename)  # Sanitize filename
    time.sleep(0.8)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        filepath = os.path.join(folder, filename)
        with open(filepath, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Error downloading {url}. Status code: {response.status_code}")

def parse_filing_summary(url, cik, year):
    try:
        content = requests.get(url, headers=headers).content
        soup = BeautifulSoup(content, 'lxml')
        reports = soup.find('myreports')
        if not reports:
            logging.error(f"No reports found for URL: {url}, CIK: {cik}, Year: {year}")
            return

        base_url = url.replace('FilingSummary.xml', '')
        for report in reports.find_all('report')[:-1]:
            file_url = None
            if report.htmlfilename and report.htmlfilename.text.startswith('R'):
                print('-'*100)
                file_url = base_url + report.htmlfilename.text
                print(file_url)
                print(report.longname.text)
                print(report.shortname.text)
            if report.menucategory:
                print(report.menucategory.text)
                print(report.position.text)

            download_path = os.path.join(DOWNLOAD_FOLDER, str(cik), year)
            if not os.path.exists(download_path):
                os.makedirs(download_path)

            if file_url:
                sanitized_filename = sanitize_filename(report.shortname.text + ".htm")
                download_file(file_url, download_path, sanitized_filename)
    except Exception as e:
        logging.error(f"Error parsing filing summary for URL: {url}, CIK: {cik}, Year: {year}. Error: {e}")

try:
    df = pd.read_excel(EXCEL_PATH)
except FileNotFoundError:
    print(f"Error: File {EXCEL_PATH} does not exist")
    exit()
except Exception as e:
    print(f"Error reading Excel file {EXCEL_PATH}: {e}")
    exit()

cik_list = df['CIK'].tolist()

for cik in cik_list:
    print(f"Processing CIK: {cik}...")
    cik_url = f"{BASE_URL}/Archives/edgar/data/{cik}/index.json"
    cik_directory_content = fetch_directory_page(cik_url)
    if cik_directory_content:
        for folder in cik_directory_content['directory']['item']:
            folder_name = folder['name']
            folder_url = f"{BASE_URL}/Archives/edgar/data/{cik}/{folder_name}/index.json"
            folder_directory_content = fetch_directory_page(folder_url)
            if folder_directory_content and len(folder_directory_content['directory']['item']) > 15:
                for file in folder_directory_content['directory']['item']:
                    if file['name'] == 'FilingSummary.xml':
                        year = folder['last-modified'].split('-')[0]
                        filing_summary_url = f"{BASE_URL}/Archives/edgar/data/{cik}/{folder_name}/{file['name']}"
                        parse_filing_summary(filing_summary_url, cik, year)
                        break
    print(f"Finished processing CIK: {cik}\n\n")
