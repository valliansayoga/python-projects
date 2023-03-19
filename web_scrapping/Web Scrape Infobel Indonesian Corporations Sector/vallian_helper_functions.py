import bs4
import datetime
import json
import logging
import pandas as pd
import re
import requests
import time
from dataclasses import dataclass
from functools import wraps
from typing import Callable

logging.basicConfig(
    filename="Log.log",
    format="%(asctime)s - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
    level=logging.INFO,
)


@dataclass
class Corporation:
    """
    Dataclass for Corporations.

    Attributes
    ----------
    name:
        Name of the company.
    address:
        Address of the company.
    sector:
        Sector of the company.
    """

    name: str | None = None
    address: str | None = None
    sector: str | None = None

    def describe(self):
        print(
            f"""{self.name} is a corporation located at {self.address}.
it's in {self.sector} sector."""
        )


def generate_soup(
    link: str,
    headers: dict | None = None,
) -> bs4.BeautifulSoup:
    """
    Generate Soup object from a link.

    Parameters
    ----------
    link:
        Link of infobel.
    headers:
        Headers setting of browser.
    Returns
    -------
    bs4.BeautifulSoup
    """

    c = requests.get(link, headers=headers).content
    return bs4.BeautifulSoup(c, "html.parser")


def generate_max_page(soup: bs4.BeautifulSoup) -> int:
    """
    Generate max page for each category.

    Parameters
    ----------
    soup:
        Soup object of link of interest.

    Returns
    -------
    String representation of the max page.
    """

    max_page = re.findall(
        r".*_([0-9]{1,2})\.htm$",
        sorted(
            [
                page.get("href")
                for page in soup.find(
                    "ul", {"class": "pagination"}
                ).find_all(  # type:ignore
                    "a",
                    {"href": re.compile(r".*index_[0-9]{1,2}\.htm")},
                )
            ],
            key=lambda link: int(re.findall(r".*_([0-9]{1,2})\.htm$", link)[0]),
        )[-1],
    )[0]
    return int(max_page)  # type:ignore


def generate_page_links(
    soup: bs4.BeautifulSoup,
    page_link: str,
    base_link: str = "https://local.infobel.co.id",
) -> list:
    """
    Generate page links for each category.

    Parameters
    ----------
    soup:
        Soup object.
    page_link:
        First page link of a category.
    base_link:
        Base link of infobel.

    Returns
    -------
    list of page links.
    """

    page_range = range(1, generate_max_page(soup) + 1)
    base_category_link = re.findall(r"(.*_)[0-9]{1,2}\.htm$", page_link)[0]
    return [f"{base_category_link}{page}.htm" for page in page_range]


def data_scrapper(soup: bs4.BeautifulSoup) -> list[Corporation]:
    """
    Scrape name, address, and sector of a company.

    Parameters
    ----------
    soup:
        Soup object.

    Returns
    -------
    list of Corporation objects
    """

    infos = soup.find_all("div", {"class": "customer-item-info"})
    data_container = []
    for info in infos:
        name = re.sub(r"^[0-9]{1,4}\.", "", info.find("h2").text).strip()
        address = info.find_all("span", {"class": "detail-text"})[0].text.strip()
        sector = soup.find(
            "div", {"class": "customer-item-labels-list"}
        ).text  # type:ignore
        data_container.append(Corporation(name=name, address=address, sector=sector))
    return data_container


def save_to_csv(obj: list[dict]) -> None:
    """
    Save successfully scrapped data into CSV.

    Parameters
    ----------
    obj:
        list of dictionary of
            name = Name of caegory
            first_link = First page of the category
    """
    logging.info("Saving files...")
    print(f"{datetime.datetime.today()} - INFO: Saving files...")
    for i, category in enumerate(obj):
        if not category.get("companies"):
            continue

        df = pd.DataFrame(category["companies"])
        rows = df.shape[0]
        df.to_csv(f"{category['name']}.csv", sep=";", index=False)

        logging.info(f"    Finished index: {i:>3} ({rows:>4} rows)")
        print(f"    Finished index: {i:>3} ({rows:>4} rows)")


