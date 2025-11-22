# Scrapy settings for bookschina project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
BOT_NAME = "bookschina"

SPIDER_MODULES = ["bookschina.spiders"]
NEWSPIDER_MODULE = "bookschina.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "bookschina (+http://www.yourdomain.com)"

# Obey robots.txt rules

ROBOTSTXT_OBEY = False
# 调整日志级别，减少控制台输出量
LOG_LEVEL = 'INFO'  # 或设置为'WARNING'进一步减少输出
# 设置Scrapy可以同时发送的最大请求数
# 值为16表示Scrapy最多可以同时处理16个请求，提高爬取效率
CONCURRENT_REQUESTS = 16
#设置每个域名可以同时发送的最大请求数，值为n表示对于目标网站，Scrapy同一时间只会发送n个请求，降低对服务器的压力，避免被反爬
CONCURRENT_REQUESTS_PER_DOMAIN = 6
# 为同一网站的请求配置延迟，这里使用 2 到 5 之间的随机数作为延迟
DOWNLOAD_DELAY = random.uniform(0.8,2.0)
# Disable cookies (enabled by default)
COOKIES_ENABLED = True
COOKIES_DEBUG = False

# 在文件末尾添加MySQL数据库配置
MYSQL_HOST = 'localhost'
MYSQL_USER = ''
MYSQL_PASSWORD = ''
MYSQL_DATABASE = 'books_db'
MYSQL_PORT = 3306
CHARSET = 'utf8mb4'
# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   "bookschina.middlewares.BookschinaSpiderMiddleware": 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   "bookschina.middlewares.BookschinaDownloaderMiddleware": 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "bookschina.pipelines.BookschinaPipeline": 300,
   "bookschina.pipelines.MySQLPipeline": 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
# 初始下载延迟设置为2秒，低于默认值以提高效率
AUTOTHROTTLE_START_DELAY = 0.8
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# 目标并发数调整为5.0，基于之前的CONCURRENT_REQUESTS=32和每个域名5的设置
AUTOTHROTTLE_TARGET_CONCURRENCY = 5.0
# Enable showing throttling stats for every response received:
# 启用调试模式以便监控调整效果
AUTOTHROTTLE_DEBUG = True

# 添加下载超时设置
DOWNLOAD_TIMEOUT = 30
# 启用重试中间件并配置
RETRY_ENABLED = True
RETRY_TIMES = 3  # 失败时最多重试3次
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429] 

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"
