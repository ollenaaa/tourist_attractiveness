import scrapy
import re


class AirlinksSpider(scrapy.Spider):
    name = "airlinks"
    allowed_domains = ["www.flightconnections.com"]
    start_urls = ["https://www.flightconnections.com/airports-by-country"]
    custom_settings = {"FEED_FORMAT": "json", 
                       "FEED_URI": "airlinks.json",
                       "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    def parse(self, response):
        content = response.xpath("/html/body/div[2]/div[2]/ul/li/a")

        for link in content:
            full_link = f"https://www.flightconnections.com{link.xpath('@href').get()}"
            yield response.follow(full_link, self.parse_airlinks)

    def parse_airlinks(self, response):
        data = response.xpath("/html/body/div[2]/div[1]/div/div[2]/p/text()").extract()
        joined_data = ''.join(data)
        airlinks = re.search(r'\b\d+\b(?=\s+countries)', joined_data)[0]
        yield {
            'url': response.url,
            'airlinks': airlinks
        }