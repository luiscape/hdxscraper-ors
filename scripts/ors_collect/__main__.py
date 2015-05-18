#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

from utilities.hdx_format import item
from ors_collect import collect as Collect
from ors_collect import patch as Patch


if __name__ == '__main__':

  Collect.Main()
  Patch.Main()


#   try:
#       Main()
#       print "SW Status: Everything seems to be just fine."
#       scraperwiki.status('ok')

#   except Exception as e:
#       print e
#       scraperwiki.status('error', 'Error collecting data.')
#       os.system("echo https://ds-ec2.scraperwiki.com/3zarzzv/0zftw6fzkjxommp/http/log.txt | mail -s 'ORS APIs: Failed collecting data.' luiscape@gmail.com")
