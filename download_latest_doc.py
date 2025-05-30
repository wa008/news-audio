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
    for i in range(60):
        print (f"\n\nChecking date: {i} days ago")
        date = datetime.now() - timedelta(days=i)
        formatted_date = date.strftime("%Y-%m-%d")
        path = f"./the_economist/{formatted_date}"
        done_file = f"{path}/done"
        if os.path.exists(done_file): 
            print (f"{done_file} exists")
            continue
        original_date = date.strftime("%Y.%m.%d")
        local_file = "./temp_epub.epub"
        file_url = f"https://raw.githubusercontent.com/hehonghui/awesome-english-ebooks/master/01_economist/te_{original_date}/TheEconomist.{original_date}.epub"
        if check_and_download_file(file_url, local_file):
            return True, formatted_date, local_file
    return False, None, None

