import bs4
import datetime
import json
import logging
import pandas as pd
import re
import requests
import time
from dataclasses import dataclass
from functools import partial, wraps
from pathlib import Path
from typing import Callable, Optional

logging.basicConfig(
    filename="Log.log",
    format="%(asctime)s - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
    level=logging.INFO,
)


class CaptchaJancoegException(Exception):
    pass


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

    name: Optional[str] = None
    address: Optional[str] = None
    sector: Optional[str] = None

    def describe(self):
        print(
            f"""{self.name} is a corporation located at {self.address}.
it's in {self.sector} sector."""
        )


def generate_soup(
    link: str,
    headers: Optional[dict] = None,
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
    soup = bs4.BeautifulSoup(c, "html.parser")

    if (
        soup.h1.text  # type:ignore
        == "By using the directory services of Infobel you accept the conditions of use."
    ):
        raise CaptchaJancoegException
    return soup


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

    try:
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
        return int(max_page)

    except AttributeError:
        logging.info("This category only has one page")
        print("This category only has one page")
        return 1


def generate_page_links(
    soup: bs4.BeautifulSoup,
    page_link: str,
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


def scrapping_process(
    obj: list[dict],
    *,
    start_index: Optional[int] = None,
    end_index: Optional[int] = None,
    headers: Optional[dict],
    category_sleep: float = 5,
    page_sleep: float = 1.5,
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
    end_index:
        Index of `obj` to start with.
        If `None` then all of the index from `start_index`.

    Returns
    -------
    Extended list of Corporations object (Not returned explicitly) and expected rows.
    """

    for category in obj[start_index:end_index]:
        try:
            start = time.perf_counter()

            logging.info(f"Started for {category['name']!r}")
            print(f"{datetime.datetime.today()} Started for {category['name']!r}")
            category["companies"] = []
            page_links = generate_page_links(
                generate_soup(category["first_link"], headers=headers),
                category["first_link"],
            )

            number_pages = len(page_links)
            category["expected_rows"] = number_pages * 20
            logging.info(
                f"    Pages: {number_pages} | Expected result: ~{category['expected_rows']}"
            )
            print(
                f"    Pages: {number_pages} | Expected result: ~{category['expected_rows']}"
            )

            # Each category's page
            for j, link in enumerate(page_links):

                if j % 10 == 0 and j > 0:
                    time.sleep(page_sleep)

                category["companies"].extend(
                    data_scrapper(generate_soup(link, headers=headers))
                )

            finish = time.perf_counter()

            ellapsed = round(finish - start, 2)

            logging.info(f"Finished for {category['name']!r} in {ellapsed} s\n{'='*80}")
            print(
                f"{datetime.datetime.today()} - INFO: Finished for {category['name']!r} in {ellapsed} s\n{'='*80}"
            )

            time.sleep(category_sleep)

        except CaptchaJancoegException:
            logging.fatal("Captcha! That's it for today, folks!")
            print(
                f"{datetime.datetime.today()} - CRITICAL: Captcha! That's it for today, folks!"
            )
            break


def save_to_csv(obj: list[dict], filepath: str = "") -> None:
    """
    Save successfully scrapped data into CSV.

    Parameters
    ----------
    obj:
        list of dictionary of
            name = Name of caegory
            first_link = First page of the category

    Returns
    -------
    Modified obj list[dict] `scrapped_rows` key.
    CSV file of said corporation.
    """
    fp = Path(filepath)
    logging.info("Saving files...")
    print(f"{datetime.datetime.today()} - INFO: Saving files...")
    for i, category in enumerate(obj):
        if not category.get("companies"):
            continue

        df = pd.DataFrame(category["companies"])
        rows = df.shape[0]
        expected = category.get("expected_rows", 1)
        category["scrapped_rows"] = rows

        logging.info(
            f"""Finished index [{i:>3}] : {category['name']!r}
        Scrapped: {category['scrapped_rows']:>4} rows | Expected {expected} rows | DIfference: {expected - category['scrapped_rows']} ({category['scrapped_rows'] / expected:.1%})"""
        )
        print(
            f"""Finished index [{i:>3}] : {category['name']!r}
        Scrapped: {category['scrapped_rows']:>4} rows | Expected {expected} rows | DIfference: {expected - category['scrapped_rows']} ({category['scrapped_rows'] / expected:.1%})"""
        )

        # Bila perbedaan >= 20 rows dari ekspektasi, harus rerun
        if expected - rows >= 20:
            df.to_csv(
                fp / f"[{i}] RERUN - {category['name']}.csv", sep="|", index=False
            )
            category["rerun"] = True
            continue

        df.to_csv(fp / f"[{i}] - {category['name']}.csv", sep="|", index=False)
        category["rerun"] = False


def load_popular_links() -> list[dict]:
    """
    Load JSON file that stores links of popular categories.

    Returns
    -------
    list of dictionary of
        name = Name of caegory
        first_link = First page of the category
    """

    with open("popular/popular_categories.json", "r") as file:
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

    with open("unpopular/unpopular_categories.json", "r") as file:
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
        logging.info(f"Main process finished for {ellapsed} s\n{'=' * 80}")
        print(f"Main process finished for {ellapsed} s\n{'=' * 80}")

    return wrapper


def progress_saver(
    obj: list[dict],
    filepath: str = "",
) -> None:
    path = Path(filepath)
    updates = [
        {
            "index": category["index"],
            "name": category["name"],
            "first_link": category["first_link"],
            "expected_rows": category.get("expected_rows"),
            "scrapped_rows": category.get("scrapped_rows"),
            "rerun": category.get("rerun"),
        }
        for category in obj
    ]
    with open(path, "r") as file:
        past_progress = json.load(file)

    for updt in updates:
        for past_prg in past_progress:
            if updt["name"] != past_prg["name"] and updt["rerun"]:
                past_prg.update(updt)
                continue
            continue

    with open(path, "w") as file:
        json.dump(past_progress, file, indent=4)


save_unpopular_progress = partial(
    progress_saver, filepath="unpopular/unpopular_categories.json"
)


@performance_counter
def main(
    obj: list[dict],
    csv_filepath: str = "",
    progress_filepath: str = "",
    *,
    start_index: Optional[int] = None,
    end_index: Optional[int] = None,
    browser_header: Optional[dict] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.43"
    },
    page_sleep: float = 1.5,
    category_sleep: float = 5,
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
    end_index:
        Index of `obj` to start with.
        If `None` then all of the index from `start_index`.

    Outputs
    -------
    CSV files of scrapped sectors.
    """
    try:
        assert start_index is not None
        scrapping_process(
            obj,
            start_index=start_index,
            end_index=end_index,
            headers=browser_header,
            category_sleep=category_sleep,
            page_sleep=page_sleep,
        )
        save_to_csv(obj, filepath=csv_filepath)
        progress_saver(obj, progress_filepath)

    except AssertionError:
        logging.fatal("You must provide `start_index`!")
        raise AssertionError("You must provide `start_index`!")


main_popular = partial(
    main,
    obj=load_popular_links(),
    csv_filepath="popular",
    progress_filepath="popular/popular_categories.json",
)
main_unpopular = partial(
    main,
    obj=load_unpopular_links(),
    csv_filepath="unpopular",
    progress_filepath="unpopular/unpopular_categories.json",
)
if __name__ == "__main__":
    main_unpopular(start_index=0)
