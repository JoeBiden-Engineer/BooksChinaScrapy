# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookschinaItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    free_shipping = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    one_star_price = scrapy.Field()
    three_star_price = scrapy.Field()
    discount = scrapy.Field()
    reader_ratings = scrapy.Field()
    rating_num = scrapy.Field()
    is_stock = scrapy.Field()
    level_1_category = scrapy.Field()
    level_2_category = scrapy.Field()
    publisher = scrapy.Field()
    publish_date = scrapy.Field()
    ranking = scrapy.Field()
    ranking_num = scrapy.Field()
    book_id = scrapy.Field()
