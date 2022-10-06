import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from goodreads.items import BookItem

class GoodreadsSpider(scrapy.Spider):
    name = "goodreads"

    def __init__(self, base_url, books_page_count, quotes_page_count):
        self.start_urls = list(base_url+str(i+1) for i in range(int(books_page_count)))
        self.quotes_page_count = int(quotes_page_count)

    def parse(self, response):
        book_links = response.css('a.bookTitle::attr(href)').getall()
        yield from response.follow_all(book_links, self.parse_book)

    def parse_book(self, response):
        loader = ItemLoader(BookItem(), response=response)
        title = response.css('#bookTitle::text').get()
        
        # The book page has two distinct HTML templates that can be served by the server due to an ongoing website change
        # They include completly different selectors, therefore we need to differentiate and handle each format differently
        if title == None:
            # First template
            quote_link = response.css('a.DiscussionCard::attr(href)').get()
            loader.add_css('title', 'h1.Text__title1::text', TakeFirst())
            loader.add_css('author', 'span.ContributorLink__name::text', TakeFirst())
            loader.add_css('rating', 'div.RatingStatistics__rating::text')
            loader.add_value('ISBN', response.css('script::text').re_first('(?<=isbn":")\d*'))
            genres = response.css('span.BookPageMetadataSection__genreButton > a > span::text').getall()
            loader.add_value('genres', genres)
            loader.add_value('pageCount', response.css('p[data-testid="pagesFormat"]::text').get().split(',')[0])

            yield response.follow(quote_link, meta={'book_loader': loader, 'quotes_list': [], 'n_page': 1}, callback=self.parse_quotes)
        else:
            # Second template
            quote_link = response.xpath("//a[re:test(.//text(), 'quotes from', 'i')]/@href").get()

            loader.add_value('title', title)
            loader.add_css('author', 'a.authorName > span::text', TakeFirst())
            loader.add_css('rating', 'span[itemprop="ratingValue"]::text')
            loader.add_css('pageCount', 'span[itemprop="numberOfPages"]::text')
            loader.add_xpath('ISBN', '//div[@class="infoBoxRowTitle"][text()="ISBN"]/following-sibling::div/text()', TakeFirst())

            genres = response.css('a.bookPageGenreLink::text').getall()
            loader.add_value('genres', list(dict.fromkeys(genres)))
            yield response.follow(quote_link, meta={'book_loader': loader, 'quotes_list': [], 'n_page': 1}, callback=self.parse_quotes)
    
    def parse_quotes(self, response):
        quotes_list = response.meta['quotes_list']
        quotes = response.css('div.quoteDetails')
        
        for quote in quotes:
            text = "".join(quote.css('div.quoteText::text').getall())
            tags = quote.css('div.quoteFooter > div.left > a::text').getall()
            likes = quote.css('div.quoteFooter > div.right >a::text').get()
            quotes_list.append({
                'text': text,
                'tags': tags,
                'likes': likes
            })

        loader = response.meta['book_loader']
        next_page_href = response.css('a.next_page::attr(href)').get()
        if response.meta['n_page'] >= self.quotes_page_count or not next_page_href:
            loader.add_value('quotes', quotes_list)
            yield loader.load_item()
        else:
            yield response.follow(next_page_href, meta={'book_loader': loader, 'quotes_list': quotes_list, 'n_page': response.meta['n_page']+1 }, callback=self.parse_quotes)