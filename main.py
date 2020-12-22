from typing import List

from selenium import webdriver
import sys
import time
from random import seed, randint
import hashlib
import json
import argparse

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement


def random_wait(lower_limit: int = 1, upper_limit: int = 10):
    time.sleep(randint(lower_limit, upper_limit))


def filter_events_element(events_element: WebElement):
    """
    If there are more elements with same name, we can determine correct by checking for the calendar icon before it.
    """
    parent = events_element.find_element_by_xpath("..")  # Get parent
    children = parent.find_elements_by_xpath(".//*")  # Get children
    icon_element = children[0]  # First element should be the icon

    return icon_element.get_attribute("class") == "icon icon-calendar"


def get_elements_sources(elements: List[WebElement]) -> List[str]:
    return list(map(lambda element: element.get_attribute("src"), elements))


def crawl_squarespace_events(site_name: str, events_name: str = "Events", output_file: str = "events.json",
                             events_file: str = None, verbose: bool = False):
    seed()

    driver = webdriver.Chrome()
    driver.get("https://www.squarespace.com/")

    login_elements = driver.find_elements_by_class_name("www-navigation__desktop__account-info__login-button")
    assert len(login_elements) == 1
    login_element = login_elements[0]

    random_wait()

    login_element.click()  # Go to the login page

    # Log in is manual because you can login from different sources (squarespace, google, facebook, apple)
    input("Click enter once logged in and on dashboard.")

    correct_site_element = driver.find_element_by_link_text(site_name)
    correct_site_element.click()

    random_wait()

    pages_navigation_tab = driver.find_element_by_link_text("Pages")
    pages_navigation_tab.click()

    random_wait()

    events_elements = driver.find_elements_by_css_selector(f"div[title=\"{events_name}\"]")
    filtered_events_elements = list(filter(filter_events_element, events_elements))
    assert len(filtered_events_elements) == 1
    events_element = filtered_events_elements[0]
    events_element.click()

    random_wait(lower_limit=5)

    past_events_element = driver.find_element_by_css_selector("input[aria-label=\"Past Events\"]")
    past_events_element.click()

    random_wait()

    already_checked_events_hashes = []
    if events_file is not None:
        with open(events_file) as json_file:
            events = json.load(json_file)
    else:
        events = []

    past_events_list = driver.find_element_by_class_name("ReactVirtualized__List")

    try:
        while True:  # TODO Detect the end state
            if verbose:
                print("Getting next batch of events")

            # Get children of first child
            past_events = past_events_list.find_elements_by_css_selector(".ReactVirtualized__List > div > div")

            for past_event in past_events:
                try:
                    event_hash = hashlib.sha256(past_event.text.encode("utf-8")).hexdigest()
                except StaleElementReferenceException:
                    # Sometimes there is no reference to the event even though it is visible on screen, so we must
                    # refresh all events
                    break

                if event_hash not in already_checked_events_hashes:
                    driver.execute_script("arguments[0].scrollIntoView();", past_event)
                    already_checked_events_hashes.append(event_hash)

                    if event_hash not in [_event["hash"] for _event in events]:
                        if verbose:
                            print()
                            print(f"New event: {event_hash}\n{past_event.text}")
                            print()

                        event = {"hash": event_hash}

                        past_event.click()
                        random_wait(lower_limit=5)

                        # Switch focus to iframe so we can get event data
                        driver.switch_to.frame(driver.find_element_by_id("sqs-site-frame"))

                        title = driver.find_element_by_css_selector(".eventitem-title").text
                        event["title"] = title

                        date_time = driver.find_element_by_css_selector(".event-meta-date-time-container").text
                        event["date_time"] = date_time

                        location = driver.find_elements_by_css_selector(".event-meta-address-container")
                        assert len(location) <= 1  # There should be max one event location
                        if len(location) == 1:
                            event["location"] = location[0].text

                        text = driver.find_elements_by_css_selector(".eventitem-column-content > div")
                        if len(text) >= 1:
                            event["text"] = text[0].text
                        else:
                            event["text"] = ""

                        images = driver.find_elements_by_css_selector(".thumb-image")
                        event["images"] = get_elements_sources(images)

                        videos = driver.find_elements_by_css_selector(".intrinsic iframe")
                        event["videos"] = get_elements_sources(videos)

                        events.append(event)

                        driver.switch_to.default_content()
                    else:
                        random_wait(lower_limit=2, upper_limit=5)
    except KeyboardInterrupt:
        with open(output_file, "w") as write_file:
            json.dump(events, write_file)

        driver.close()


def main():
    parser = argparse.ArgumentParser("Extract squarespace events into json")
    parser.add_argument("-o", "--output", type=str, default="events.json", help="Output json file for events")
    parser.add_argument("-p", "--parsed_events", type=str,
                        help="Events that were already parsed, so they can be skipped in current parsing")
    parser.add_argument("-v", "--verbose", action="store_true", help="Logging")
    parser.add_argument("-s", "--site", type=str, required=True, help="Site name, so that it can be found on dashboard")
    parser.add_argument("-e", "--events_name", type=str, default="Events",
                        help="Events tab name can be localized or named something else")

    args = parser.parse_args()

    crawl_squarespace_events(site_name=args.site, events_name=args.events_name, output_file=args.output,
                             events_file=args.parsed_events, verbose=args.verbose)


if __name__ == "__main__":
    sys.exit(main())
