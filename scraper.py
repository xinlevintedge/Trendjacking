from bs4 import BeautifulSoup
import requests
import pandas as pd
import pygsheets
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
import os
import re 
import datetime
from datetime import date, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

secret_value = r"""
{
  "type": "service_account",
  "project_id": "master-tangent-415102",
  "private_key_id": "3c7bd110b6b3a648e6e40b05885d3fc46a641225",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDDBWmKXB9IEZH9\n5VHMbUETuBmB1wmY8fGmO+MfdqB3AapGn7Nzy8ofmrJ9+Yjb3UM+9sHmLA1ZIK33\nZZYp6QcRbGKO/YVUlJZgkSbaxBboPc6XWeYengyzjHsK65TWTSQ7t2CuBbuqwvSN\niKBFSmsr23WWr766LxYxlg+zUpgDClAdue4Pz0YR/XejmMdtO2bs2Vl3vyU2eiXc\nIfa1C76K9EOFVZXjy3ZO9NccHotIGgB+fimyPfI9TvrozhrVBZMbHMBmJwFartw8\niMpRI/THt67oaWBCO+kQjq/CI+35NHyBQg3ZZIxY38d1TOA8GN+7LEyqpQsI7rXY\nsWpUspSvAgMBAAECggEAM1VA3xD5kOxDC9wpSFB3wTuDx0f1eEMzEskPsw/0E+8l\nxVozD6dUKDZ9hihBLHJUyYWFK1NsHgo6kHS2boiuehkX5kB4MHe+D2QVoJ7d0rq2\nHuOkbWm3uSkgmBLDhhcfEvLlaVkL+VpAqeKNIUAB7rThAk13PCW5x0qTDmYOqjm+\na2bbIGXvBoWsge6jKnUc7iPelP4Dyqhi6z5VmuzLs7kVlgxVOETt06keaDgeuHoV\nUgKVLtm6CB285pT5jPdb9bL7OyZHpfCyHrt2fsDAJ8zJ5xy5JuJMvu2MSRiF7IMN\nRqJFdoHb95cVCpj6pjcSpHxwnCe+glJ9pUhSAvA61QKBgQDrfe+oYpFxSheTaacw\nbFNNiYBGNkjesljQx0HRqc3DZkfZko5JE8ewIHS7VJBWc0K7eMmriaMXMDHIUtYb\n+qRAmgBnlO6bzGrSKq8VpRqnNAR/H3QKh+7n8sLng8Cq2Xtq1pyT61vC+/7Zd9LM\niGNDRsLPza2pJOQwNpSBgbkJowKBgQDUATgS8wbEl0V0RzGdwSCANjMj97/iw/hK\ncHFlGPpnjsTWDo97dgd/YqgtCJl2qS8gVgdfRvoDMFF8kvVBa16o2dN16NDjwMqY\nFWdFHYuE7/grB7r1DMxDnoASb1VZac4o9n5iyjZ8uLsjIzFbR9NeJcIPTAKKLGMH\ndU+fDqxRhQKBgFgMpmcXM7pgMaB0iIaaeisrlkKqWWSq2np1hi6WhtDglUzMd1br\nhmZcPEkuvSkVv4XJC96Pf+NTqcl074lWlcNx0WTpUq3+KJKcUwqMyQJreKLvZ7vo\nR3OCWU2m/Yrj9jlkNPc5sP2eqxM0siS3eiXVd1GrXZs4p/k+7xfdIQpxAoGBALz5\nwTQS8Wt3s+9sLqwCJKhkp71d7+uA5+fixxFo7Hw25PoxzHAuy4wfMu3BhpohQOLA\nDJ4/NEh3X4t9q6R+wsgcMsQdnWYGyhA6s+0F4wHCriIdJ+ebWtDDjkHgf+HN0Hjv\nD8WbnmoaeKVfj3VgVubLHWppRLJJ0pQpW6naeHvJAoGBAKyQsYndVldf/PJrAMjy\n6h9T6KQM3nVDCex2H0J1pAR1Jil7fw8nC20MTKfYggEWsl+Qcnb2fxjItuWfuKOo\n6F90X1Lhpnib9powkz3RlJ6G7lJ42cEAUpEZJ3tSujfI02EnWH6uUibgWWzQK72W\nxzM+60V+JxhqiBvmTil3mIgK\n-----END PRIVATE KEY-----\n",
  "client_email": "xin-550@master-tangent-415102.iam.gserviceaccount.com",
  "client_id": "115346889995173445539"
}
"""

creds_dict = json.loads(secret_value)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict)

