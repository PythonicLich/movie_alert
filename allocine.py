import requests_html
import re
import css
import json
import datetime


def initialization(url, existing_session=None):
    if existing_session is None:
        session = requests_html.HTMLSession()
    else:
        session = existing_session
    page = session.get(url)
    movie_links = page.html.find(css.values["css_movie_url"])
    movie_urls = [list(x.absolute_links)[0] for x in movie_links]
    other_pages = page.html.find(css.values["css_crawl_more"])
    other_pages_urls = [list(x.absolute_links)[0] for x in other_pages]
    if existing_session is not None:
        session.close()
    return movie_urls, other_pages_urls


def movie_page_scraping(movie_url, existing_session=None):
    if existing_session is None:
        session = requests_html.HTMLSession()
    else:
        session = existing_session
    home_page = session.get(movie_url).html

    casting_url = [x for x in home_page.absolute_links if "casting" in x][0]
    critic_url = [x for x in home_page.absolute_links if "/critiques/presse/" in x][0]
    public_url = [x for x in home_page.absolute_links if "/critiques/spectateurs/" in x][0]

    casting_page = session.get(casting_url).html
    critic_page = session.get(critic_url).html
    public_page = session.get(public_url).html

    title = home_page.find(css.values["css_page_title"], first=True).text
    synopsis = home_page.find(css.values["css_synopsis"], first=True).text
    meta = home_page.find(css.values["css_meta"], first=True).text
    date = re.findall(".+(?=en salle)", meta)[0].strip()
    time = re.findall("/(.+?)/", meta)[0].strip()
    genre = re.findall("/(.+?)/(.+)", meta)[0][1].strip()
    directors = [x.text for x in casting_page.find(css.values["css_directors"])]
    writers = [x.text for x in casting_page.find(css.values["css_writers"])]
    actors = [x.text for x in casting_page.find(css.values["css_actors"])]
    soundtrack = [x.text for x in casting_page.find(css.values["css_sound_track"])]
    everyone = [x.text for x in casting_page.find(css.values["css_everyone"])]
    public_note = float(public_page.find(css.values["css_note"], first=True).replace(",", "."))
    critic_note = float(critic_page.find(css.values["css_note"], first=True).replace(",", "."))
    dictionary = {"title": title,
                  "synopsis": synopsis,
                  "date": date,
                  "time": time,
                  "genre": genre,
                  "directors": directors,
                  "writers": writers,
                  "actors": actors,
                  "soundtrack": soundtrack,
                  "public note": public_note,
                  "critic note": critic_note,
                  "everyone": everyone}
    if existing_session is not None:
        session.close()
    return dictionary


def get_movie_links(existing_session=None):
    container_page_urls_to_visit = []
    container_movie_urls_to_visit = []
    container_page_urls_visited = []
    if existing_session is None:
        session = requests_html.HTMLSession()
    else:
        session = existing_session
    container_page_urls_to_visit.append(css.values["start_crawl_page"])
    while len([x for x in container_page_urls_to_visit if x not in container_page_urls_visited]) != 0:
        for new_link in container_page_urls_to_visit:
            try:
                new_movies, new_pages = initialization(new_link, session)
                container_page_urls_visited.append(new_link)
                container_movie_urls_to_visit.extend([x for x in new_movies if x not in container_movie_urls_to_visit])
                container_page_urls_to_visit.extend([x for x in new_pages if
                                                     x not in container_page_urls_to_visit and x not in container_page_urls_visited])
            except Exception as e:
                print("Error during the for loop: " + str(type(e)) + "  " + str(e))

    if existing_session is None:
        session.close()
    return container_movie_urls_to_visit


if __name__ == "__main__":
    timestamp = datetime.datetime.now().strftime("%Y %m %d - %H %m %S")
    main_session = requests_html.HTMLSession()
    try:
        movie_links = get_movie_links(main_session)
        with open(timestamp + " data.json", "w", encoding="utf-8") as f:
            json.dump(movie_links, f)
    except Exception as e:
        print("Error while retrieving the links " + str(type(e)) + " " + str(e))

    main_session.close()
