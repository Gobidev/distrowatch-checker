import xmltodict
import requests
import json
import time
import os.path
from discord_webhook import DiscordWebhook, DiscordEmbed
import SECRETS


class NewsEvent:

    def __init__(self, title: str, time: str, description: str, link: str) -> None:
        self.title = title
        self.time = time
        self.description = description
        self.link = link
    
    def __repr__(self) -> str:
        return f"{self.time}\n--\n{self.title}\n--\n{self.description}\n--\n{self.link}"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NewsEvent):
            return False
        return other.__dict__ == self.__dict__


def fetch_current_distro_news() -> dict:
    return xmltodict.parse(requests.get(r"https://distrowatch.com/news/dw.xml").text)


def filter_news_entries(news_dict: dict) -> list:
    return news_dict["rdf:RDF"]["item"]


def convert_dicts_to_objects(news: list) -> list:
    object_list = []
    for entry in news:
        object_list.append(NewsEvent(entry["title"], entry["dc:date"], entry["description"], entry["link"]))
    return object_list


def get_events() -> list:
    return convert_dicts_to_objects(filter_news_entries(fetch_current_distro_news()))


def send_webhook(news_event: NewsEvent):
    webhook = DiscordWebhook(url=SECRETS.WEBHOOK_URL)
    embed = DiscordEmbed(title=news_event.title, description=news_event.description, color="7f0304", url=news_event.link)
    embed.set_footer(text=news_event.time)
    webhook.add_embed(embed)
    webhook.execute()
    time.sleep(1)


def save_events_to_file(news_events: list):
    with open("news_data.json", "w") as news_data_file:
        json.dump([e.__dict__ for e in news_events], news_data_file, indent=2)


def load_events_from_file() -> list:
    if not os.path.isfile("news_data.json"):
        return []
    with open("news_data.json", "r") as news_data_file:
        return [NewsEvent(**e) for e in json.load(news_data_file)]


if __name__ == "__main__":
    current_events = get_events()
    saved_events = load_events_from_file()

    print("Sending notifications for news..")
    for new_event in current_events:
        if new_event not in saved_events:
            print(f"New event:\n{new_event}")
            send_webhook(new_event)
    print("..done")
    
    save_events_to_file(current_events)
