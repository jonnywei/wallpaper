#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import urllib
import cookielib
import json
import hashlib
import random
import datetime
import time
import socket

#中文


def get_content_from_url(url):
    content = urllib.urlopen(url).read()
    return content

