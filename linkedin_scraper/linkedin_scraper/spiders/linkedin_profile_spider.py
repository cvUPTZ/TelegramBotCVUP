import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from ..items import LinkedInProfileItem, ExperienceItem, EducationItem
from urllib.parse import urljoin
import time
import random
from dotenv import load_dotenv
import os

# from scrapy.http import FormRequest
# from scrapy.utils.response import open_in_browser
from itemloaders import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags
from urllib.parse import urljoin
import time
import random
from dotenv import load_dotenv
import os
import logging
import json

class LinkedInProfileSpider(scrapy.Spider):
    name = 'linkedin_profile_spider'
    allowed_domains = ['linkedin.com']
    start_urls = ['https://www.linkedin.com/login']
    
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'DOWNLOAD_DELAY': 5,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 5,
        'AUTOTHROTTLE_MAX_DELAY': 60,
        'CONCURRENT_REQUESTS': 1,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 403, 404, 408],
    }

    def __init__(self, *args, **kwargs):
        super(LinkedInProfileSpider, self).__init__(*args, **kwargs)
        load_dotenv()
        self.linkedin_username = kwargs.get('linkedin_username') or os.getenv('LINKEDIN_USERNAME')
        self.linkedin_password = kwargs.get('linkedin_password') or os.getenv('LINKEDIN_PASSWORD')
        self.max_profiles = int(kwargs.get('max_profiles', 10))
        self.scraped_profiles = 0
        self.search_query = kwargs.get('search_query', 'software developer')

        if not self.linkedin_username or not self.linkedin_password:
            raise ValueError("LinkedIn credentials are required. Provide them as spider arguments or in the .env file.")

    def start_requests(self):
        self.logger.info(f"Starting login process with username: {self.linkedin_username}")
        return [FormRequest(
            "https://www.linkedin.com/uas/login-submit",
            formdata={
                'session_key': self.linkedin_username,
                'session_password': self.linkedin_password,
            },
            callback=self.after_login,
            errback=self.error_handler
        )]

    def after_login(self, response):
        if "feed" in response.url:
            self.logger.info("Login successful")
            return self.start_search()
        else:
            self.logger.error("Login failed. Check credentials and try again.")
            open_in_browser(response)
            return

    def start_search(self):
        search_url = f'https://www.linkedin.com/search/results/people/?keywords={self.search_query}&origin=GLOBAL_SEARCH_HEADER'
        return scrapy.Request(url=search_url, callback=self.parse_search_results, errback=self.error_handler)

    def parse_search_results(self, response):
        profile_links = response.css('span.entity-result__title-text a::attr(href)').getall()
        
        for link in profile_links:
            if '/in/' in link and self.scraped_profiles < self.max_profiles:
                profile_link = urljoin(response.url, link)
                self.scraped_profiles += 1
                yield scrapy.Request(profile_link, callback=self.parse_profile, errback=self.error_handler)

        if self.scraped_profiles < self.max_profiles:
            next_page = response.css('button.artdeco-pagination__button--next:not([disabled])::attr(aria-label)').get()
            if next_page:
                yield response.follow(next_page, callback=self.parse_search_results)

    def parse_profile(self, response):
        loader = ItemLoader(item=LinkedInProfileItem(), response=response)
        loader.default_output_processor = TakeFirst()

        loader.add_css('name', 'h1.text-heading-xlarge::text')
        loader.add_css('title', 'div.text-body-medium::text')
        loader.add_css('location', 'span.text-body-small.inline::text')
        loader.add_value('url', response.url)
        
        about_section = response.css('div#about').xpath('./following-sibling::div[1]')
        loader.add_value('about', about_section.css('::text').getall())

        # Experience
        loader.add_value('experience', self.parse_experience(response))

        # Education
        loader.add_value('education', self.parse_education(response))

        # Skills
        skills_section = response.css('section[aria-label="Skills"]')
        loader.add_value('skills', skills_section.css('span.mr1.hoverable-link-text::text').getall())

        # Certifications
        loader.add_value('certifications', self.parse_certifications(response))

        # Languages
        languages_section = response.css('section[aria-label="Languages"]')
        loader.add_value('languages', languages_section.css('span.mr1.hoverable-link-text::text').getall())

        # Volunteering
        loader.add_value('volunteering', self.parse_volunteering(response))

        # Recommendations
        loader.add_value('recommendations', self.parse_recommendations(response))

        # Accomplishments
        accomplishments_section = response.css('section[aria-label="Accomplishments"]')
        loader.add_value('accomplishments', accomplishments_section.css('span.mr1.hoverable-link-text::text').getall())

        # Interests
        interests_section = response.css('section[aria-label="Interests"]')
        loader.add_value('interests', interests_section.css('span.mr1.hoverable-link-text::text').getall())

        yield loader.load_item()
        
        self.random_delay()

    def parse_experience(self, response):
        experience_items = response.css('li.artdeco-list__item.pvs-list__item--line-separated')
        experiences = []
        for item in experience_items:
            exp_loader = ItemLoader(item=ExperienceItem(), selector=item)
            exp_loader.default_output_processor = TakeFirst()
            exp_loader.add_css('title', 'span.mr1.t-bold span[aria-hidden="true"]::text')
            exp_loader.add_css('company', 'span.t-14.t-normal span[aria-hidden="true"]::text')
            exp_loader.add_css('duration', 'span.t-14.t-normal.t-black--light span[aria-hidden="true"]::text')
            exp_loader.add_css('location', 'span.t-14.t-normal.t-black--light span[aria-hidden="true"]::text')
            exp_loader.add_css('description', 'div.pvs-list__outer-container ul.pvs-list li span.visually-hidden::text')
            experiences.append(exp_loader.load_item())
        return experiences

    def parse_education(self, response):
        education_items = response.css('li.artdeco-list__item.pvs-list__item--line-separated')
        educations = []
        for item in education_items:
            edu_loader = ItemLoader(item=EducationItem(), selector=item)
            edu_loader.default_output_processor = TakeFirst()
            edu_loader.add_css('school', 'span.mr1.t-bold span[aria-hidden="true"]::text')
            edu_loader.add_css('degree', 'span.t-14.t-normal span[aria-hidden="true"]::text')
            edu_loader.add_css('field_of_study', 'span.t-14.t-normal.t-black--light span[aria-hidden="true"]::text')
            edu_loader.add_css('date_range', 'span.t-14.t-normal.t-black--light span[aria-hidden="true"]::text')
            educations.append(edu_loader.load_item())
        return educations

    def parse_certifications(self, response):
        cert_items = response.css('li.artdeco-list__item.pvs-list__item--line-separated')
        certifications = []
        for item in cert_items:
            cert_loader = ItemLoader(item=CertificationItem(), selector=item)
            cert_loader.default_output_processor = TakeFirst()
            cert_loader.add_css('name', 'span.mr1.t-bold span[aria-hidden="true"]::text')
            cert_loader.add_css('issuer', 'span.t-14.t-normal span[aria-hidden="true"]::text')
            cert_loader.add_css('date', 'span.t-14.t-normal.t-black--light span[aria-hidden="true"]::text')
            certifications.append(cert_loader.load_item())
        return certifications

    def parse_volunteering(self, response):
        volunteering_items = response.css('section[aria-label="Volunteer experience"] li.artdeco-list__item')
        volunteering = []
        for item in volunteering_items:
            vol_loader = ItemLoader(item=VolunteeringItem(), selector=item)
            vol_loader.default_output_processor = TakeFirst()
            vol_loader.add_css('role', 'span.mr1.t-bold span[aria-hidden="true"]::text')
            vol_loader.add_css('organization', 'span.t-14.t-normal span[aria-hidden="true"]::text')
            vol_loader.add_css('date_range', 'span.t-14.t-normal.t-black--light span[aria-hidden="true"]::text')
            volunteering.append(vol_loader.load_item())
        return volunteering

    def parse_recommendations(self, response):
        recommendation_items = response.css('section[aria-label="Recommendations"] li.artdeco-list__item')
        recommendations = []
        for item in recommendation_items:
            rec_loader = ItemLoader(item=RecommendationItem(), selector=item)
            rec_loader.default_output_processor = TakeFirst()
            rec_loader.add_css('recommender', 'span.mr1.t-bold span[aria-hidden="true"]::text')
            rec_loader.add_css('relationship', 'span.t-14.t-normal span[aria-hidden="true"]::text')
            rec_loader.add_css('text', 'div.pvs-list__outer-container ul.pvs-list li span.visually-hidden::text')
            recommendations.append(rec_loader.load_item())
        return recommendations

    def random_delay(self):
        delay = random.uniform(3, 7)
        self.logger.info(f"Waiting for {delay:.2f} seconds before next request")
        time.sleep(delay)

    def error_handler(self, failure):
        self.logger.error(f"Request failed: {failure.request.url}")
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error(f"HttpError on {response.url}")
            self.logger.error(f"HttpError with response status {response.status}")
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error(f"DNSLookupError on {request.url}")
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error(f"TimeoutError on {request.url}")