1.Setup Instructions 
  1. Install Required Tools: 
    o Install Google Chrome and ChromeDriver. 
    o Place the chromedriver.exe in the same directory as the script or specify its path. 
  2. Install Python Dependencies: 
    o Use the command: 
        pip install selenium beautifulsoup4 
  3. Create a Data Directory: 
    o Ensure the data folder exists in the script's directory. The script will store HTML files 
      here. 
  4. Run the Script: 
    o Execute the script using: 
        python main.py 
2.Functionality 
  1. Web Scraping: 
    o The script uses Selenium to automate interaction with Amazon's bestseller pages 
      and saves raw HTML files. 
  2. Data Parsing: 
    o BeautifulSoup extracts product details such as title, URL, image, rating, and price 
      from the saved HTML. 
  3. Data Storage: 
     o Extracted data is saved in structured CSV files, categorized by product type. 
  4. Error Handling: 
     o Includes try-finally blocks to handle errors gracefully and ensure the driver is closed. 
3.Usage Guidelines 
  • Dynamic Adjustments: 
    o Change the categories list to target different categories. 
    o Adjust the page range in the for loop to scrape more pages. 
  • Output Validation: 
    o Verify saved HTML files in the data directory. 
    o Open generated CSV files in Excel or any viewer to inspect the extracted data.
