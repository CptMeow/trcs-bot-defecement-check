import datetime
import re
import scrapy
from langdetect import detect
from urllib.parse import urlparse
from .__init__ import BaseSpider

class AllSite(scrapy.Spider):
    name = 'allsite'
    start_urls = [
        'https://centralb.redcross.or.th',
        'https://centralb.redcross.or.th/sawangkanives',
        'https://somdej.or.th',
        'https://thaircy.redcross.or.th',
        'https://thaircy.redcross.or.th/thaircy100Anniversary',
        'https://plant.redcross.or.th',
        'https://youdee.redcross.or.th',
        'https://vb.redcross.or.th',
        'https://blooddonationthai.com',
        'https://rehab.redcross.or.th',
        'https://finance.redcross.or.th',
        'https://eyebankthai.redcross.or.th',
        'https://trcch.redcross.or.th',
        'https://hrtrcs.redcross.or.th',
        'https://jobtrc.redcross.or.th',
        'https://adminis.redcross.or.th',
        'https://trcroadsafety.redcross.or.th',
        'https://ncp.redcross.or.th/',
        'https://property.redcross.or.th',
        'https://www.redcross.or.th',
        'https://english.redcross.or.th',
        'https://covid19.redcross.or.th',
        'https://procurement.redcross.or.th',
        'https://it.redcross.or.th',
        'https://intranet.redcross.or.th',
        'https://elearning.redcross.or.th',
        'https://portal.redcross.or.th',
        'https://ebook.redcross.or.th',
        'https://clipping.redcross.or.th',
        'https://audit.redcross.or.th',
        'https://oim.redcross.or.th/',
        'https://chapternews.redcross.or.th',
        'https://strategy.redcross.or.th/',
        'https://thethairedcrosssociety.sharepoint.com/SitePages/สำนักกฎหมาย-สภากาชาดไทย.aspx',
        'https://khaolan.redcross.or.th'
    ]

    allowed_domains = [
        'centralb.redcross.or.th',
        'medcertificate.somdej.or.th',
        'centralb.redcross.or.th/sawangkanives',
        'somdej.or.th',
        'thaircy.redcross.or.th',
        'thaircy.redcross.or.th/thaircy100Anniversary',
        'plant.redcross.or.th',
        'youdee.redcross.or.th',
        'vb.redcross.or.th',
        'blooddonationthai.com',
        'rehab.redcross.or.th',
        'finance.redcross.or.th',
        'eyebankthai.redcross.or.th',
        'trcch.redcross.or.th',
        'hrtrcs.redcross.or.th',
        'jobtrc.redcross.or.th',
        'adminis.redcross.or.th',
        'trcroadsafety.redcross.or.th',
        'ncp.redcross.or.th',
        'property.redcross.or.th',
        'www.redcross.or.th',
        'english.redcross.or.th',
        'covid19.redcross.or.th',
        'procurement.redcross.or.th',
        'it.redcross.or.th',
        'intranet.redcross.or.th',
        'elearning.redcross.or.th',
        'portal.redcross.or.th',
        'ebook.redcross.or.th',
        'clipping.redcross.or.th',
        'audit.redcross.or.th',
        'oim.redcross.or.th',
        'chapternews.redcross.or.th',
        'strategy.redcross.or.th',
        'thethairedcrosssociety.sharepoint.com',
        'khaolan.redcross.or.th'
    ]

    def parse(self, response):

        for item in response.css('a'):
            exists = self.checkPageDuplicate(item, response)
            if exists and (exists not in self.UNIQUE_DATA):
                self.UNIQUE_DATA.add(exists)
                yield self.createRow(item, response)

        for next_page in response.css('a::attr(href)'):
            if self.validateRule(next_page,response):
                yield response.follow(next_page, callback=self.parse)