# SEC Filing Scraper

## Overview
This script is designed to automate the process of downloading and parsing SEC filings using Python. It extracts financial report data from the SEC EDGAR database, downloads relevant filing summary files, and saves them locally.

## Features
- Fetches directory pages for given CIK numbers
- Downloads `FilingSummary.xml` files for each CIK
- Extracts and processes reports from the filings
- Saves downloaded files in a structured directory
- Handles exceptions and logging for errors

## Requirements
### Dependencies
The script requires the following Python libraries:

- `requests` - For handling HTTP requests
- `os` - For managing file operations
- `pandas` - For handling Excel files
- `time` - For managing request delays
- `re` - For sanitizing filenames
- `logging` - For error logging
- `beautifulsoup4` - For parsing HTML/XML data

You can install the required dependencies using:
```sh
pip install requests pandas beautifulsoup4 lxml
```

## Usage

1. Ensure you have an Excel file containing a column named `CIK` with the CIK numbers you want to process.
2. Update the `EXCEL_PATH` variable with the path to your Excel file.
3. Update the `DOWNLOAD_FOLDER` variable to set where files should be saved.
4. Run the script using:
```sh
python script.py
```

## Script Breakdown
### Functions:
- **`sanitize_filename(filename)`**: Cleans filenames to remove invalid characters.
- **`fetch_directory_page(url)`**: Fetches directory listings from SEC URLs.
- **`download_file(url, folder, filename)`**: Downloads a file and saves it locally.
- **`parse_filing_summary(url, cik, year)`**: Extracts and downloads relevant reports from the filing summary.

### Error Handling:
- Logs errors to `error_log.txt`.
- Skips over non-responsive URLs or missing files.

## File Structure
```
SEC_Filing_Scraper/
│-- script.py
│-- README.md
│-- error_log.txt
│-- data/
│   ├── Book2.xlsx (input file with CIKs)
│   ├── E:/sec_table/ (downloaded filings stored here)
```

## Notes
- Ensure you have a stable internet connection, as the script sends multiple requests to the SEC website.
- Some filings may not contain `FilingSummary.xml`, which can cause them to be skipped.
- If the SEC server returns too many errors, consider slowing down requests by increasing the `time.sleep()` value.

## License
This project is licensed under the MIT License.