def scrapping_process(
    obj: list[dict], *, start_index: int | None = None, headers: dict | None
) -> None:
    """
    Process function to scrape data accross pages.

    Parameters
    ----------
    obj:
        list of dictionary of
            name = Name of caegory
            first_link = First page of the category
    start_index:
        Index of `obj` to start with.
    """

    for i, category in enumerate(obj[start_index:]):
        try:
            start = time.perf_counter()

            logging.info(f"Started for {category['name']!r}")
            print(f"{datetime.datetime.today()} Started for {category['name']!r}")
            category["companies"] = []
            page_links = generate_page_links(
                generate_soup(category["first_link"], headers=headers),
                category["first_link"],
            )

            # Each category's page
            for j, link in enumerate(page_links):

                if j % 10 == 0 and j > 0:
                    time.sleep(1.5)

                category["companies"].extend(
                    data_scrapper(generate_soup(link, headers=headers))
                )

            finish = time.perf_counter()

            ellapsed = round(finish - start, 2)

            logging.info(f"Finished for {category['name']!r} in {ellapsed} s\n{'='*80}")
            print(
                f"{datetime.datetime.today()} - INFO: Finished for {category['name']!r} in {ellapsed} s\n{'='*80}"
            )

        except AttributeError as e:
            logging.critical(f"Captcha appeared for {category['name']!r}")
            print(
                f"{datetime.datetime.today()} - CRITICAL: Captcha appeared for {category['name']!r}"
            )
            break


def load_popular_links() -> list[dict]:
    """
    Load JSON file that stores links of popular categories.

    Returns
    -------
    list of dictionary of
        name = Name of caegory
        first_link = First page of the category
    """

    with open("popular_categories.json", "r") as file:
        data = json.load(file)
    return data


def load_unpopular_links() -> list[dict]:
    """
    Load JSON file that stores links of other categories.

    Returns
    -------
    list of dictionary of
        name = Name of caegory
        first_link = First page of the category
    """

    with open("unpopular_categories.json", "r") as file:
        data = json.load(file)
    return data


def performance_counter(function: Callable) -> Callable:
    """
    Logging performance time of a function.

    Parameters
    ----------
    function
        Any function its time to be counted.

    Returns
    -------
        Log entries of performance in second.
    """

    @wraps(function)
    def wrapper(*args, **kwargs):

        start = time.perf_counter()
        logging.info(f"Main process started...\n{'=' * 80}")
        print(f"Main process started...\n{'=' * 80}")

        function(*args, **kwargs)

        finish = time.perf_counter()

        ellapsed = round(finish - start, 2)
        logging.info(f"Main process finished for {ellapsed} s")
        print("Main process finished for", ellapsed, "s")

    return wrapper


@performance_counter
def main(
    obj: list[dict],
    *,
    start_index: int | None = None,
    browser_header: dict
    | None = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.43"
    },
) -> None:
    """
    Main function that combines helper functions to scrape Infobel
    for corporations data.

    Parameters
    ----------
    obj:
        list of dictionary of
        name = Name of caegory
        first_link = First page of the category
    start_index:
        Index of `obj` to start with.

    Outputs
    -------
    CSV files of scrapped sectors.
    """
    try:
        assert start_index is not None
        scrapping_process(obj, start_index=start_index, headers=browser_header)
        save_to_csv(obj)

    except AssertionError as e:
        logging.fatal("You must provide `start_index`!")
        raise AssertionError("You must provide `start_index`!")

    # except


if __name__ == "__main__":
    popular_links = load_popular_links()
    start_index = input("Please enter start index: ")
    try:
        start_index = int(start_index)
        main(popular_links, start_index=start_index)
    except ValueError:
        raise ValueError("Index must be an integer!")
