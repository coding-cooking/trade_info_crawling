import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'https://panjiva.com/sitemap/supplier_country_detail/Viet%252525252520Nam/45/'
data = []

# Loop through pages (example for the first 10 pages)
for page_num in range(1, 11):
    url = f'{base_url}{page_num}'
    print(f"Scraping page: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                if cols:  # Only append non-empty rows
                    data.append(cols)
            print(f"Found {len(rows)} rows on page {page_num}")
        else:
            print(f'No table found on page {page_num}')
    except requests.RequestException as e:
        print(f"Error fetching page {page_num}: {e}")

# Create DataFrame and inspect it
df = pd.DataFrame(data)
print(f"DataFrame shape: {df.shape}")
print(df.head())  # Print the first few rows of the DataFrame

if not df.empty:
    # Automatically generate column names based on the number of columns
    df.columns = [f'Column{i + 1}' for i in range(len(df.columns))]
    df.to_excel('output.xlsx', index=False)
    print('Scraping complete, data saved to output.xlsx')
else:
    print("No data was scraped. The DataFrame is empty.")