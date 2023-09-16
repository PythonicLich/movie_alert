import requests_html
import re
import css
import json

container_page_urls = []
container_movie_urls = []
container_movie_info = []


def initialization():
    session = requests_html.HTMLSession()
    page = session.get(css.values["start_crawl_page"])
    movie_links = page.html.find(css.values["css_movie_url"])
    movie_urls = [list(x.absolute_links)[0] for x in movie_links if x not in container_movie_urls]
    other_movies = page.html.find(css.values["css_crawl_more"])
    other_movie_urls = [list(x.absolute_links)[0] for x in other_movies if x not in container_page_urls]
    session.close()
    return movie_urls, other_movie_urls


def movie_page_scraping(url, existing_session=None):
    if existing_session is None:
        session = requests_html.HTMLSession()
    else:
        session = existing_session
    home_page = session.get(url).html

    casting_url = home_page.find(css.values["css_selector_casting_url"], first=True)
    critic_url = home_page.find(css.values["css_public_critic_url"], first=True)
    public_url = home_page.find(css.values["css_pro_critic_url"], first=True)

    casting_page = session.get(casting_url).html
    critic_page = session.get(critic_url).html
    public_page = session.get(public_url).html

    title = home_page.find(css.values["css_selector_page_title"])
    meta = home_page.find(css.values["css_selector_meta"])
    date = re.findall(".+(?=en salle)", meta.text)[0].strip()
    time = re.findall("/(.+?)/", meta.text)[0].strip()
    genre = re.findall("/(.+?)/(.+)", meta.text)[0][1].strip()
    directors = [x.text for x in casting_page.find(css.values["css_directors"])]
    writers = [x.text for x in casting_page.find(css.values["css_writers"])]
    actors = [x.text for x in casting_page.find(css.values["css_actors"])]
    soundtrack = [x.text for x in casting_page.find(css.values["css_sound_track"])]
    public_note = float(public_page.find(css.values["css_note"], first=True).replace(",", "."))
    critic_note = float(critic_page.find(css.values["css_note"], first=True).replace(",", "."))
    dictionary = {"title": title,
                  "date": date,
                  "time": time,
                  "genre": genre,
                  "directors": directors,
                  "writers": writers,
                  "actors": actors,
                  "soundtrack": soundtrack,
                  "public note": public_note,
                  "critic note": critic_note}
    if existing_session is not None:
        session.close()
    return dictionary


def movie_score_scraping(url):
    session = requests_html.HTMLSession()
    page = session.get(url)

    session.close()
