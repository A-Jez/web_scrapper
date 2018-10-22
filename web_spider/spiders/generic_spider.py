from scrapy import Spider, Request


class GenericSpider(Spider):
    name="generic"

    def start_requests(self):
        yield Request(url='https://www.fmi.pk.edu.pl')
    
    def parse(self, response):
        data = []
        for child in response.xpath('//div[contains(@id, "dvh")]/div[contains(@mytype, "news")]'):
            match = child.xpath('string(.)').extract_first().strip()
            time, text = match.split(' \n ')
            data.append({ "time": time, "text": text })
        return data
