from bs4 import BeautifulSoup
import requests
import pandas as pd
import pygsheets
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
import os
from datetime import datetime

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
authors = []
for author in author_elements:
    author_text = author.get_text(strip=True)
    if "Upload by" not in author_text:
        authors.append(author_text)
 

# Combine data into a DataFrame
yt_data = pd.DataFrame({"Rank": ranks, "Topic": topics, "YouTuber": authors, "Views": views,"Likes": likes,"Comments": comments})
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
        return 10000  # Interpret 'Under 10k' as 10,000
    elif 'k' in volume_str:
        return float(volume_str.replace('k', '')) * 1000
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
        if rank_change_val > 0:
            rank_change_str = f"+{rank_change_val}"
        else:
            rank_change_str = str(rank_change_val)

        # Prepare the volume change for display
        if abs(volume_change_val) >= 1000:
            volume_change_str = f"{volume_change_val / 1000}K"
        else:
            volume_change_str = str(int(volume_change_val))  # Converting to int to remove any decimal point for whole numbers

        rank_change.append(rank_change_val)
        volume_change.append(volume_change_str)
    else:
        rank_change.append('-')
        volume_change.append('-')

# Combine data into a DataFrame with the date column
twitter_data = pd.DataFrame({"Rank": ranks, "Hashtags/Topics": topics, "Date": [previous_date]*len(ranks), "Tweet Volume": tweet_volume})

# Add rank change and volume change to the twitter_data DataFrame
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
    # Process each title
    for title in titles:
        if "Example" in title:  # Check if title contains the word "Example"
            segments = title.split("|")
            title_part = segments[0].strip()
            # Remove "Trend" and "*" from title_part
            title_part = title_part.replace("Trend", "").replace("*", "").strip()
            titles_cleaned.append(title_part)
            description_part = ""
            if len(segments) > 1:
                description_part = segments[1].strip()
                description_part = description_part.replace("Example:", "").strip()
                description_part = description_part.replace("Posting a", "").strip()
            descriptions.append(description_part)

    # Create a DataFrame with title and description
    instareel_data = pd.DataFrame({"Title": titles_cleaned, "Description": descriptions})
    instareel_data['Date'] = previous_date


    # Display the first few rows of the data
    print(instareel_data.head(10))
    
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
    
    # List to store indexes of found trends in Google Sheets
    found_indexes = []
    
    # Check each trend in google_data
    for index, row in google_data.iterrows():
        trend = row['Trends']
        if trend in sheet_trends:
            # Note: This approach assumes the trends in the Google Sheet are unique
            found_indexes.append(sheet_trends.index(trend))
    
    # If any trends are found, sort indexes and process accordingly
    if found_indexes:
        found_indexes.sort()
        # Find the index of the first matched trend in google_data
        first_found_index = google_data['Trends'].tolist().index(sheet_trends[found_indexes[0]])
        # Get trends before the first found one
        google_new = google_data.iloc[:first_found_index]  # Slice to get trends before the found one
        return new_trends
    else:
        print("No matching trends found in Google Sheets.")
        return None

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

titles_list = []
descriptions = []
date = []

# Process each title
for title in titles:
    if "Example" in title:  # Check if title contains the word "Example"
        segments = title.split("|")
        title_part = segments[0].strip()
        # Remove "Trend" and "*" from title_part
        title_part = title_part.replace("Trend", "").replace("*", "").strip()
        # Split the title_part by ")"
        title_segments = title_part.split(")")
        # Ensure that there is a part after the split and it's not empty
        if len(title_segments) > 1 and title_segments[1].strip():
            date_part_raw = title_segments[0].strip("(Added")
            # Parse the date
            # Parse the date, ensuring to strip any leading/trailing whitespace
            date_object = datetime.datetime.strptime(date_part_raw.strip(), "%B %d, %Y")
            # Convert the date to the desired format
            date_formatted = date_object.strftime("%Y-%m-%d")
            title_cleaned = title_segments[1].strip()
            # Append to respective lists
            date.append(date_formatted)
            titles_list.append(title_cleaned)
            description_part = ""
            if len(segments) > 1:
                description_part = segments[1].strip()
                description_part = description_part.replace("Example:", "").strip()
                descriptions.append(description_part)
        # If the condition is not met, continue to the next iteration without appending
        else:
            continue

# Create a DataFrame with title and description
tiktok_data = pd.DataFrame({"Title": titles_list , "Description": descriptions, "Date": date})

    
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
update_sheet('YouTube', yt_data, include_header=True)
update_sheet('Twitter', twitter_data, include_header=True)
update_sheet('Instagram Reels', instareel_data, include_header=True)
update_sheet('Google Trends', google_new, include_header=True)
update_sheet('TikTok Trends', tiktok_data, include_header=True)
