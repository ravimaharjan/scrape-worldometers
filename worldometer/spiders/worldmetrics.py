# -*- coding: utf-8 -*-
import scrapy
import logging


class WorldmetricsSpider(scrapy.Spider):
    name = 'worldmetrics'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        # country_anchor_elements = response.xpath('//table[@class="table table-striped table-bordered dataTable no-footer"]/tbody/tr/td/a')
        country_anchor_elements = response.xpath('//td/a')
        for element in country_anchor_elements:
            country_name = element.xpath('.//text()').get()
            country_url = element.xpath('.//@href').get()

            yield response.follow(url=country_url, callback=self.parse_country, meta={'country_name': country_name})

    def parse_country(self, response):
        country = response.request.meta['country_name']
        table_rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        for row in table_rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            change_rate = row.xpath(".//td[3]/text()").get()
            median_age = row.xpath(".//td[5]/text()").get()
            yield {
                'country': country,
                'year': year,
                'population': population,
                'change rate': change_rate,
                'median age' : median_age
            }
