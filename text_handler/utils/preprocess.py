# utils/preprocess.py
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup


def get_preprocessed_text(url: str) -> str:
    """
    주어진 URL에서 HTML 파일을 읽어들인 후 텍스트를 전처리하여 반환합니다.

    Parameters:
    url (str): HTML 파일을 가져올 URL

    Returns:
    str: 전처리된 텍스트
    """
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    time_to_live = 3
    while True:
        try:
            driver.get(url)
            wait = WebDriverWait(driver, timeout=5)
            wait.until(lambda d: d.find_element(By.TAG_NAME, 'body'))
            break
        except:
            time_to_live -= 1
            if time_to_live > 0:
                continue
            else:
                return ""

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    headers = soup.find_all('header')
    header = None
    if len(headers) == 0:
        if soup.find('div', 'post-header') != None:
            header = soup.find('div', 'post-header')
        if soup.find('div', 'post-author-info') != None:
            header = soup.find('div', 'post-author-info')
        if soup.find('div', 'area_title') != None:
            header = soup.find('div', 'area_title')
    else:
        header = headers[1] if len(headers) > 1 else headers[0]

    article = soup.article
    if article == None:
        if soup.find('div', 'post') != None:
            article = soup.find('div', 'post')
        if soup.find('div', 'post-content-body') != None:
            article = soup.find('div', 'post-content-body')
        if soup.find('div', 'contents_style') != None:
            article = soup.find('div', 'contents_style')
        if soup.find('div', 'post_details') != None:
            article = soup.find('div', 'post_details')

    preprocessed_text = ''

    if article != None:
        preprocessed_text += 'Title: '
        title = ''
        if header != None:
            if header.h1 != None:
                title = header.h1.get_text()
            elif header.h3 != None:
                title = header.h3.get_text()
        if title == '':
            if article.h1 != None:
                title = article.h1.get_text()
            else:
                title = article.h2.get_text()
        preprocessed_text += title + '\n'
        for tag in article.find_all(['h1', 'h2', 'h3', 'p']):
            if tag.get_text() != title:
                if tag.name in ['h1', 'h2', 'h3']:
                    preprocessed_text += 'Subtitle: '
                preprocessed_text += tag.get_text() + '\n'

    return preprocessed_text
