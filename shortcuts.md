# Global Commands
# ...
starts a new scrapy project ```console 
scrapy startproject {project_name}
```

```console
scrapy genspider {spider_name} {site_domain}
```
generates a new spider based on predefined template

```console 
scrapy shell
```
starts a scrapy shell

```console
scrapy shell {url}
```
to examine a url for the html returned.

```console
scrapy view {url}
```
opens the url in a browser

```console
scrapy fetch {url}
```
downloads the html content returned on the url and save to stndard output

```console
scrapy bench
```
runs a quick benchmark test

```console
scrapy -h
```
see all available commands

```console
scrapy {sommand} -h
```
see more information on a command
# ...
# ...
# ...
# Project only commands

```console
scrapy crawl spider_name
```
Runs spider file with name provided. The name of the spider can be without the ending .py. You must navigate to project directory to run

```console
scrapy crawl {spider name} -o {csv file name}
```
crawls a spider and add data into csv file provided without overwriting the already present data if any.

```console 
crapy crawl {spider name} -O {csv file name}
```
crawls a spider and add data into csv file, overwriting any data present in the csv file

```console
scrapy list
```
list all available spiders

