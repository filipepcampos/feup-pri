import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Join


class BookItem(scrapy.Item):
    title = scrapy.Field(
        input_processor = MapCompose(lambda s : s.strip()),
        output_processor = TakeFirst()
    )
    authors = scrapy.Field()
    ISBN = scrapy.Field(
        input_processor = MapCompose(lambda s : s.strip()),
        output_processor = TakeFirst()
    )
    rating = scrapy.Field(
        input_processor = MapCompose(lambda s : s.strip()),
        output_processor = TakeFirst()
    )
    pageCount = scrapy.Field(
        input_processor = MapCompose(lambda s : s.strip()),
        output_processor = TakeFirst()
    )
    url = scrapy.Field(
        output_processor = TakeFirst()
    )
    description = scrapy.Field(
        input_processor = MapCompose(lambda s : s.strip()),
        output_processor = TakeFirst()
    )
    genres = scrapy.Field()
    quotes = scrapy.Field()