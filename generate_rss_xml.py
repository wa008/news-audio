import os
from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import formatdate # For RFC 822 date formatting

# --- Configuration Parameters ---
URL_PREFIX = "https://github.com/wa008/news-audio/raw/refs/heads/main/"
RSS_CHANNEL_TITLE = "中文外刊"
RSS_CHANNEL_LINK = "https://wa008.github.io/news-audio/rss.xml" # Main link for the RSS channel
RSS_CHANNEL_DESCRIPTION = "经济学人外刊音频，持续更新中"
# --- End of Configuration ---

def create_rss_feed(SOURCE_DIRECTORY_NAME, RSS_OUTPUT_FILE):
    source_dir = Path(SOURCE_DIRECTORY_NAME)
    if not source_dir.is_dir():
        print(f"Error: Directory {SOURCE_DIRECTORY_NAME} not found.")

    # 1. Create RSS root element and channel element
    rss_element = ET.Element("rss", version="2.0", attrib={"xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"})
    channel_element = ET.SubElement(rss_element, "channel")

    # 2. Set Channel metadata
    ET.SubElement(channel_element, "title").text = RSS_CHANNEL_TITLE
    ET.SubElement(channel_element, "link").text = RSS_CHANNEL_LINK
    ET.SubElement(channel_element, "description").text = RSS_CHANNEL_DESCRIPTION
    ET.SubElement(channel_element, "language").text = "zh-cn" # Can be changed based on actual content
    # lastBuildDate will be set to the current time after all items are processed or at the beginning
    ET.SubElement(channel_element, "lastBuildDate").text = formatdate(
        datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=8))).timestamp() # For Shanghai time zone
    )

    # 3. Find all .wav files and sort them by modification time in descending order
    wav_files = []
    for wav_path in source_dir.glob("*.wav"):
        try:
            mtime = wav_path.stat().st_mtime
            wav_files.append((wav_path, mtime))
        except FileNotFoundError:
            print(f"Warning: File {wav_path} not found while getting status, skipped.")
            continue

    # Sort by modification time in descending order (newest first)
    wav_files.sort(key=lambda item: item[1], reverse=True)


    # 4. Create an <item> element for each .wav file
    for wav_path, mtime in wav_files:
        base_name = wav_path.stem
        txt_path = os.path.join(SOURCE_DIRECTORY_NAME, wav_path.name.replace("audio.wav", "translated.txt"))

        # Get description (first line of the .txt file)
        item_description = f"Audio: {base_name}" # Default description
        print (txt_path)
        if os.path.exists(txt_path):
            try:
                with open(txt_path, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    if first_line:
                        item_description = first_line
            except Exception as e:
                print(f"Warning: Failed to read description file '{txt_path}': {e}")
        else:
            print(f"Info: Description file '{txt_path}' not found, using default description.")
        item_description = item_description.strip().strip('.').strip('。')

        pub_date = formatdate(
            float(mtime) + 3600 * 8.0
        )

        # Construct file link
        # Link structure: URL_PREFIX + directory_name + / + file_name
        file_link = f"{URL_PREFIX.rstrip('/')}/{SOURCE_DIRECTORY_NAME}/{wav_path.name}"

        # Get file size
        try:
            file_size = str(wav_path.stat().st_size)
        except FileNotFoundError:
            print(f"Warning: File {wav_path} not found while getting size, skipping this item.")
            continue

        # Create <item>
        item_element = ET.SubElement(channel_element, "item")
        ET.SubElement(item_element, "title").text = item_description
        ET.SubElement(item_element, "link").text = file_link # Can be the audio file link or a related webpage link
        ET.SubElement(item_element, "description").text = item_description
        ET.SubElement(item_element, "pubDate").text = pub_date
        ET.SubElement(item_element, "guid", isPermaLink="true").text = file_link # GUID is usually a permalink

        # Add <enclosure> tag, used by podcast clients to identify the audio file
        ET.SubElement(item_element, "enclosure", {
            "url": file_link,
            "length": file_size,
            "type": "audio/mpeg" # MIME type
        })

    # 5. Generate XML tree and write to file
    tree = ET.ElementTree(rss_element)
    # Python 3.9+ supports ET.indent() for pretty printing
    if hasattr(ET, 'indent'):
        ET.indent(tree, space="  ", level=0)

    try:
        with open(RSS_OUTPUT_FILE, 'wb') as f: # Use 'wb' to write XML declaration with UTF-8 encoding
            tree.write(f, encoding='utf-8', xml_declaration=True)
        print(f"RSS feed file '{RSS_OUTPUT_FILE}' generated successfully.")
    except IOError as e:
        print(f"Error: Failed to write RSS file '{RSS_OUTPUT_FILE}': {e}")

if __name__ == "__main__":
    # Ensure the script is run from the parent directory of the 'the_economist' directory,
    # or that SOURCE_DIRECTORY_NAME is an absolute path or a correct relative path.
    # For example, if the script is at the same level as the 'the_economist' directory,
    # the current setting is correct.
    SOURCE_DIRECTORY_NAME = "the_economist/2025-05-24" # Name of the directory containing audio files
    RSS_OUTPUT_FILE = "rss.xml"
    create_rss_feed(SOURCE_DIRECTORY_NAME, RSS_OUTPUT_FILE)
