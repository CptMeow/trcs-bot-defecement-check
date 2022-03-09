# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from langdetect import detect
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
import re
import logging

class BaseSpider(Spider):
    # Do not give it a name so that it does not show up in the spiders list.
    # This contains only common functions.

    UNIQUE_DATA = set()

    UNIQUE_URL = set()
    
    ALLOW_PROTOCALS = [
        'http://', 'https://',
    ]

    DENY_PATH = [
        '\/ปฎิทิน\/', 'calendar', 'wp-content', '\?ical', 'events', '\?download'
    ]

    POLICY_PAGES = [
        'policy',
        'นโยบาย',
        'cookie'
    ]

    IGNORED_EXTENSIONS = [
        # images
        'mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif',
        'tiff', 'ai', 'drw', 'dxf', 'eps', 'ps', 'svg',

        # audio
        # 'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',

        # video
        # '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv',
        # 'm4a',

        # other
        'css', 'pdf', 'doc', 'exe', 'bin', 'rss', 'zip', 'rar', 'msi', 'docx', 'pptx', 'ppt', 'xlsx', 'xls', 'iso'
    ]

    def checkPageDuplicate(self, page, response):

        parsed_uri = urlparse(response.url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        text = "'text': " + str(page.css('text').get())
        target = "'target': " + str(page.css('a::attr(href), ::attr(onclick)').get())
        url = "'url': " + str(response.url)
        # exists = domain + css + id + name + text + url
        return domain + text + target + url
    
    def createRow(self, item, response):
        next_page = response.urljoin(item.get())
        parsed_uri = urlparse(next_page)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        return {
                'domain': domain,
                'text': str(item.css('::text').get()).replace("\r\n", "").replace("\n", "").replace("\r", "").replace("\t", "").replace(" ", ""),
                'target': str(item.css('a::attr(href), ::attr(onclick)').get()).replace("\r\n", "").replace("\n", "").replace("\r", "").replace("\t", "").replace(" ", ""),
                'url': response.url
            }

    def validateRule(self, next_page ,response, options=[]):
        exists = next_page.get()
        next_page = response.urljoin(exists)

        ALLOW_PROTOCALS = self.ALLOW_PROTOCALS if not 'ALLOW_PROTOCALS' in options else options['ALLOW_PROTOCALS']
        DENY_PATH = self.DENY_PATH if not 'DENY_PATH' in options else options['DENY_PATH']
        IGNORED_EXTENSIONS = self.IGNORED_EXTENSIONS if not 'IGNORED_EXTENSIONS' in options else options['IGNORED_EXTENSIONS']

        if next_page.lower().startswith(tuple(ALLOW_PROTOCALS)): 
            if not next_page.lower().endswith(tuple(IGNORED_EXTENSIONS)): 
                if not re.search("("+")|(".join(DENY_PATH)+")", next_page.lower()):
                    return True
                else:
                    logging.warning('\033[93mDENY PATH on %s\033[0m', next_page.lower())
                    return False
            else:
                logging.warning('\033[93mDENY EXTENSION on %s\033[0m', next_page.lower())
                return False
        else:
            logging.warning('\033[93mDENY PROTOCAL on %s\033[0m', next_page.lower())
            return False