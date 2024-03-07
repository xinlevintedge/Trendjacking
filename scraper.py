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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Path to your chromedriver executable
CHROMEDRIVER_PATH = "C:\\Users\\XINLE\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"

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
        break  # Exit the loop if the button is not found or any error occur
    
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

# Create DataFrame
tiktok_hashtag = pd.DataFrame({"Rank": ranks, "Hashtag": hashtags, "Rank Change": rankchange,"Posts": posts,"Views": views})
tiktok_hashtag['Date'] = previous_date
driver.quit()

'''# YOUTUBE TRENDING VIDEOS  ----------------------------------------------------------------------------

url = "https://yttrendz.com/youtube-trends/singapore"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find the elements containing ranks, topics, and YouTuber's names
rank_elements = soup.select(".feed-count span")
topic_elements = soup.select(".feed-title .videoPopup-open")
YouTuber_elements = soup.select(".feed-author")
view_elements = soup.select("li:nth-child(1) .feed-view-figure")
like_elements = soup.select("li:nth-child(2) .feed-view-figure")
comment_elements = soup.select("li~ li+ li .feed-view-figure")


# Extract text from elements
ranks = [rank.get_text(strip=True) for rank in rank_elements]
topics = [topic.get_text(strip=True) for topic in topic_elements]
views = [view.get_text(strip=True) for view in view_elements]
likes = [like.get_text(strip=True) for like in like_elements]
comments = [comment.get_text(strip=True) for comment in comment_elements]

# Extract authors and remove rows containing "Upload by:"
YouTuber_list = []
for YouTuber in YouTuber_elements:
    YouTuber_text = YouTuber.get_text(strip=True)
    if "Upload by" not in YouTuber_text:
        YouTuber_list.append(YouTuber_text)
 
worksheet = sh.worksheet('YouTube')
old_trends = worksheet.get_all_records()
rank_change = []
# Iterate through the old trends data
for i, new_topic in enumerate(topics):
    new_YouTuber = YouTuber_list[i]
    found_match = False  # Flag to track if a match is found
    
    # Iterate through the old trends data
    for old_trend_row in old_trends:
        old_topic = old_trend_row['Topic']
        old_YouTuber = old_trend_row['YouTuber']
        old_rank = old_trend_row['Rank']
        
        # Check if the new trend matches any old trend
        if old_topic == new_topic and old_YouTuber == new_YouTuber:
            # Calculate rank change
            rank_change_val = int(old_rank) - int(ranks[i])
            if rank_change_val > 0:
                rank_change_str = "+" + str(rank_change_val)
            else:
                rank_change_str = str(rank_change_val) if rank_change_val != 0 else '-'
            rank_change.append(rank_change_str)
            found_match = True  # Set the flag to True to indicate a match is found
            break
        
    # If no match is found for the new trend in the old trends, label rank change as "NEW"
    if not found_match:
        rank_change.append('NEW')

# Combine data into a DataFrame
yt_data = pd.DataFrame({"Rank": ranks, "Topic": topics, "YouTuber": YouTuber_list, "Views": views,"Likes": likes,"Comments": comments, "Rank Change": rank_change})
yt_data['Date'] = previous_date

# TWITTER HASHTAGS ----------------------------------------------------------------------------

twitter_url = "https://twitter-trends.iamrohit.in/singapore"

# Send a GET request to the URL
response = requests.get(twitter_url)
soup = BeautifulSoup(response.content, "html.parser")

# Find the elements containing Twitter ranks and topics
rank_elements = soup.select("#copyData th:nth-child(1)")
topic_elements = soup.select(".tweet")
tweet_volume_elements = soup.select("#copyData .sml")

# Extract text from elements
ranks = [rank.get_text(strip=True).replace('.', '') for rank in rank_elements]
topics = [topic.get_text(strip=True) for topic in topic_elements]
tweet_volume = [tweet_volume.get_text(strip=True) for tweet_volume in tweet_volume_elements]

# Read data from the Google Sheet into a DataFrame
worksheet = sh.worksheet('Twitter')
twitter_sheet_data = worksheet.get_all_values()
twitter_sheet_df = pd.DataFrame(twitter_sheet_data[1:], columns=twitter_sheet_data[0])  # assuming the first row contains headers

# Initialize lists to store rank change and volume change
rank_change = []
volume_change = []

def convert_volume(volume_str):
    if volume_str == 'Under 10k':
        return 10
    elif 'k' in volume_str:
        return float(volume_str.replace('k', '')) 
    else:
        return float(volume_str)

# Iterate through the new trends
for topic, rank, volume in zip(topics, ranks, tweet_volume):
    # Remove dots from rank if present and convert to integer
    rank = int(rank.replace('.', ''))
    
    # Convert the new volume string to a numeric value
    volume_numeric = convert_volume(volume)

    # Check if the topic exists in the old trends
    if topic in twitter_sheet_df['Hashtags/Topics'].values:
        old_row = twitter_sheet_df.loc[twitter_sheet_df['Hashtags/Topics'] == topic].iloc[0]
        old_rank = int(old_row['Rank'].replace('.', ''))
        old_volume_str = old_row['Tweet Volume']
        old_volume_numeric = convert_volume(old_volume_str)

        # Calculate rank and volume change
        rank_change_val = old_rank - rank
        volume_change_val = volume_numeric - old_volume_numeric
        volume_change_str = f"{volume_change_val:+.1f}K" if volume_change_val != 0 else "-"
        
        # Determine the rank change string based on whether there is an actual change
        if rank_change_val == 0:
            rank_change_str = "-"
        elif rank_change_val > 0:
            rank_change_str = f"+{rank_change_val}"
        else:
            rank_change_str = str(rank_change_val)
        
        rank_change.append(rank_change_str)
        volume_change.append(volume_change_str)
    else:
        # If the topic is new and wasn't in the old trends
        rank_change.append('NEW')
        volume_change.append('NEW')  


# Combine data into a DataFrame with the date column
twitter_data = pd.DataFrame({"Rank": ranks, "Hashtags/Topics": topics, "Date": [previous_date]*len(ranks), "Tweet Volume": tweet_volume})
twitter_data['Rank Change'] = rank_change
twitter_data['Volume Change'] = volume_change
    
 # INSTAGRAM REELS ----------------------------------------------------------------------------
 
instareel_url = "https://slayingsocial.com/instagram-reels-trends/  "

# Send a GET request to the URL
try:
    response = requests.get(instareel_url)
    response.raise_for_status()  # Raise an exception for non-200 status codes
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the elements containing insta reels
    title_elements = soup.select("p+ p")
   
    # Extract text from elements
    titles = [title.get_text(strip=True) for title in title_elements]

    titles_cleaned = []
    descriptions = []
    URLS = []
    # Process each title
    for title_element in title_elements:
        title_text = title_element.get_text(strip=True)
        if "Example" in title_text:  # Check if title contains the word "Example"
            segments = title_text.split("|")
            title_part = segments[0].strip()
            # Remove "Trend" and "*" from title_part
            title_part_cleaned = title_part.replace("Trend", "").replace("*", "").strip()

            # Try to find an <a> tag within the title_element
            a_tag = title_element.find('a')
            URL = a_tag['href'] if a_tag else None

            titles_cleaned.append(title_part_cleaned)
            if URL:
                URLS.append(URL)
            else:
                URLS.append("-")

            description_part = ""
            if len(segments) > 1:
                description_part = segments[1].strip()
                description_part = description_part.replace("Example:", "").replace("Posting a", "").replace("Posting an", "").strip()
            descriptions.append(description_part)


    # Create a DataFrame with title and description
    instareel_data = pd.DataFrame({"Title": titles_cleaned, "Description": descriptions, "URL": URLS})
    instareel_data['Date'] = previous_date
    
except requests.exceptions.RequestException as e:
    print(f"Failed to retrieve the webpage: {e}")
    
    
# GOOGLE TRENDS ----------------------------------------------------------------------------
from pytrends.request import TrendReq
import pandas as pd
from datetime import date, timedelta

# Set up pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# Get trending searches
google_data = pytrends.trending_searches(pn='singapore')
google_data['Date'] = previous_date

google_data = google_data.rename(columns={google_data.columns[0]: "Trends"})

worksheet = sh.worksheet('Google Trends')
def process_google_data(google_data, worksheet):
    # Get all trends from the Google Sheet
    sheet_trends = worksheet.col_values(1)

    matched_trends = []
    # Check each trend in google_data
    for index, row in google_data.iterrows():
        trend = row['Trends']
        if trend in sheet_trends:
            matched_trends.append(trend)
    
    if not matched_trends:
        print("No matching trends found in Google Sheets.")
        return google_data  # Return the entire google_data DataFrame if no matching trends are found
    
    # Find the first matched trend
    first_matched_trend = matched_trends[0]

    # Split google_data based on the first matched trend
    split_index = google_data.index[google_data['Trends'] == first_matched_trend][0]
    google_new = google_data.iloc[:split_index]

    return google_new

# Process the scraped data and get new trends
google_new = process_google_data(google_data, worksheet)

# TIKTOK TRENDS  ----------------------------------------------------------------------------
 
tiktok_url = "https://slayingsocial.com/tiktok-trends-right-now/"

# Send a GET request to the URL
response = requests.get(tiktok_url)
response.raise_for_status()  # Raise an exception for non-200 status codes
soup = BeautifulSoup(response.content, "html.parser")

# Find the elements containing insta reels
elements = soup.select("p+ p")
   
# Extract text from elements
titles = [title.get_text(strip=True) for title in elements]

date, titles_list, descriptions, urls = [], [], [], []

# Process each title
for title_element in elements:
    title_text = title_element.get_text(strip=True)
    
    if "Example" in title_text:
        # Find an <a> tag within the title_element for the URL
        a_tag = title_element.find('a')
        url = a_tag['href'] if a_tag else "-"
        
        segments = title_text.split("|")
        title_part = segments[0].strip()
        title_part = title_part.replace("Trend", "").replace("*", "").strip()

        title_segments = title_part.split(")")

        if len(title_segments) > 1 and title_segments[1].strip():
            date_part_raw = title_segments[0].strip("(Added")
            try:
                date_object = datetime.datetime.strptime(date_part_raw.strip(), "%B %d, %Y")
                date_formatted = date_object.strftime("%Y-%m-%d")
            except ValueError:
                date_formatted = "-"
            title_cleaned = title_segments[1].strip()

            date.append(date_formatted)
            titles_list.append(title_cleaned)
            urls.append(url)  # Use extracted URL

            description_part = ""
            if len(segments) > 1:
                description_part = segments[1].strip()
                description_part = description_part.replace("Example:", "").replace("Posting a", "").replace("Posting an", "").strip()
                descriptions.append(description_part)

                
# Create a DataFrame with title and description
tiktok_data = pd.DataFrame({"Title": titles_list , "Description": descriptions, "URL": urls, "Date": date})'''
  
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
