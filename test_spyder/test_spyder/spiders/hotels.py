import scrapy


class HotelsSpider(scrapy.Spider):
    name = "hotels"
    allowed_domains = ["www.booking.com"]
    start_urls = ["https://www.booking.com/country.en-gb.html?"]
    custom_settings = {"FEED_FORMAT": "json", 
                       "FEED_URI": "hotels.json",
                       "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    
    def parse(self, response):
        countries = response.xpath('//*[@id="countryTmpl"]/div/div/h2/a/text()').extract()

        for country in countries:
            country = country.replace("\\n", "")
            full_link = f"https://www.booking.com/searchresults.en-gb.html?ss={country}"
            yield response.follow(full_link, self.parse_hotel)

    def parse_hotel(self, response):
        data = response.xpath('//*[@id="bodyconstraint-inner"]/div[2]/div/div[2]/div[3]/div[2]/div[1]/h1/text()').extract()

        yield {
            'num_hotels': data,
            'url': response.url
        }

