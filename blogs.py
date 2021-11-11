import argparse
import sys


def parse_square_space_blogs(site_url: str, output_file: str = "blogs.json", verbose: bool = False):
    print("TODO")


def main():
    parser = argparse.ArgumentParser("Extract squarespace blogs into json")
    parser.add_argument("-o", "--output", type=str, default="blogs.json", help="Output json file for blogs")
    parser.add_argument("-s", "--site", type=str, required=True, help="Site url")
    parser.add_argument("-v", "--verbose", action="store_true", help="Logging")
    args = parser.parse_args()

    parse_square_space_blogs(site_url=args.site, output_file=args.output, verbose=args.verbose)


if __name__ == "__main__":
    sys.exit(main())
