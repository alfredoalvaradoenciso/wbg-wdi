import requests
import pandas as pd
from bs4 import BeautifulSoup
import re


def extract_pages_value(url):
    response = requests.get(url)
    if response.status_code == 200:
        content = response.content.decode('utf-8')  # Decode response content as text
        first_two_lines = content.split("\n", 2)[:2]
        for line in first_two_lines:
            pages_match = re.search(r'pages="(\d+)"', line)
            if pages_match:
                pages_value = int(pages_match.group(1))
                return pages_value
    return None

# URL for the World Bank API
url = "https://api.worldbank.org/v2/country/LCN;EAP;WLD;ECA/indicator/NY.GDP.MKTP.KD.ZG?date=1980:2021"

# Extract the value of "pages"
pages_value = extract_pages_value(url)
perpage = pages_value*50
url = f"https://api.worldbank.org/v2/country/LCN;EAP;WLD;ECA/indicator/NY.GDP.MKTP.KD.ZG?date=1980:2021&per_page={perpage}"


# Make the API request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    try:
        soup = BeautifulSoup(response.content, "xml")

        # Extract the relevant data from the API response
        extracted_data = []
        for data_element in soup.find_all("data"):
            countryiso3code = data_element.find("countryiso3code").text
            date = int(data_element.find("date").text)
            value = data_element.find("value").text
            if value.strip() == "":
                value = None
            else:
                value = float(value)
            extracted_data.append({"countryiso3code": countryiso3code, "date": date, "value": value})

        # Create a DataFrame from the extracted data
        df = pd.DataFrame(extracted_data)
        print(df)

    except Exception as e:
        print("Error parsing XML:", e)

else:
    print("Error: Unable to fetch data from the API.")
