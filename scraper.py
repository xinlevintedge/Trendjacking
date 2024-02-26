from bs4 import BeautifulSoup
import requests
import pandas as pd
import pygsheets
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
import os

# YOUTUBE TRENDING VIDEOS  ----------------------------------------------------------------------------

# URL of the website to scrape
url = "https://yttrendz.com/youtube-trends/singapore"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, "html.parser")

# Find the elements containing ranks, topics, and YouTuber's names
rank_elements = soup.select(".feed-count span")
topic_elements = soup.select(".feed-title .videoPopup-open")
author_elements = soup.select(".feed-author")

# Extract text from elements
ranks = [rank.get_text(strip=True) for rank in rank_elements]
topics = [topic.get_text(strip=True) for topic in topic_elements]


# Extract authors and remove rows containing "Upload by:"
authors = []
for author in author_elements:
    author_text = author.get_text(strip=True)
    if "Upload by" not in author_text:
        authors.append(author_text)
 

# Combine data into a DataFrame
yt_data = pd.DataFrame({"Rank": ranks, "Topic": topics, "YouTuber": authors})

# Display the DataFrame
print(yt_data)
yt_data.to_excel("trends.xlsx", index=False)


# TWITTER HASHTAGS ----------------------------------------------------------------------------

# URL of the website to scrape
twitter_url = "https://twitter-trends.iamrohit.in/singapore"

# Send a GET request to the URL
response = requests.get(twitter_url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the elements containing Twitter ranks and topics
    rank_elements = soup.select("#copyData th:nth-child(1)")
    topic_elements = soup.select(".tweet")

    # Extract text from elements
    ranks = [rank.get_text(strip=True) for rank in rank_elements]
    topics = [topic.get_text(strip=True) for topic in topic_elements]

    # Combine data into a DataFrame
    twitter_data = pd.DataFrame({"Rank": ranks, "Hashtags/Topics": topics})

    # Display the first few rows of the data
    print(twitter_data.head(10))
else:
    print("Failed to retrieve the webpage")
    
# INSTAGRAM HASTAGS ----------------------------------------------------------------------------

insta_url = "https://displaypurposes.com/hashtags/rank/best/country/sg"

# Send a GET request to the URL
try:
    response = requests.get(insta_url)
    response.raise_for_status()  # Raise an exception for non-200 status codes
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the elements containing Twitter ranks and topics
    rank_elements = soup.select("td:nth-child(1)")
    hashtag_elements = soup.select(".font-bold.border-accent")

    # Extract text from elements
    ranks = [rank.get_text(strip=True) for rank in rank_elements]
    hashtag = [hashtag.get_text(strip=True) for hashtag in hashtag_elements]

    # Combine data into a DataFrame
    insta_data = pd.DataFrame({"Rank": ranks, "Hashtags": hashtag})

    # Display the first few rows of the data
    print(insta_data.head(10))
except requests.exceptions.RequestException as e:
    print(f"Failed to retrieve the webpage: {e}")


 # INSTAGRAM REELS ----------------------------------------------------------------------------
 
instareel_url = "https://slayingsocial.com/instagram-reels-trends/  "

# Send a GET request to the URL
try:
    response = requests.get(insta_url)
    response.raise_for_status()  # Raise an exception for non-200 status codes
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the elements containing insta reels
    rank_elements = soup.select("p+ p")
    hashtag_elements = soup.select(".font-bold.border-accent")

    # Extract text from elements
    ranks = [rank.get_text(strip=True) for rank in rank_elements]
    hashtag = [hashtag.get_text(strip=True) for hashtag in hashtag_elements]

    # Combine data into a DataFrame
    insta_data = pd.DataFrame({"Rank": ranks, "Hashtags": hashtag})

    # Display the first few rows of the data
    print(insta_data.head(10))
except requests.exceptions.RequestException as e:
    print(f"Failed to retrieve the webpage: {e}")
    
    
# GOOGLE TRENDS ----------------------------------------------------------------------------
from pytrends.request import TrendReq
import pandas as pd
from datetime import date

# Set up pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# Get trending searches
google_data = pytrends.trending_searches(pn='singapore')

# Get the current date
current_date = date.today().strftime("%Y-%m-%d")

# Add the date as a new column to the datafram
google_data['Date'] = current_date

# Show only the first 10 rows of the dataframe
print(google_data)


# TIKTOK TRENDS ----------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


# URL of the website to scrape
url = "https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en?rid=9oca3166fgo&region=SG&period=7&orderBy=popular"

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set path to chromedriver as per GitHub Actions setup
# No need to specify a path explicitly, GitHub Actions will have chromedriver in PATH
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

# Click the "View More" button
for _ in range(20):
    view_more_button = driver.find_element(By.XPATH, "//div[contains(@class, 'CcButton_common__aFDas') and contains(@class, 'CcButton_secondary__N1HnA') and contains(@class, 'index-mobile_common__E86XM')]")
    view_more_button.click()  # Click the "View More" button
    # Wait for the page to load the newly loaded content
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='LoadingIndicator_text__29MyQ']")))


# Find all the ranking elements
rank_elements = driver.find_elements(By.CLASS_NAME, "RankingStatus_rankingIndex__ZMDrH")

# Find all the hashtag elements
hashtag_elements = driver.find_elements(By.CLASS_NAME, "CardPc_titleText__RYOWo")

# Create a list to store the data
tikok = []

# Iterate through all elements and store ranks and hashtags in the list
for rank, hashtag in zip(rank_elements, hashtag_elements):
    tikok.append({"Rank": rank.text.strip(), "Hashtag": hashtag.text.strip()})


tikok_data = pd.DataFrame(tikok)
print(tikok_data)

# Close the browser
driver.quit()

    
# UPDATING TO GOOGLE SHEETS ----------------------------------------------------------------------------

# Load Google Sheets credentials from the secret
secret_value = os.environ.get('GOOGLE_SHEETS_CREDS')
creds_dict = json.loads(secret_value)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict)

# Authorize the clientsheet
client = gspread.authorize(creds)

# Open the Google Sheet using its URL
sh = client.open_by_url('https://docs.google.com/spreadsheets/d/1EgrVNuuFs_XxHskJ5LoUfWTJKCsoxrqxlssTv2ChXIk/edit?usp=sharing')

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
update_sheet('YouTube', yt_data, include_header=True)
update_sheet('Twitter', twitter_data, include_header=True)
update_sheet('Instagram', insta_data, include_header=True)
update_sheet('Google Trends', google_data, include_header=True)
update_sheet('TikTok', tikok_data, include_header=True)
