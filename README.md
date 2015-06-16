## ORS Collector
Series of scripts to collect data from ORS using [ScraperWiki](https://scraperwiki.com/). The resulting datasets can be accessed on HDX under the [Sahel ORS](https://data.hdx.rwlabs.org/organization/sahel-ors) page.

## Installation
The scraper was designed to be used in `ScraperWiki`. Run the [`bin/setup.sh`](bin/setup.sh) script to install dependencies and setup the database:

```shell
$ make setup
```

## Usage
To run the scraper, do:
```bash
$ make run
```

Or using Python:
```bash
$ python scripts/ors_collect/
```