# Authorize the clientsheet
client = gspread.authorize(creds)

# Open the Google Sheet using its URL
sh = client.open_by_url('https://docs.google.com/spreadsheets/d/1EgrVNuuFs_XxHskJ5LoUfWTJKCsoxrqxlssTv2ChXIk/edit?usp=sharing')
# Get the previos date and format it as "YYYY-MM-DD"
previous_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

# URL of the website to scrape
url = "https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en"

# Set up Chrome webdriver 
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")  # Required for running as root in Docker
chrome_options.add_argument("--disable-dev-shm-usage")  # Required for running in Docker
chrome_options.add_argument("--start-maximized")  # Maximize the window (optional)
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

while True:
    try:
        # Attempt to find the "View More" button
        view_more_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="ccContentContainer"]/div[3]/div/div[2]/div/div[1]/div'))
        )
        # Click the "View More" button if it is visible
        view_more_button.click()
        # Wait for the page to load the newly loaded content
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, "//div[@class='LoadingIndicator_text__29MyQ']"))
        )
    except Exception as e:
        break  # Exit the loop if the button is not found or any error occurs

# After clicking the "View More" button, wait for the page to load completely
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "CardPc_itemValue__XGDmG"))
)

# Find all the  elements
rank_elements = driver.find_elements(By.CLASS_NAME, "index-mobile_rankingIndex__9mXja")
hashtag_elements = driver.find_elements(By.CLASS_NAME, "CardPc_titleText__RYOWo")
rankchange_elements = driver.find_elements(By.CLASS_NAME, "index-mobile_rankingvalue__LMuXc")
postview_elements = driver.find_elements(By.CLASS_NAME, "CardPc_itemValue__XGDmG")
# Collect data into lists
ranks = [rank.text.strip() for rank in rank_elements]
hashtags = [hashtag.text.strip() for hashtag in hashtag_elements]
postsviews = [postview.text.strip() for postview in postview_elements]
posts = postsviews[0::2]  # Get every other element, starting from the first
views = postsviews[1::2]  # Get every other element, starting from the second


rankchange = []
# Loop through each element to check its content
for element in rankchange_elements:
    try:
        text = element.text.strip()
        if text and text.isdigit():
            arrow_up_element = element.find_elements(By.XPATH, ".//span[@class='i-icon i-icon-arrow-up']")
            arrow_down_element = element.find_elements(By.XPATH, ".//span[@class='i-icon i-icon-arrow-down']")
            if arrow_up_element:
                rankchange.append("+" + text)  # Append "+" if the rank is rising
            elif arrow_down_element:
                rankchange.append("-" + text)  # Append "-" if the rank is falling
            else:
                rankchange.append(text)
        else:
            src = element.get_attribute('src')
            if src:
                rankchange.append("NEW")  # Assuming images are indicators for "NEW".
            else:
                rankchange.append("-")
    except Exception as e:
        rankchange.append("-")

print(len(ranks))
print(len(rankchange))
print(len(hashtags))
print(len(posts))
print(len(views))
# Create DataFrame
tiktok_hashtag = pd.DataFrame({"Rank": ranks, "Hashtag": hashtags, "Rank Change": rankchange,"Posts": posts,"Views": views})
tiktok_hashtag['Date'] = previous_date
driver.quit()


# UPDATING TO GOOGLE SHEETS ----------------------------------------------------------------------------

# Load Google Sheets credentials from the secret
#secret_value = os.environ.get('GOOGLE_SHEETS_CREDS')

# Function to update or create a worksheet and write data
def update_sheet(worksheet_title, df, include_header=False):
    try:
        # Try to open the worksheet
        wks = sh.worksheet(worksheet_title)
    except gspread.exceptions.WorksheetNotFound:
        # If not found, create a new worksheet
        wks = sh.add_worksheet(worksheet_title, rows=100, cols=30)
    
    # Clear the existing contents of the worksheet
    wks.clear()
    
    # Convert DataFrame to a list of lists
    data = df.values.tolist()
    
    # Write the data to the worksheet starting from cell A1
    if include_header:
        header = df.columns.tolist()
        wks.update('A1', [header] + data)
    else:
        wks.update('A1', data)

# Update Google Sheets with the collected data
#update_sheet('YouTube', yt_data, include_header=True)
#update_sheet('Twitter', twitter_data, include_header=True)
#update_sheet('Instagram Reels', instareel_data, include_header=True)
#update_sheet('Google Trends', google_new, include_header=True)
#update_sheet('TikTok Trends', tiktok_data, include_header=True)
update_sheet('TikTok Hashtags', tiktok_hashtag, include_header=True)
