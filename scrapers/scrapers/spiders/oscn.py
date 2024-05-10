import scrapy


''' Module documentation
'''


class OscnSpider(scrapy.Spider):
    name = "oscn"
    allowed_domains = ["www.oscn.net"]
    start_urls = ["https://www.oscn.net/dockets/Search.aspx"]

    def parse(self, response):
        pass
