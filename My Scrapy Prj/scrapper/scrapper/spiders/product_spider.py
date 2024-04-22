import scrapy
import json

class ProductSpider(scrapy.Spider):
    name = 'product_spider'
    #allowed_domains = ["amazon.in","flipkart.com"]
    
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'products.json'
    }

    def start_requests(self):
        product = input("Enter the product you want to search for: ")
        urls = [
            f'https://www.flipkart.com/search?q={product}',
            f'https://www.amazon.com/s?k={product}'
        ]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        if 'flipkart' in response.url:
            yield from self.parse_flipkart(response)
        elif 'amazon' in response.url:
            yield from self.parse_amazon(response)

    def parse_flipkart(self, response):
        products = response.css('.s-result-item')
        for product in products:
            yield {
                'source': 'flipkart',
                'name': product.css('a::text').get(),
                'price': product.css('div[class*="_30"]::text').get(),
                'no_of_ratings': product.css('span[class*="_38sUEc"]::text').get(),
                'offers': product.css('div[class*="_3Ay6Sb"]::text').get()
            }

        # Follow pagination link
        next_page = response.css('a._1LKTO3::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse_flipkart)

    def parse_amazon(self, response):
        products = response.css('.s-result-item')
        for product in products:
            yield {
                'source': 'amazon',
                'name': product.css('h2 a span::text').get(),
                'price': product.css('.a-price span[class*="a-offscreen"]::text').get(),
                'no_of_ratings': product.css('.a-link-normal span[class*="a-size-base"]::text').get(),
                'offers': product.css('.a-badge-text::text').get()
            }

        # Follow pagination link
        next_page = response.css('.a-last a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse_amazon)

    def closed(self, reason):
        flipkart_count = 0
        amazon_count = 0
        with open('products.json') as file:
            data = json.load(file)
            for item in data:
                if item['source'] == 'flipkart':
                    flipkart_count += 1
                elif item['source'] == 'amazon':
                    amazon_count += 1

        self.log(f'Total items scraped from Flipkart: {flipkart_count}')
        self.log(f'Total items scraped from Amazon: {amazon_count}')


