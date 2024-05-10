
# import built-in modules
import os
import re
import string
from datetime import datetime

# import external module
import scrapy

""" Module documentation
"""


class DelawareSpider(scrapy.Spider):
    name = "delaware"
    allowed_domains = ["courtconnect.courts.delaware.gov"]
    start_urls = ["https://courtconnect.courts.delaware.gov/cc/cconnect/ck_public_qry_main.cp_main_idx"]

    def parse(self, response):
        pass
