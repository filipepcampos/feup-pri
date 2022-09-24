import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from goodreads.items import BookItem

BASE_URL = 'https://www.goodreads.com/list/show/1.Best_Books_Ever?page='
N_PAGES = 2

class GoodreadsSpider(scrapy.Spider):
    name = "goodreads"
    start_urls = list(BASE_URL+str(i+1) for i in range(2))

    def parse(self, response):
        book_links = response.css('a.bookTitle::attr(href)').getall()
        yield from response.follow_all(book_links, self.parse_book)

    def parse_book(self, response):
        loader = ItemLoader(BookItem(), response=response)
        title = response.css('#bookTitle::text').get()
        
        if title == None:
            #fmt 1
            quote_link = response.css('a.DiscussionCard::attr(href)').get()
            loader.add_css('title', 'h1.Text__title1::text', TakeFirst())
            loader.add_css('author', 'span.ContributorLink__name::text', TakeFirst())

            yield response.follow(quote_link, meta={'book_loader': loader}, callback=self.parse_quotes)
        else:
            #fmt 2
            quote_link = response.xpath("//a[re:test(.//text(), 'quotes from', 'i')]/@href").get()

            loader.add_value('title', title)
            loader.add_css('author', 'a.authorName > span::text', TakeFirst()),
            yield response.follow(quote_link, meta={'book_loader': loader}, callback=self.parse_quotes)
    
    def parse_quotes(self, response):
        quotes_list = []
        quotes = response.css('div.quoteDetails')
        
        for quote in quotes:
            text = "".join(quote.css('div.quoteText::text').getall())
            source = "".join(quote.css('.authorOrTitle::text').getall())
            tags = quote.css('div.quoteFooter > div.left > a::text').getall()
            likes = quote.css('div.quoteFooter > div.right >a::text').get()
            quotes_list.append({
                'text': text,
                'source': source,
                'tags': tags,
                'likes': likes
            })

        loader = response.meta['book_loader']
        loader.add_value('quotes', quotes_list)
        yield loader.load_item()
