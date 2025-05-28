import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import sys 

def parse_epub(epub_path, text_file):
    """
    Parses an EPUB file and returns a dictionary with chapter titles as keys
    and chapter content (plain text) as values.

    Args:
        epub_path (str): The path to the EPUB file.
        text_file (str): The path to the text file where the content will be saved.

    Returns:
        dict: A dictionary where keys are chapter titles and values are
              the corresponding chapter content as plain text.
              Returns an empty dictionary if the EPUB cannot be processed
              or has no discernible chapters in the TOC.
    """
    book = epub.read_epub(epub_path)
    chapters_dict = {}

    # Helper function to clean HTML and extract text
    def get_text_from_html(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        # Remove script and style elements
        for script_or_style in soup(["script", "style", "te_section_title"]):
            script_or_style.decompose()

        section_title_element = soup.find(class_='te_section_title')
        if section_title_element:
            section_title = section_title_element.string
        else:
            section_title = None
        te_article_rubric_element = soup.find(class_='te_article_rubric')
        if te_article_rubric_element:
            te_article_rubric = te_article_rubric_element.string
            te_article_rubric = te_article_rubric.strip()
            if not te_article_rubric.endswith('.'):
                te_article_rubric += '. '
        else:
            te_article_rubric = None 
        remove_classes = ['title', 'te_section_title', 'te_article_title', 'te_fly_span', \
                    'te_article_datePublished', 'te_article_rubric']
        # for i in range(20):
        #     remove_classes.append(f"calibre{i}")
        for key in remove_classes:
            for element in soup.find_all(class_=key):
                element.decompose()
        for element in soup.find_all('head'):
            element.decompose()
        # print(soup.prettify())
        # sys.exit(0)
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        text.strip().strip(".").strip().strip(".")
        
        download_sufix = "This article was downloaded by"
        if download_sufix in text and len(text.split(download_sufix)[1]) < 300:
            text = text.split(download_sufix)[0]
        ads_sufix = "To stay on top of the biggest stories in business and technology"
        if ads_sufix in text and len(text.split(ads_sufix)[1]) < 300:
            text = text.split(ads_sufix)[0]
        text = ".".join([x for x in text.split(" | ") if len(x.strip()) > 100])

        if te_article_rubric: 
            text = te_article_rubric + text 
        return section_title, text

    for item in book.toc:
        if isinstance(item, tuple) or isinstance(item, list): # Handling sections or nested chapters
            if len(item) > 1 and (isinstance(item[1], tuple) or isinstance(item[1], list)):
                section_title = item[0] # Or handle section titles as needed
                for sub_item in item[1]:
                    if isinstance(sub_item, ebooklib.epub.Link):
                        title = sub_item.title
                        # Optionally prepend section title: f"{section_title} - {sub_item.title}"
                        href = sub_item.href
                        href_cleaned = href.split('#')[0]
                        doc_item = book.get_item_with_href(href_cleaned)
                        if doc_item:
                            html_content = doc_item.get_content()
                            section_title, text_content = get_text_from_html(html_content.decode('utf-8', errors='ignore'))
                            if section_title: 
                                title = section_title + " - " + title
                            if len(text_content) > 500:
                                chapters_dict[title] = text_content

    
    outputs = []
    for title, content in chapters_dict.items():
        outputs.append(f"{title}\n\n{content}")
    # Save the parsed content to a text file
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(("\n\n" + "-" * 50 + "\n\n").join(outputs))
    return chapters_dict
