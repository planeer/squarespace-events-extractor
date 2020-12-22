# squarespace-events-extractor

Extract events from squarespace, so they can be reused elsewhere. Square space does not offer this option, which is really problematic if you need it and you have hundreds of events on it.

## Usage

```commandline
usage: Extract squarespace events into json [-h] [-o OUTPUT] [-p PARSED_EVENTS] [-v] -s SITE [-e EVENTS_NAME]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output json file for events
  -p PARSED_EVENTS, --parsed_events PARSED_EVENTS
                        Events that were already parsed, so they can be skipped in current parsing
  -v, --verbose         Logging
  -s SITE, --site SITE  Site name, so that it can be found on dashboard
  -e EVENTS_NAME, --events_name EVENTS_NAME
                        Events tab name can be localized or named something else
```

## Important

You have to manually log in, when prompt in the console and then press enter to continue the program. This is because there are different options of logging in and would be a bit harder to support automatically since most of them open in a new window and can also have 2FA enabled. 

## TODO

* [ ] Detect when end of events was reached. Currently, you have to press `Ctrl+C` to exit and save the events when the end point is reached.
