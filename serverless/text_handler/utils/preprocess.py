# utils/preprocess.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup

from typing import Tuple

def get_preprocessed_text(url: str) -> Tuple[str]:
    """
    주어진 URL에서 HTML 파일을 읽어들인 후 텍스트를 전처리하여 반환합니다.

    Parameters:
    url (str): HTML 파일을 가져올 URL

    Returns:
    str: 전처리된 텍스트
    """
    chrome_options = Options()
    chrome_options.binary_location = "/opt/chrome/chrome"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument('window-size=1392x1150')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")

    service = Service(executable_path="/opt/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    time_to_live = 3
    while True:
        try:
            driver.get(url)
            wait = WebDriverWait(driver, timeout=10)
            wait.until(lambda d: d.find_element(By.CSS_SELECTOR, 'h1'))
            break
        except Exception as e:
            time_to_live -= 1
            if time_to_live > 0:
                continue
            else:
                print(f"error : unable to get post data {url}")
                driver.quit()
                exit()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    title = None
    articles = None
    if soup.find('h1', 'daum-wm-title') and soup.find('div', 'daum-wm-content'):
        # kakao
        title = soup.find('h1', 'daum-wm-title')
        articles = [soup.find('div', 'daum-wm-content')]
    elif soup.find('article', 'blog-post') and soup.find('section', itemprop='articleBody'):
        # skplanet
        title = soup.find('article', 'blog-post').header.h2
        articles = [soup.find('section', itemprop='articleBody')]
    elif soup.find('h1', 'Post-module--tit--932c8') and soup.find('div', 'blog-post-content'):
        # oliveyoung
        title = soup.find('h1', 'Post-module--tit--932c8')
        articles = [soup.find('div', 'blog-post-content')]
    elif soup.find('h1', 'page-title') and soup.find('div', 'post'):
        # kurly
        title = soup.find('h1', 'page-title')
        articles = [soup.find('div', 'post')]
    elif soup.find('h1', 'blog-post-title') and soup.find('section', 'blog-post-content'):
        # aws
        title = soup.find('h1', 'blog-post-title')
        articles = [soup.find('section', 'blog-post-content')]
    elif soup.find('h1', 'title') and soup.find('div', 'content'):
        # ly corporation
        title = soup.find('h1', 'title')
        articles = [soup.find('div', 'content').div]
    elif soup.find('h1', 'css-vf4rrt') and soup.find('div', 'css-1vn47db'):
        # toss
        title = soup.find('h1', 'css-vf4rrt')
        articles = [soup.find('div', 'css-1vn47db')]
    elif soup.find('h1', 'pw-post-title') and soup.find('section'):
        # daangn, yogiyo, yeogi, cj, 29cm, heydealer
        title = soup.find('h1', 'pw-post-title')
        articles = soup.find('section').find_all('div', 'gn go gp gq gr')
    elif soup.find('h1', 'pw-post-title') and soup.find('p', 'pw-post-body-paragraph'):
        # daangn 25.3.20.
        title = soup.find('h1', 'pw-post-title')
        articles = soup.find_all('p', 'pw-post-body-paragraph')
    elif soup.find('h1', 'entry-title') and soup.find('div', 'entry-content'):
        # hancom
        title = soup.find('h1', 'entry-title')
        articles = [soup.find('div', 'entry-content')]
    elif soup.find('h1', 'astro-QLFJKSAO') and soup.find('article', 'astro-ETA4E5NM'):
        # kakaopay
        title = soup.find('h1', 'astro-QLFJKSAO')
        articles = [soup.find('article', 'astro-ETA4E5NM')]
    elif soup.find('div', 'post-heading') and soup.find('article', 'blog-post'):
        # saramin
        title = soup.find('div', 'post-heading').h1
        articles = [soup.find('article', 'blog-post')]
    elif soup.find('header', 'mb-13 border-b border-bg-line-weak pb-13') and soup.find('article', id='article'):
        # devsisters
        title = soup.find('header', 'mb-13 border-b border-bg-line-weak pb-13').h1
        articles = [soup.find('article', id='article').div]
    elif soup.find('h1', 'title') and soup.find('article', 'post-content'):
        # brandilabs
        title = soup.find('h1', 'title')
        articles = [soup.find('article', 'post-content')]
    elif soup.find('div', 'post-header') and soup.find('div', 'post-content-body'):
        # woowahan
        title = soup.find('div', 'post-header').h1
        articles = [soup.find('div', 'post-content-body')]
    elif soup.find('h3', 'tit_post') and soup.find('div', 'contents_style'):
        # gmarket
        title = soup.find('h3', 'tit_post')
        articles = [soup.find('div', 'contents_style')]
    elif soup.find('h1', 'post-title') and soup.find('div', 'post'):
        # spoqa
        title = soup.find('h1', 'post-title')
        articles = [soup.find('div', 'post')]
    elif soup.find('h1', 'postDetailsstyle__PostTitle-sc-r1ppdr-1') and soup.find('div', 'postDetailsstyle__PostDescription-sc-r1ppdr-5'):
        # banksalad
        title = soup.find('h1', 'postDetailsstyle__PostTitle-sc-r1ppdr-1')
        articles = [soup.find('div', 'postDetailsstyle__PostDescription-sc-r1ppdr-5')]
    else:
        print(f"error: unable to find title and articles {url}")
        return ''

    preprocessed_text_with_subtitle = ''
    preprocessed_text = ''
    title_text = title.get_text().strip()
    preprocessed_text_with_subtitle += 'Title: ' + title_text + '\n'
    preprocessed_text += 'Title: ' + title_text + '\n'
    for article in articles:
        for tag in article.find_all(['h1', 'h2', 'h3', 'p', 'ul'], recursive=True):
            article_text = tag.get_text().strip()
            if article_text != '' and article_text != title_text:
                if tag.name in ['h1', 'h2', 'h3']:
                    preprocessed_text_with_subtitle += 'Subtitle: '
                preprocessed_text_with_subtitle += article_text + '\n'
                preprocessed_text += article_text + '\n'

    return preprocessed_text_with_subtitle, preprocessed_text
