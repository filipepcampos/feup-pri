import scrapy
from itemloaders.processors import MapCompose, TakeFirst


class BookItem(scrapy.Item):
    title = scrapy.Field(
        input_processor = MapCompose(lambda s : s.strip()),
        output_processor = TakeFirst()
    )
    author = scrapy.Field(
        input_processor = MapCompose(lambda s : s.strip()),
        output_processor = TakeFirst()
    )
    quotes = scrapy.Field()