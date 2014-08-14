cd ..
rm -rf -- tool
mv hdxscraper-ors tool
crontab -l | { cat; echo "@daily bash tool/run.sh"; } | crontab -
printf "Now install the packages XML and sqldf in R.\n"
R