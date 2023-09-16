import requests_html
import re

start_crawl_page = "https://www.allocine.fr/film/aucinema/"
css_selector_movie_url = "h2.meta-title a.meta-title-link"
css_selector_crawl_more = "nav.pagination.cf div.pagination-item-holder a.button.button-md.item"
css_selector_page_title = "div.titlebar.titlebar-page div.titlebar-titl"
css_selector_casting_url = "a[title='Casting']"
css_selector_presse_rating = "div.rating-holder.rating-holder-3 div.rating-item div.rating-item-content div.stareval.stareval-medium.stareval-theme-default span.stareval-note"
css_selector_public_rating = "div.rating-holder.rating-holder-3 div.rating-item div.rating-item-content div.stareval.stareval-medium.stareval-theme-default span.stareval-note"
css_selector_ratings = "div.rating-item-content"
css_selector_original_title = "div.meta div.meta-body div.meta-body-item span.light"
css_selector_synopsis = "section#synopsis-details div.content-txt"
css_selector_cities = "div.gd-col-left section.section.ovw div.mdl-more.gd.small-crop"
css_selector_date = "div.meta div.meta-body div.meta-body-item.meta-body-info a.xXx.date.blue-link"
css_selector_meta = "div.meta div.meta-body div.meta-body-item.meta-body-info"
css_selector_directors = "section.section.casting-director a.meta-title-link"
css_selector_writers = "div.section.casting-list-gql a.xXx.item.link"
css_selector_actors = "section.section.casting-actor a.meta-title-link, section.section.casting-actor a.item.link"
css_sound_track = "div.section.casting-list-gql a.item.link"
css_public_critic_url = "a[title='Critiques spectateurs']"
css_pro_critic_url = "a[title='Critiques presse']"
css_note = "div.big-note span.note"


container_page_urls = []
container_movie_urls = []
container_movie_info = []


def initialization():
    session = requests_html.HTMLSession()
    page = session.get(start_crawl_page)
    movie_links = page.html.find(css_selector_movie_url)
    movie_urls = [list(x.absolute_links)[0] for x in movie_links]
    other_movies = page.html.find(css_selector_crawl_more)
    other_movie_urls = [list(x.absolute_links)[0] for x in other_movies]
    session.close()


def movie_scraping(url):
    session = requests_html.HTMLSession()
    page = session.get(url)
    title = page.html.find(css_selector_page_title)
    ratings = page.html.find(css_selector_public_rating)
    casting_url = page.html.find(css_selector_casting_url)
    meta = page.html.find(css_selector_meta)
    date = re.findall(".+(?=en salle)", meta.text)[0].strip()
    time = re.findall("/(.+?)/", meta.text)[0].strip()
    genre = re.findall("/(.+?)/(.+)", meta.text)[0][1].strip()

    session.close()

