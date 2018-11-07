import scrapy


class PurePcSpider(scrapy.Spider):
    name = "purepc"
    start_urls = ["https://www.purepc.pl/node?page=300"]

    def parse(self, response):
        #extracts links from a website
        for href in response.xpath("//div[contains(@class, 'nl_item')]/h2/a/@href").extract():
            yield response.follow(href, self.paginate_articles)
        #handles pagination of a website
        next_page = response.xpath("//li[contains(@class, 'pager-next')]/a/@href").extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def paginate_articles(self, response):
        # handles pagination of a single article (if it has more than one page)
        page_menu = response.xpath('//div[@id="PageMenuList"]/ul/li/a/@href').extract()

        if not page_menu:
            yield self.parse_article(response)
        else:
            for page in page_menu:
                yield response.follow(page, self.parse_article)

    def parse_article(self, response):
        article_parts = response.xpath('//div[contains(@class, "content clear-block")]/p/text()').extract()

        return {
            "url": response.url,
            "text": "\n".join(article_parts)
        }
