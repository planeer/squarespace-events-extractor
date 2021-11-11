import argparse
import sys

import requests
from bs4 import BeautifulSoup


def parse_square_space_blogs(site_url: str, blog_subpage: str, output_file: str = "blogs.json", verbose: bool = False):
    if verbose:
        print(f"Getting site {site_url}{blog_subpage}")

    site = BeautifulSoup(requests.get(f"{site_url}{blog_subpage}").text, "html.parser")

    # Pages are broken up into sections with blogs
    sections = site.find(id="content").find_all(class_="sqs-gallery-design-list")
    if verbose:
        print()
        print(f"Need to parse {len(sections)} sections")

    parsed_blogs = []

    for index, sections in enumerate(sections):
        blogs = sections.find_all(class_="summary-item")

        if verbose:
            print()
            print(f"Parsing {index+1} section ({len(blogs)} blogs)")

        for blog in blogs:
            parsed_blog = {}

            blog_preview = blog.find(class_="summary-content")

            title_element = blog_preview.find(class_="summary-title")
            url = site_url + title_element.find("a")["href"][1:]
            title = title_element.text.strip()
            parsed_blog["title"] = title

            date_element = blog_preview.find(class_="summary-metadata-item--date")
            date = ""
            if date_element is not None:
                date = date_element.text.strip()
            parsed_blog["date"] = date

            if verbose:
                print(f"-> Parsing blog: {title} | {date}")

            excerpt_element = blog_preview.find(class_="summary-excerpt")
            excerpt = ""
            if excerpt_element is not None:
                excerpt = excerpt_element.text.strip()
            parsed_blog["summary"] = excerpt

            featured_image = blog.find(class_="summary-thumbnail").find("img")["data-src"]
            parsed_blog["featured_image"] = featured_image

            parsed_blogs.append(parsed_blog)


def main():
    parser = argparse.ArgumentParser("Extract squarespace blogs into json")
    parser.add_argument("-o", "--output", type=str, default="blogs.json", help="Output json file for blogs")
    parser.add_argument("-s", "--site", type=str, required=True, help="Site url")
    parser.add_argument("-b", "--blog", type=str, required=True, help="Site subpage, so complete link is [SITE][BLOG]")
    parser.add_argument("-v", "--verbose", action="store_true", help="Logging")
    args = parser.parse_args()

    parse_square_space_blogs(site_url=args.site, blog_subpage=args.blog, output_file=args.output, verbose=args.verbose)


if __name__ == "__main__":
    sys.exit(main())
