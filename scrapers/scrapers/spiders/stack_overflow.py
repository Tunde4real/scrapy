# import system module
from typing import Any

# import external module
import scrapy


""" Module documentation
""" 

data = {}


class StackOverflowSpider(scrapy.Spider):
    name = "stack-overflow"
    allowed_domains = ["stackoverflow.com"]
    # start_urls = [f"https://stackoverflow.com/users{i}" for i in range(1, 675997)]
    # start_urls = ['https://stackoverflow.com/users?page=1&tab=reputation&filter=all']
    start_urls = ['https://stackoverflow.com/users?tab=Reputation&filter=week']
    # start_urls = ['https://stackoverflow.com/users?tab=Reputation&filter=year']
    

    def __init__(self, name: str | None = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        self.previous_page = ''
        self.page = 1


    # def start_requests(self):
    #     # alter the user agent's platform with new custom headers
    #     custom_headers = {
    #         "Sec-Ch-Ua-Platform": "\"Linux\"",
    #         "User-Agent": "Mozilla/5.0 (Linux; x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    #         }
    #     for url in self.start_urls:
    #         yield scrapy.Request(url, headers=custom_headers, callback=self.parse, meta={"proxy": "http://51.89.255.67"})
 


    def parse(self, response):
        """
        """
        for user in response.xpath('//*[@id="user-browser"]/div[1]/div'): #.getall() here will return a str of all elements
            profile_link = user.css('a::attr("href")').get()
            # name = user.xpath('div[2]/a/text()').get().strip()
            name, location = user.xpath('div[2]/text()').get().strip().split('\n')
            location = user.xpath('div[2]/span/text()').get()
            if location != None: location = location.strip()
            data[response.urljoin(profile_link)] = [name, location]
            self.logger.info(f'Scraping for user {profile_link}')
            yield response.follow(profile_link, callback=self.parse_user)
        
        pages = [0] + response.xpath('//*[@id="user-browser"]/div[2]/a/@href')
        if pages[-1] != 0:
            next_page_url = pages[-1].get()
            if next_page_url != self.previous_page:
                self.logger.info(f"Going to page {self.page+1} - {next_page_url}")
                self.previous_page = next_page_url
                self.page += 1
                yield response.follow(pages[-1], callback=self.parse)

    
    def parse_user(self, response):
        """
        """
        tags = ''
        # name = response.xpath('//*[@id="mainbar-full"]/div[1]/div[1]/div/div[1]/div[1]/text()').get().strip()
        membership = response.xpath('//*[@id="mainbar-full"]/div[1]/div[1]/div/ul[1]/li[1]/div/div[2]/span/text()').get().strip()
        # if self.location == None: self.location = response.xpath('//*[@id="mainbar-full"]/div[1]/div[1]/div/ul[2]/li[2]/div/div[2]/text()').get()
        # if self.location != None: self.location = self.location.strip()
        name, location = data[response.url]
        reputation = response.xpath('//*[@id="stats"]/div[2]/div/div[1]/div/text()').get().strip()
        reached = response.xpath('//*[@id="stats"]/div[2]/div/div[2]/div/text()').get().strip()
        answers = response.xpath('//*[@id="stats"]/div[2]/div/div[3]/div/text()').get().strip()
        questions = response.xpath('//*[@id="stats"]/div[2]/div/div[4]/div/text()').get().strip()
        gold_badges = response.xpath('//*[@id="main-content"]/div/div[2]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[1]/text()').get()
        silver_badges = response.xpath('//*[@id="main-content"]/div/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[1]/text()').get()
        bronze_badges = response.xpath('//*[@id="main-content"]/div/div[2]/div/div[2]/div[2]/div[3]/div/div[1]/div[2]/div[1]/text()').get()
        if gold_badges != None: gold_badges = gold_badges.strip()
        if silver_badges != None: silver_badges = silver_badges.strip()
        if bronze_badges != None: bronze_badges = bronze_badges.strip()
        tags_ = response.xpath('//*[@id="top-tags"]/div[2]/div')
        for tag in tags_:
            name = tag.xpath('div/div/a/text()').get().strip()
            score = tag.xpath('div/div[2]/div/div/div/text()').get().strip()
            tags += f'{name} {score},'
        yield{
            "Profile Link" : response.url,
            "Name" : name,
            "Membership" : membership,
            "Location" : location,
            "Reputation" : reputation,
            "Reached" : reached,
            "Answers" : answers,
            "Questions" : questions,
            "Gold Badges" : gold_badges,
            "Silver Badges" : silver_badges,
            "Bronze Badges" : bronze_badges,
            "Tags" : tags
        }
