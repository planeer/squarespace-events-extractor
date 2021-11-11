import argparse
import json
import sys
from enum import Enum

import requests
from bs4 import BeautifulSoup


class BlogType(Enum):
    NORMAL = "normal"
    PHOTO = "photo"

    # Needed for input in argparse
    def __str__(self):
        return self.value


def parse_square_space_blogs(site_url: str, blog_subpage: str, output_file: str = "blogs.json", blogs_file: str = None,
                             blog_type: BlogType = BlogType.NORMAL, verbose: bool = False):
    if verbose:
        print(f"Getting site {site_url}{blog_subpage}")

    site = BeautifulSoup(requests.get(f"{site_url}{blog_subpage}").text, "html.parser")

    # Pages are broken up into sections with blogs
    if blog_type == BlogType.PHOTO:
        sections = site.find_all(class_="summary-item-list-container")
    else:
        sections = site.find(id="content").find_all(class_="sqs-gallery-design-list")

    if verbose:
        print()
        print(f"Need to parse {len(sections)} sections")

    if blogs_file is not None:
        with open(blogs_file) as json_file:
            parsed_blogs = json.load(json_file)
    else:
        parsed_blogs = []

    try:
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

                if title not in [_blog["title"] for _blog in parsed_blogs]:
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

                    blog_site = BeautifulSoup(requests.get(url).text, "html.parser")

                    if date == "":
                        # Sometimes date is not available in preview, so we must parse it from the actual site
                        parsed_blog["date"] = blog_site.find(class_="entry-dateline-link").text.strip()

                    blog_content = blog_site.find(class_="entry-content")

                    images = blog_content.find_all(class_="thumb-image")
                    images_urls = [image["data-src"] for image in images]

                    for image in images:
                        # Remove images from content html, because they need to be inserted manually later. We need to
                        # go so many parents above, because otherwise we leave the button "view full size" that belongs
                        # to the image
                        if blog_type == BlogType.PHOTO:
                            image.parent.decompose()
                        else:
                            image.parent.parent.parent.decompose()

                    parsed_blog["images"] = images_urls
                    parsed_blog["content"] = str(blog_content)

                    parsed_blogs.append(parsed_blog)
    finally:
        with open(output_file, "w") as write_file:
            json.dump(parsed_blogs, write_file)


def main():
    parser = argparse.ArgumentParser("Extract squarespace blogs into json")
    parser.add_argument("-o", "--output", type=str, default="blogs.json", help="Output json file for blogs")
    parser.add_argument("-s", "--site", type=str, required=True, help="Site url")
    parser.add_argument("-b", "--blog", type=str, required=True, help="Site subpage, so complete link is [SITE][BLOG]")
    parser.add_argument("-v", "--verbose", action="store_true", help="Logging")
    parser.add_argument("-p", "--parsed_blogs", type=str,
                        help="Json file with blogs that were already parsed so they can be skipped in current parsing")
    parser.add_argument("-t", "--type", type=BlogType, default=BlogType.NORMAL, choices=BlogType,
                        help="Type of site configuration")

    args = parser.parse_args()

    parse_square_space_blogs(site_url=args.site, blog_subpage=args.blog, output_file=args.output,
                             blogs_file=args.parsed_blogs, blog_type=args.type, verbose=args.verbose)


if __name__ == "__main__":
    sys.exit(main())
