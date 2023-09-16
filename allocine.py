import requests_html

start_crawl_page = "https://www.allocine.fr/film/aucinema/"
css_selector_movie_url = "h2.meta-title a.meta-title-link"
css_selector_crawl_more = "nav.pagination.cf div.pagination-item-holder a.button.button-md.item"

container_page_urls = []
container_movie_urls = []
container_movie_info = []