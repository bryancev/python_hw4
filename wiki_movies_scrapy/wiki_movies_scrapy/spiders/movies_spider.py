import scrapy

class MoviesSpiderSpider(scrapy.Spider):
    name = "movies_spider"
    custom_settings = {'ROBOTSTXT_OBEY': False}

    def start_requests(self):
        URL = "https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B3%D0%BE%D0%B4%D0%B0%D0%BC"
        
        yield scrapy.Request(url = URL, callback=self.parse_pages_years)

    def parse_pages_years(self, response):
        years_movies =  response.css('div[class="CategoryTreeItem"] a::attr(href)').extract()
        for url_year in years_movies:
            url_year = response.urljoin('https://ru.wikipedia.org' + url_year)

            yield response.follow(url=url_year, callback=self.parse_pages_movies)     

    def parse_pages_movies(self, response):
        movies_on_page =  response.css('div[id="mw-pages"]  div[class="mw-category-group"]  li a::attr(href)').extract()
        for url_movie in movies_on_page:
            url_movie = response.urljoin('https://ru.wikipedia.org' + url_movie)

            yield response.follow(url=url_movie, callback=self.parse_movie)

        next_page = response.css('div[id="mw-pages"] > a:last-of-type::attr(href)').extract()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse_pages_movies)

    def parse_movie(self, response):
         yield {
                'title'     : response.css('span[class="mw-page-title-main"]::text').extract_first(),
                'genre'     : response.css('td > span[data-wikidata-property-id="P136"] a::attr(title)').extract_first(),
                'producer'  : response.css('td > span[data-wikidata-property-id="P57"] a::attr(title)').extract_first(),
                'country'   : response.css('td > span[data-wikidata-property-id="P495"] a::attr(title)').extract_first(),
                'year'      : response.css('span[class="dtstart"]::text').extract_first(),
                'rating_url': response.css('td > span[data-wikidata-property-id="P345"] a::attr(href)').extract_first()       
        }