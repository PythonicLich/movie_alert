import requests_html
import re
import css
import json
import datetime
import traceback


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
    casting_url = ""
    critic_url = ""
    public_url = ""
    if(False):
        timestamp = datetime.datetime.now().strftime("%Y %m %d - %H %M %S")
        with open(timestamp + "faulty_movie.html", "w", encoding="utf-8") as file:
            file.write(home_page.html)

    try:
        critic_url = [x for x in home_page.absolute_links if "/critiques/presse/" in x][0]
        public_url = [x for x in home_page.absolute_links if "/critiques/spectateurs/" in x][0]
        casting_url = [x for x in home_page.absolute_links if "casting" in x][0]
    except Exception as e:
        print("Error while setting the urls " + str(type(e)) + " " + str(e))
        print(f"number of urls : {len(home_page.absolute_links)}")
        if (len([x for x in home_page.absolute_links if "casting" in x]) == 0):
            casting_url = public_url.replace("/critiques/spectateurs/", "/casting")
        #[print(x) for x in home_page.absolute_links]
    try:
        casting_page = session.get(casting_url).html if casting_url != "" else None
        critic_page = session.get(critic_url).html if critic_url != "" else None
        public_page = session.get(public_url).html if public_url != "" else None
    except Exception as e:
        print("Error while retrieving the urls " + str(type(e)) + " " + str(e))

    try:
        title = home_page.find(css.values["css_page_title"], first=True).text if home_page is not None else ""
        synopsis = home_page.find(css.values["css_synopsis"], first=True).text if home_page is not None else ""
        meta = home_page.find(css.values["css_meta"], first=True).text if home_page is not None else ""
        date = re.findall(".+(?=en salle)", meta)[0].strip() if home_page is not None else ""
        time = re.findall("/(.+?)/", meta)[0].strip() if home_page is not None else ""
        genre = re.findall("/(.+?)/(.+)", meta)[0][1].strip() if home_page is not None else ""
    except Exception as e:
        print("Error while processing home_page : " + str(type(e)) + " " + str(e))
    try:
        directors = [x.text for x in casting_page.find(css.values["css_directors"])] if casting_page is not None else ""
        writers = [x.text for x in casting_page.find(css.values["css_writers"])] if casting_page is not None else ""
        actors = [x.text for x in casting_page.find(css.values["css_actors"])] if casting_page is not None else ""
        soundtrack = [x.text for x in casting_page.find(css.values["css_sound_track"])] if casting_page is not None else ""
        everyone = [x.text for x in casting_page.find(css.values["css_everyone"])] if casting_page is not None else ""
    except Exception as e:
        print("Error while accessing the casting page " + str(type(e)) + " " + str(e))
    try:
        public_note = 0
        critic_note = 0
        public_note = float(public_page.find(css.values["css_note"], first=True).text.replace(",", ".")) if public_page is not None else 0
        critic_note = float(critic_page.find(css.values["css_pro_critic_note"], first=True).text.replace(",", ".")) if public_page is not None else 0
    except Exception as e:
        print("Weird exception while trying to convert the string note to a number " + str(type(e)) + " " + str(e))
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


def default_loop():
    timestamp = datetime.datetime.now().strftime("%Y %m %d - %H %M %S")
    main_session = requests_html.HTMLSession()
    movies = []
    movie_links = []
    try:
        movie_links = get_movie_links(main_session)
        # with open("2023 09 16 - 17 09 48 data.json", "r", encoding="utf-8") as f:
        #    movie_links = json.load(f)
        with open(timestamp + " data.json", "w", encoding="utf-8") as f:
            json.dump(movie_links, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("Error while retrieving the links " + str(type(e)) + " " + str(e))
    try:
        # with open("2023 09 16 - 17 09 48 data.json", "r", encoding="utf-8") as file:
        #    json_movie_links = json.load(file)
        json_movie_links = movie_links
        for movie_link in json_movie_links:
            try:
                print(movie_link)
                movie_data = movie_page_scraping(movie_link, main_session)
                movies.append(movie_data)
            except Exception as e:
                print("Error while looping the movies " + str(type(e)) + " " + str(e))
    except Exception as e:
        print("Error while retrieving the movies " + str(type(e)) + " " + str(e))
    with open(timestamp + " movie_data.json", "w", encoding="utf-8") as f:
        json.dump(movies, f, indent=4, ensure_ascii=False)
    main_session.close()


def test_faulty_movie():
    try:
        that_movie = movie_page_scraping("https://www.allocine.fr/film/fichefilm_gen_cfilm=309058.html")
        #[print(x, " ", that_movie[x]) for x in that_movie]

    except Exception as e:
        print("Error while retrieving the faulty link : " + str(type(e)) + " " + str(e) + " \n" + str(e.__traceback__))


if __name__ == "__main__":
    default_loop()
    #test_faulty_movie()
