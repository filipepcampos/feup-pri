import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Join


class BookItem(scrapy.Item):
    title = scrapy.Field(
        input_processor = MapCompose(lambda s : s.strip()),
        output_processor = TakeFirst()
    )
    author = scrapy.Field(
        input_processor = MapCompose(lambda s : s.strip()),
        output_processor = TakeFirst()
    )
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
    genres = scrapy.Field()
    quotes = scrapy.Field()