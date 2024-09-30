import scrapy


class StackOverflowQaSpider(scrapy.Spider):
    name = "stack_overflow_qa"
    allowed_domains = ["stackoverflow.com"]
    start_urls = ["https://stackoverflow.com/questions?tab=Newest"]

    def parse(self, response):
        pass
