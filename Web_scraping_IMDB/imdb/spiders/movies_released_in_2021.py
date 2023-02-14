import scrapy
import regex 
import re


class MoviesReleasedIn2020Spider(scrapy.Spider):
    name = "movies-released-in-2021"
    allowed_domains = ["www.imdb.com"]
    start_urls = [
        "https://www.imdb.com/search/title/?title_type=feature&release_date=2021-01-01,2022-01-01&runtime=1,&sort=release_date,asc&count=250"]
    current_page = 1

    def parse(self, response):
        movies_el = response.css("div.lister-item > .lister-item-content")
        year_pattern = re.compile(r'\(.*?(\d+).*\)')

        for movie_el in movies_el:
            title = movie_el.css('.lister-item-header a::text').get()

            try:
                year = movie_el.css('.lister-item-header > .lister-item-year::text').get()
                year = year_pattern.findall(year)[0]
            except:
                year = None

            try:
                duration = movie_el.css('p:nth-of-type(1) > span.runtime::text').get().split()[0]
            except:
                duration = None

            try:
                genre = movie_el.css('p:nth-of-type(1) > span.genre::text').get().strip()
            except:
                genre = None

            try:
                rating = movie_el.css('.ratings-bar > .ratings-imdb-rating > strong::text').get()
            except:
                rating = None

            try:
                synopsis = movie_el.css('p:nth-of-type(2)::text').get().strip()
            except:
                synopsis = None

            people_raw = ''.join([x.strip() for x in movie_el.css('p:nth-of-type(3) *::text').getall()])
            people_raw_split = people_raw.split('|')

            try:
                directors = people_raw_split[0].split(':')[1]
            except:
                directors = None

            try:
                stars = people_raw_split[1].split(':')[1]
            except:
                stars = None

            yield {
                'title': title,
                'year': year,
                'duration': duration,
                'genre': genre,
                'rating': rating,
                'synopsis': synopsis,
                'directors': directors,
                'stars': stars
            }

            next_page = response.css('.next-page')
            if next_page and self.current_page < 3:
                self.current_page += 1
                yield response.follow(next_page[0])

                
