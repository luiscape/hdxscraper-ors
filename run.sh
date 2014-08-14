Rscript code/scraper.R
mv scraperwiki.sqlite ../
zip -r data/ocha-ors.zip data/indicator.csv data/value.csv data/dataset.csv
mv data/ocha-ors.zip http/csv.zip