ORS in HDX
==========

From [ORS' website](http://ors.ocharowca.info/):

"The Online Reporting System (ORS) is a real- time web-based performance monitoring tool that allows UN agencies and 	NGOs participating in inter-agency planning processes (Strategic Response Plans or Emergency Action Plans) to directly 		report on the achievements based on the activities they specified during the SRP. The database has been designed to 	facilitate information sharing and monitor performance of all humanitarian interventions.

ORS is being deployed across the Sahel region (9 countries) and is managed by the OCHA Regional Office for West and 	Central Africa (ROWCA) working closely with the country offices.

The tool hosts all project data as submitted by partners during the SRP process and is also linked to the Financial 	Tracking Service (FTS) database and website that tracks funding requests and funding status of projects in inter-agency 	plans."



Data Summary
------------
To run scraper, do:
```bash
$ bash code/run.sh
```

Or using Python:
```bash
$ python code/scraper.py
```

API Documentation
-----------------
ORS has an undocumented API. The following endpoints can be used as a guidance.

 * All reported data http://ors.ocharowca.info/DataFeeds/ReportedData.ashx?project=&country=&subcluster=&cluster=&org=&obj=&act=&ind=&month=&admin1=&lng=
 * Validated reported data only http://ors.ocharowca.info/Anonymous/allvalidateddatafeed.ashx?country=&cluster=&org=&month=&project=&ops=&lng=
 * Country Framework http://ors.ocharowca.info/datafeeds/indicators.ashx?country=&cluster=&obj=&act=&ind=
 * Country Framework with targets http://ors.ocharowca.info/datafeeds/frameworktargets.ashx?country=&cluster=&obj=&act=&admin1=
 * OPS Projects http://ors.ocharowca.info/datafeeds/projects.ashx?project=&country=&subcluster=&cluster=&org=&lng=
 * OPS Projects targets http://ors.ocharowca.info/DataFeeds/projectsrptargets.ashx?project=&country=&subcluster=&cluster=&org=&act=&ind=&status=&tloc=&lng=
 * Cluster Indicators http://ors.ocharowca.info/datafeeds/clusterindicator.ashx?country=&cluster=
- List of Organization with ID http://ors.ocharowca.info/datafeeds/organizations.ashx
 * List of Cluster ID http://ors.ocharowca.info/datafeeds/clusters.ashx
 * List of Country http://ors.ocharowca.info/datafeeds/country.ashx