from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
import time

SBR_WEBDRIVER = 'https://brd-customer-hl_b8ba7595-zone-ai_scraper:mrgwpkds5qwc@brd.superproxy.io:9515'

def scrape_website(website):
    print("Launching chrome browser...")
    
    ua = UserAgent()
    user_agent = ua.random
    
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument("--disable-gpu") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f'--user-agent={user_agent}')

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(website)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        html = driver.page_source
    finally:
        driver.close()
    
    return html
    
def extract_body_content(html_content):
    '''
    Extracting the body content which will then be cleaned.
    '''
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body

    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    '''
    Remove script and style tags from the DOM.
    '''
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get all of the text and separate it with a new line
    cleaned_content = soup.getText(separator="\n")
    # Remove any backslash n characters that are unnecessary. 
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    '''
    Creating batches of 6000 characters, because LLM can't handle more than that.
    '''
    return [
        dom_content[i: i+ max_length] for i in range(0, len(dom_content), max_length)
    ]