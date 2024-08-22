import scrapy


class EntertainmentSpider(scrapy.Spider):
    name = "entertainment"
    allowed_domains = ["www.civitatis.com"]
    start_urls = ["https://www.civitatis.com/en/"]
    countries = ['united-states', 
                 'france',
                 'united-kingdom',
                 'morocco',
                 'italy',
                 'iceland',
                 'jordan',
                 'netherlands',
                 'peru',
                 'egypt',
                 'greece',
                 'spain',
                 'france',
                 'colombia',
                 'slovakia',
                 'belgium',
                 'hungary',
                 'mexico',
                 'denmark',
                 'ireland',
                 'croatia',
                 'jamaica',
                 'norway',
                 'brazil',
                 'ecuador',
                 'cuba',
                 'vietnam',
                 'switzerland',
                 'turkey',
                 'rwanda',
                 'poland',
                 'malaysia',
                 'japan',
                 'portugal',
                 'argentina',
                 'germany',
                 'panama',
                 'dominican-respublic',
                 'chile',
                 'south-korea',
                 'bulgaria',
                 'georgia',
                 'tunisia',
                 'austria', 
                 'ukraine',
                 'poland']
    custom_settings = {"FEED_FORMAT": "json", 
                       "FEED_URI": "entertainment.json",
                       "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    def parse(self, response):
        for country in self.countries:
            link = f"{self.start_urls[0]}{country}"
            yield response.follow(link, self.parse_entertainment, meta={'country': country})

    def parse_entertainment(self, response):
        attraction = response.xpath('//*[@id="civ-main-element"]/header/div[2]/div/div[2]/span[1]/text()').extract()
        impression = response.xpath('//*[@id="civ-main-element"]/header/div[2]/div/div[4]/span[2]/text()').extract()
        country = response.meta['country']

        yield{
            'attraction': attraction,
            'impression': impression,
            'country': country
        }