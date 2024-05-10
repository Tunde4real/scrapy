# Global Commands
# ...
start a new scrapy project
```console 
scrapy startproject {project_name}
```

generate a new spider based on predefined template
```console
scrapy genspider {spider_name} {site_domain}
```

start a scrapy shell
```console 
scrapy shell
```

to examine a url for the html returned.
```console
scrapy shell {url}
```

open the url in a browser
```console
scrapy view {url}
```

download the html content returned on the url and save to stndard output
```console
scrapy fetch {url}
```

see all available commands
```console
scrapy -h
```

see more information on a command
```console
scrapy {sommand} -h
```

run a quick benchmark test
```console
scrapy bench
```
# ...
# ...
# ...
# Project only commands

Run spider file with name provided. The name of the spider can be without the ending .py. You must navigate to project directory to run
```console
scrapy crawl spider_name
```

crawls a spider and add data into csv file provided without overwriting the already present data if any.
```console
scrapy crawl {spider name} -o {csv file name}
```

crawls a spider and add data into csv file, overwriting any data present in the csv file
```console 
crapy crawl {spider name} -O {csv file name}
```

list all available spiders
```console
scrapy list
```

