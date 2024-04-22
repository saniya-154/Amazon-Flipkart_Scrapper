# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

class ProductItem(scrapy.Item):
    source = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    no_of_ratings = scrapy.Field()
    offers = scrapy.Field()