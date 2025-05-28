from datetime import datetime, timedelta
import os 
import requests

def check_and_download_file(url, destination_path):
    # delete destination_path if it exists
    if os.path.exists(destination_path):
        print(f"Destination path '{destination_path}' already exists. Deleting it.")
        os.remove(destination_path)
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        if response.status_code == 200:
            with open(destination_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"File downloaded successfully to: {destination_path}")
            return True 
        else:
            print(f"File not found or an error occurred. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return False 

def download_latest_doc():
    # date from today to the last 365 days 
    for i in range(365):
        print (f"\n\nChecking date: {i} days ago")
        date = datetime.now() - timedelta(days=i)
        formatted_date = date.strftime("%Y-%m-%d")
        te_target_file = f"./the_economist/{formatted_date}-parse.txt"
        # if target exist, continue 
        if os.path.exists(te_target_file):
            print(f"Target file found: {te_target_file}")
            continue
        original_date = date.strftime("%Y.%m.%d")
        local_file = "./local_file.epub"
        # Example usage with your provided URL:
        file_url = f"https://raw.githubusercontent.com/hehonghui/awesome-english-ebooks/master/01_economist/te_{original_date}/TheEconomist.{original_date}.epub"
        if check_and_download_file(file_url, local_file):
            return True, local_file, te_target_file
    return False, None, None
