# squarespace-extractor

Extract events or blogs from squarespace, so they can be reused elsewhere. Square space does not offer this option, which is really problematic if you need it and you have hundreds of events on it.

## Events

### Usage

```commandline
usage: Extract squarespace events into json [-h] [-o OUTPUT] [-p PARSED_EVENTS] [-v] -s SITE [-e EVENTS_NAME]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output json file for events
  -p PARSED_EVENTS, --parsed_events PARSED_EVENTS
                        Json file with events that were already parsed so they can be skipped in current parsing
  -v, --verbose         Logging
  -s SITE, --site SITE  Site name, so that it can be found on dashboard
  -e EVENTS_NAME, --events_name EVENTS_NAME
                        Events tab name can be localized or named something else
```

### Important

You have to manually log in, when prompt in the console and then press enter to continue the program. This is because there are different options of logging in and would be a bit harder to support automatically since most of them open in a new window and can also have 2FA enabled. 

### TODO

* [ ] Detect when end of events was reached. Currently, you have to press `Ctrl+C` to exit and save the events when the end point is reached.

## Blogs

### Usage

```commandline
usage: Extract squarespace blogs into json [-h] [-o OUTPUT] -s SITE -b BLOG [-v] [-p PARSED_BLOGS] [-t {normal,photo}]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output json file for blogs
  -s SITE, --site SITE  Site url
  -b BLOG, --blog BLOG  Site subpage, so complete link is [SITE][BLOG]
  -v, --verbose         Logging
  -p PARSED_BLOGS, --parsed_blogs PARSED_BLOGS
                        Json file with blogs that were already parsed so they can be skipped in current parsing
  -t {normal,photo}, --type {normal,photo}
                        Type of site configuration
```

### Important

Squarespace can block after a with `429 To Many Requests` status code. Just rerun the parser with `--parsed_blogs` with current json file, and it will continue there.

### TODO

* [ ]  Mitigate `429 To Many Requests` problem

