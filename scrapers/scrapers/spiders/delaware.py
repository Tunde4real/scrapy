# import built-in modules
import os
import re
import string
from datetime import datetime

# import third party modules
import pandas as pd
from scrapy import Spider
from scrapy.loader import ItemLoader
# from delaware.items import CaseItem, PartiesItem

""" Module documentation
"""


# class DelawareSpider(scrapy.Spider):
#     name = "delaware"
#     allowed_domains = ["courtconnect.courts.delaware.gov"]
#     start_urls = ["https://courtconnect.courts.delaware.gov/cc/cconnect/ck_public_qry_main.cp_main_idx"]

#     def parse(self, response):
#         pass

# -- coding: utf-8 -
# Written by Ibrahim Aderinto


class DelawareDocketSpider(Spider):

    # The spider name is how the spider is located (and instantiated) by Scrapy, so it must be unique
    name = 'delaware_docket'    # has to be unique for every project. 
    allowed_domains = ['courtconnect.courts.delaware.gov']
    alphabets = string.ascii_lowercase
    start_urls = [
                    f'https://courtconnect.courts.delaware.gov/cc/cconnect/ck_public_qry_cpty.cp_personcase_srch_details?
                    backto=P&soundex_ind=&partial_ind=checked&last_name={i}&first_name=&middle_name=&begin_date=&end_date=
                    &case_type=ALL&id_code=&PageNo=1'\
                    for i in alphabets
                ]
    
    
    def __init__(self):
        super().__init__()
        # self.seen_cases = []
        self.seen_cases = set(pd.read_csv(os.path.abspath(os.pardir)+'\delaware\docket.csv')['Id'].to_list())
        print(len(self.seen_cases))
        self.parties_csv = open('parties.csv', 'a', encoding='utf-8')
        # self.parties_csv.write('case_id,party_id,party_type,party_name,party_address\n')


    def parse(self, response):
        rows = response.css('table')[1].css('tr')
        for row in rows[1:]:
            case_id = row.css('a::text').get()
            if case_id in self.seen_cases:
                continue
            # scrapy.Requests did not work here for unknown reason
            yield response.follow(f'https://courtconnect.courts.delaware.gov/cc/cconnect/ck_public_qry_doct.cp_dktrpt_docket_report?backto=P&case_id={case_id}&begin_date=&end_date=',\
                                self.parse_case_page)
            self.seen_cases.add(case_id)
        
        next_page = response.css('a[target="Big"]::attr("href")')[-1].get()
        if next_page is not None:
            # response.follow can also accept a tag object or a css locator as in the example below
            # yield from response.follow_all(css='ul.pager a', callback=self.parse) 
            yield response.follow('https://courtconnect.courts.delaware.gov/cc/cconnect/'+next_page, callback=self.parse)
    

    def parse_case_page(self, response):
        '''
        
        '''

        def remove_newline_char(string):
            return string.replace('\n', ' ')
        
        def parse_date(date):
            date = date.lower().strip()
            months = {
                        'january':'01',
                        'february':'02',
                        'march':'03',
                        'april':'04',
                        'may':'05',
                        'june':'06',
                        'july':'07',
                        'august':'08',
                        'september':'09',
                        'october':'10',
                        'november':'11',
                        'december':'12'
                        }
            month = ''
            for i in months:
                if i in date:
                    month = months[i]
            day = re.findall('[0-9]{2}[a-z]', date)[0][:-1]
            year = date[-4:]
            return f'{day}-{month}-{year}'

        tables = response.css('table')
        description_table = tables[1]
        for table in tables[2:]:    # get parties table
            if 'party end date' in table.get().lower():
                parties_table = table
        description_table_rows = description_table.css('tr')

        # case table variables
        case_id = response.css('table')[0].css('td::text')[1].get().strip()
        case_description = remove_newline_char(description_table_rows[0].css('td::text')[1].get().strip())
        date_filled = description_table_rows[1].css('td::text')[1].get()
        case_type = description_table_rows[2].css('td::text')[2].get().strip()
        case_status = description_table_rows[3].css('td::text')[2].get().strip()

        # case_loader = ItemLoader(item = CaseItem())
        # case_loader.add_value('case_id', case_id)
        # case_loader.add_value('case_description', case_description)
        # case_loader.add_value('date_filled', date_filled)
        # case_loader.add_value('case_type', case_type)
        # case_loader.add_value('case_status', case_status)
        # yield case_loader.load_item()

        parties_table_rows = parties_table.css('tr')

        x = 0
        # parties_loader = ItemLoader(item = PartiesItem())
        for row in parties_table_rows[1:]:
            if x==0:
                party_type = row.css('td::text').getall()[3]
                party_id = row.css('a::text').get()
                party_name = row.css('b::text').get().strip()

                # parties_loader.add_value('case_id', case_id) 
                # parties_loader.add_value('party_id', party_id)
                # parties_loader.add_value('party_type', party_type)
                # parties_loader.add_value('party_name', party_name)

            elif x==1:
                try:
                    party_address = row.xpath('td/i/text()').get().replace('\n', ' ')
                    if str(party_address).lower() == 'none':
                        row_source = row.css('td')[1].get()
                        party_address = re.sub(r'<.+>', ' ', row_source).replace('\n', ' ').strip()
                except:
                    row_source = row.css('td')[1].get()
                    party_address = re.sub(r'<.+>', ' ', row_source).replace('\n', ' ').strip()
                # parties_loader.add_value('party_address', party_address)
                # yield parties_loader.load_item()
                
                # parties_loader = ItemLoader(item = PartiesItem())

                self.parties_csv.write(f'{case_id}|{party_id}|{party_type}|{party_name}|{party_address}\n')
            elif x == 2:
                x = 0
                continue
            x += 1

        yield{
            'Id' : case_id,
            'Description' : remove_newline_char(case_description).split(' - ')[1].strip(),
            'Date Filled' : parse_date(remove_newline_char(date_filled)),
            'Type' : remove_newline_char(case_type),
            'Status' : remove_newline_char(case_status)
        }
