# # Scrapy settings for linkedin_scraper project
# #
# # For simplicity, this file contains only settings considered important or
# # commonly used. You can find more settings consulting the documentation:
# #
# #     https://docs.scrapy.org/en/latest/topics/settings.html
# #     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# #     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# BOT_NAME = "linkedin_scraper"

# SPIDER_MODULES = ["linkedin_scraper.spiders"]
# NEWSPIDER_MODULE = "linkedin_scraper.spiders"


# # Crawl responsibly by identifying yourself (and your website) on the user-agent
# #USER_AGENT = "linkedin_scraper (+http://www.yourdomain.com)"

# # Obey robots.txt rules
# ROBOTSTXT_OBEY = False

# # Configure maximum concurrent requests performed by Scrapy (default: 16)
# #CONCURRENT_REQUESTS = 32

# # Configure a delay for requests for the same website (default: 0)
# # See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# # See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3

# # Enable and configure the AutoThrottle extension
# AUTOTHROTTLE_ENABLED = True
# AUTOTHROTTLE_START_DELAY = 5
# AUTOTHROTTLE_MAX_DELAY = 60
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# # The download delay setting will honor only one of:
# #CONCURRENT_REQUESTS_PER_DOMAIN = 16
# #CONCURRENT_REQUESTS_PER_IP = 16

# # Disable cookies (enabled by default)
# #COOKIES_ENABLED = False
# # Override the default request headers

# # ... (previous settings remain the same)

# DOWNLOADER_MIDDLEWARES = {
#     'linkedin_scraper.middlewares.LinkedinAuthMiddleware': 543,
#     'linkedin_scraper.middlewares.RotateUserAgentMiddleware': 400,
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
# }

# USER_AGENT_LIST = [
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47',
#     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
# ]

# # Proxy settings (if you decide to use proxies)
# # PROXY_POOL_ENABLED = True
# # PROXY_POOL_BAN_POLICY = 'linkedin_scraper.policy.BanDetectionPolicyNotText'
# DEFAULT_REQUEST_HEADERS = {
#    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#    'Accept-Language': 'en',
#    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
# }

# # Configure item pipelines
# ITEM_PIPELINES = {
#    'linkedin_scraper.pipelines.LinkedinScraperPipeline': 300,
# }

# # Enable and configure HTTP caching
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# # Disable Telnet Console (enabled by default)
# #TELNETCONSOLE_ENABLED = False

# # Override the default request headers:
# #DEFAULT_REQUEST_HEADERS = {
# #    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
# #    "Accept-Language": "en",
# #}

# # Enable or disable spider middlewares
# # See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# #SPIDER_MIDDLEWARES = {
# #    "linkedin_scraper.middlewares.LinkedinScraperSpiderMiddleware": 543,
# #}

# # Enable or disable downloader middlewares
# # See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# #DOWNLOADER_MIDDLEWARES = {
# #    "linkedin_scraper.middlewares.LinkedinScraperDownloaderMiddleware": 543,
# #}

# # Enable or disable extensions
# # See https://docs.scrapy.org/en/latest/topics/extensions.html
# #EXTENSIONS = {
# #    "scrapy.extensions.telnet.TelnetConsole": None,
# #}

# # Configure item pipelines
# # See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# #ITEM_PIPELINES = {
# #    "linkedin_scraper.pipelines.LinkedinScraperPipeline": 300,
# #}
# PROXY_POOL_ENABLED = True
# PROXY_POOL_BAN_POLICY = 'linkedin_scraper.policy.BanDetectionPolicyNotText'
# # Enable and configure the AutoThrottle extension (disabled by default)
# # See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# #AUTOTHROTTLE_ENABLED = True
# # The initial download delay
# #AUTOTHROTTLE_START_DELAY = 5
# # The maximum download delay to be set in case of high latencies
# #AUTOTHROTTLE_MAX_DELAY = 60
# # The average number of requests Scrapy should be sending in parallel to
# # each remote server
# #AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# # Enable showing throttling stats for every response received:
# #AUTOTHROTTLE_DEBUG = False

# # Enable and configure HTTP caching (disabled by default)
# # See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# #HTTPCACHE_ENABLED = True
# #HTTPCACHE_EXPIRATION_SECS = 0
# #HTTPCACHE_DIR = "httpcache"
# #HTTPCACHE_IGNORE_HTTP_CODES = []
# #HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# # Set settings whose default value is deprecated to a future-proof value
# REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
# FEED_EXPORT_ENCODING = "utf-8"



# Scrapy settings for linkedin_scraper project

BOT_NAME = "linkedin_scraper"

SPIDER_MODULES = ["linkedin_scraper.spiders"]
NEWSPIDER_MODULE = "linkedin_scraper.spiders"

# Obey robots.txt rules (set to False for scraping LinkedIn)
ROBOTSTXT_OBEY = False

# Set download delay to avoid getting banned (LinkedIn may throttle requests)
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True  # Random delay between requests

# Enable AutoThrottle for dynamic delays based on the server's response time
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5  # Initial delay
AUTOTHROTTLE_MAX_DELAY = 60   # Max delay in case of high latencies
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0  # Average requests in parallel
AUTOTHROTTLE_DEBUG = False  # Set to True to see throttling in action

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8  # Reduce to avoid LinkedIn rate-limiting

# Rotate user agents to mimic real traffic
DOWNLOADER_MIDDLEWARES = {
    'linkedin_scraper.middlewares.LinkedinAuthMiddleware': 543,
    'linkedin_scraper.middlewares.RotateUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,  # Enable retry
    'scrapy_proxies.RandomProxy': 740,  # Enable proxy rotation
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
}

# User-agent list to rotate from
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
]

# Default headers to mimic browser behavior
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en',
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

# Proxy settings for rotating proxies to prevent bans
PROXY_POOL_ENABLED = True
PROXY_POOL_BAN_POLICY = 'linkedin_scraper.policy.BanDetectionPolicyNotText'
PROXY_LIST = '/path/to/proxy/list.txt'  # List of proxies (can be local or remote)

# Retry settings to handle failed requests and banned proxies
RETRY_ENABLED = True
RETRY_TIMES = 5  # Retry 5 times for a failed request
RETRY_HTTP_CODES = [403, 429]  # Retry on forbidden (403) and too many requests (429)

# Enable caching to reduce load and avoid re-fetching data
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0  # Cache forever (useful for development)
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = [403, 429]  # Ignore cache for banned responses
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Enable Telnet Console for debugging
TELNETCONSOLE_ENABLED = False

# Enable logging to monitor scraper activity
LOG_ENABLED = True
LOG_LEVEL = 'INFO'

# Export settings
FEED_EXPORT_ENCODING = 'utf-8'

# Twisted reactor settings
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
