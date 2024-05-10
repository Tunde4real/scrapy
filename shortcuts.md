# Global Commands

### scrapy startproject {project_name}
starts a new scrapy project

### scrapy genspider {spider_name} {site_domain}
generates a new spider based on predefined template

### scrapy shell
starts a scrapy shell

### scrapy shell {url}
E.g "scrapy shell 'https://quotes.toscrape.com/page/1/'" to examine a url for the html returned.

### scrapy view {url}
opens the url in a browser

### scrapy fetch {url}
downloads the html content returned on the url and save to stndard output

### scrapy bench
runs a quick benchmark test

### scrapy -h 
see all available commands

### scrapy {sommand} -h
see more information on a command



# Project only commands

### scrapy crawl spider_name
Runs spider file with name provided. The name of the spider can be without the ending .py. You must navigate to project directory to run

### scrapy crawl {spider name} -o {csv file name}
crawls a spider and add data into csv file provided without overwriting the already present data if any.

### scrapy crawl {spider name} -O {csv file name}
crawls a spider and add data into csv file, overwriting any data present in the csv file

### scrapy list
list all available spiders

