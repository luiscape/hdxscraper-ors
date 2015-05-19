## ORS Collector
Series of scripts to collect data from ORS using [ScraperWiki](https://scraperwiki.com/). The resulting datasets can be accessed on HDX under the [Sahel ORS](https://data.hdx.rwlabs.org/organization/sahel-ors) page.

## Installation
The scraper was designed to be used in `ScraperWiki`. Run the `setup.sh` script to install dependencies and setup the database:

```shell
$ ./setup.sh
```

## Usage
To run the scraper, do:
```bash
$ ./run.sh
```

Or using Python:
```bash
$ python scripts/ors_collect/
```