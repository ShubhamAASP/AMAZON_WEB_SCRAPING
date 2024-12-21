from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import  os
from bs4 import BeautifulSoup

# # Initialize the driver
# service = Service('chromedriver.exe')  # Replace with the path to your ChromeDriver
# driver = webdriver.Chrome(service=service)

# # Open the Amazon Login Page
# driver.get('https://www.amazon.in/ap/signin?openid.pape.max_auth_age=900&openid.return_to=https%3A%2F%2Fwww.amazon.in%2Fgp%2Fyourstore%2Fhome%3Fpath%3D%252Fgp%252Fyourstore%252Fhome%26signIn%3D1%26useRedirectOnSuccess%3D1%26action%3Dsign-out%26ref_%3Dnav_AccountFlyout_signout&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0')

# # Add categories you want to scrape
# categories = [
    # "electronics",
    # "computers",
    # "kitchen",
    # "apparel",
    # "books",
    # "automotive",
    # "grocery",
    # "hpc",
    # "sports",
    # "garden",
    # "jewelry",
    # "beauty",
    # "luggage"
# ]

# file = 0

# # Step 1: Locate and click the "All" section (hamburger menu)
# all_button = WebDriverWait(driver, 15).until(
#     EC.element_to_be_clickable((By.ID, 'nav-hamburger-menu'))
# )
# all_button.click()
# print("Clicked on the 'All' section successfully.")

# # Step 2: Loop through each category and scrape items
# for category in categories:
#     print(f"Scraping {category}...")

#     # Open Bestsellers page for the category
#     for i in range(1, 3):  # Scrape first 2 pages (you can change this to more pages)
#         driver.get(f"https://www.amazon.in/gp/bestsellers/{category}/ref=zg_bs_pg_{i}{category}?ie=UTF8&pg={i}")

#         # Wait for the page to load and get elements
#         elems = driver.find_elements(By.CLASS_NAME, "p13n-sc-uncoverable-faceout")
#         print(f"{len(elems)} items found for {category} on page {i}")

#         for elem in elems:
#             d = elem.get_attribute("outerHTML")
#             with open(f"data/{category}_{file}.html", "w", encoding="utf-8") as f:
#                 f.write(d)
#                 file += 1
#                 print(elem.text)

#         time.sleep(6)

# driver.close()



# Function to extract details from a product block
def extract_product_details(elem):
    # Extract the product title
    title = elem.find('div', class_='_cDEzb_p13n-sc-css-line-clamp-3_g3dy1').get_text(strip=True) if elem.find('div', class_='_cDEzb_p13n-sc-css-line-clamp-3_g3dy1') else ''
    
    # Extract the product URL
    product_url = elem.find('a', class_='a-link-normal aok-block')['href'] if elem.find('a', class_='a-link-normal aok-block') else ''
    
    # Extract the image URL
    image_url = elem.find('img', class_='a-dynamic-image p13n-sc-dynamic-image p13n-product-image')['src'] if elem.find('img', class_='a-dynamic-image p13n-sc-dynamic-image p13n-product-image') else ''
    
    # Extract the rating (if available)
    rating = ''
    rating_elem = elem.find('a', class_='a-link-normal')
    if rating_elem:
        rating_icon = rating_elem.find('i', class_='a-icon-star-small')
        if rating_icon:
            rating = rating_icon['title'].split(',')[0]
    
    # Extract the number of reviews (if available)
    num_reviews = ''
    reviews_elem = elem.find('a', class_='a-link-normal')
    if reviews_elem:
        num_reviews_elem = reviews_elem.find('span', {'aria-hidden': 'true'})
        if num_reviews_elem:
            num_reviews = num_reviews_elem.get_text(strip=True)
    
    # Extract the price (if available)
    price = ''
    price_elem = elem.find('span', class_='_cDEzb_p13n-sc-price_3mJ9Z')
    if price_elem:
        price = price_elem.get_text(strip=True)
    
    # Return the product details in a dictionary
    return {
        'Title': title,
        'Product URL': 'https://www.amazon.in' + product_url if product_url else '',
        'Image URL': image_url,
        'Rating': rating,
        'Number of Reviews': num_reviews,
        'Price': price
    }



# Function to save data into a CSV file
def save_to_csv(data, category):
    with open(f'{category}.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# Directory containing the HTML files
html_directory = 'data'

# Categories to process (you can modify based on your requirements)
categories = ["electronics",
    "computers",
    "kitchen",
    "apparel",
    "books",
    "automotive",
    "grocery",
    "hpc",
    "sports",
    "garden",
    "jewelry",
    "beauty",
    "luggage"]

# Initialize a dictionary to hold data for each category
category_data = {category: [] for category in categories}

# Iterate over each HTML file in the directory
for filename in os.listdir(html_directory):
    if filename.endswith('.html'):
        # Extract category from the filename (e.g., electronics_0.html -> electronics)
        category = filename.split('_')[0]
        if category in categories:
            # Read and parse the HTML content
            with open(os.path.join(html_directory, filename), 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')

            # Find all product elements in the HTML file
            product_elems = soup.find_all('div', class_='p13n-sc-uncoverable-faceout')

            # Extract product details and append to the corresponding category
            for elem in product_elems:
                product_details = extract_product_details(elem)
                category_data[category].append(product_details)

# Save the extracted data for each category to CSV
for category, data in category_data.items():
    if data:  # Only save CSV if there are data entries
        save_to_csv(data, category)
        print(f"Saved {len(data)} products to {category}.csv")

