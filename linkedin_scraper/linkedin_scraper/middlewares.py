import random
import scrapy
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LinkedinAuthMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def spider_opened(self, spider):
        self.driver = webdriver.Chrome()  # Make sure you have ChromeDriver installed
        self.login(spider)

    def spider_closed(self, spider):
        self.driver.quit()

    def login(self, spider):
        self.driver.get('https://www.linkedin.com/login')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
        self.driver.find_element(By.ID, 'username').send_keys(spider.linkedin_username)
        self.driver.find_element(By.ID, 'password').send_keys(spider.linkedin_password)
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        WebDriverWait(self.driver, 10).until(EC.url_contains('feed'))

    def process_request(self, request, spider):
        self.driver.get(request.url)
        body = self.driver.page_source
        return scrapy.http.HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)

class RotateUserAgentMiddleware:
    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        user_agents = crawler.settings.get('USER_AGENT_LIST', [])
        return cls(user_agents)

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)