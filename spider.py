#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import urllib
from urllib.request import urlopen
from urllib.parse import urlparse, urlunparse, ParseResult, parse_qs, quote_plus
from html.parser import HTMLParser
import re
import nltk
import os
import ssl

def get_topad_url_addr(address, topaddr=None):
  url = urlparse(address)
  schemepart = url.scheme
  if schemepart == '':
    if topaddr:
      schemepart = topaddr['scheme']
    else:
      schemepart = 'http'
  netlocpart = url.netloc
  if netlocpart == '':
    if topaddr:
      netlocpart = topaddr['netloc']
    else:
      raise ValueError("cant infer net location from '%s' alone" % address)
  url = ParseResult(
    scheme=schemepart,
    netloc=netlocpart,
    path=url.path,
    params=url.params,
    query=url.query,
    fragment=url.fragment)
  address = urlunparse(url)
  topaddr = {
    'scheme' : schemepart,
    'netloc' : netlocpart }
  return topaddr, url, address
  

class HTMLSpiderParser(HTMLParser):
  def __init__(self, links, url_filter=lambda u: True, data_filter=lambda s: True, tag_filter=lambda t: True, writer=lambda s: print(s), traverse=lambda u: None, debug=False, capacity=1000):
    if isinstance(links, str):
      links = [links]
    HTMLParser.__init__(self)
    self._i = 0
    self._visited_links = set()
    self._links = links
    self._reading = True
    self._write = writer
    self._url_filter = url_filter
    self._data_filter = data_filter
    self._tag_filter = tag_filter
    self._f_traverse = traverse
    self._capacity = capacity
    self._topaddr = None
    self._rawdata = u''
  def capacity(self):
    return self._capacity
  def address(self):
    return self._address
  def nextaddress(self):
    return self._links[-1]
  def url(self):
    return self._url
  def visited_links(self):
    return self._visited_links
  def f_traverse(self):
    return self._f_traverse
  def url_filter(self):
    return self._url_filter
  def data_filter(self):
    return self._data_filter
  def tag_filter(self):
    return self._tag_filter
  def canparsenext(self):
    return len(self._links) > 0
  def parsenext(self):
    self._topaddr, self._url, self._address = get_topad_url_addr(self._links.pop(), self._topaddr)
    if self._url_filter(self._url):
      try:
        res = urlopen(self._address)
        data = res.readall().decode("utf-8")
        self.feed(data)
      except urllib.error.HTTPError as e:
        print('%-60s%20s' % ('%s...' % parser.address()[0:57] if len(parser.address()) > 57 else parser.address(), e)) 
      except ssl.CertificateError as e:
        print('%-60s%20s' % ('%s...' % parser.address()[0:57] if len(parser.address()) > 57 else parser.address(), e))
  def links(self):
    return self._links
  def datapath(self):
    return self._datapath
  def isreading(self):
    return self._reading
  def _traverse(self, url, link):
    self.f_traverse()(url)
    if url not in self._visited_links:
      if self._url_filter(url):
        if self._capacity and len(self._links) >= self._capacity:
          self._links[self._i] = link
        else:
          self._links.insert(0, link)
        if self._capacity and len(self._visited_links) >= self._capacity:
          self._visited_links.pop()
        self._visited_links.add(url)
        if self._capacity:
          self._i = (self._i + 1) % self._capacity
        else:
          self._i += 1
  def handle_starttag(self, tag, attrs):
    self._reading = False
    if tag.lower() == 'a':
      attrs = dict(attrs)
      if 'href' in attrs:
        link = attrs['href']
        _, url, link = get_topad_url_addr(link, self._topaddr)
        self._traverse(url, link)
    self._reading = self._tag_filter(tag)
  def handle_endtag(self, tag):
    if tag.lower() == 'html':
      print('%-60s%20s' % ('%s...' % parser.address()[0:57] if len(parser.address()) > 57 else parser.address(), 'L=%d, N=%d' % (len(self._links), len(self._visited_links))))
      for data in data_filter(self._rawdata):
        self._write(data)
  def handle_data(self, data):
    if self._reading:
      self._rawdata += data
      
if __name__ == '__main__':
  def data_filter(data):
    #return []
    for sent in nltk.tokenize.sent_tokenize(data):
      if True:#re.search(r'^.*\Ware\W.*$', sent):
        yield sent
  def write(sent):
    address = parser.address()
    f = open('./data/%s.txt' % quote_plus(address), 'a')
    f.write(sent + '\n')
    pass
  def path_filter(path):
    return re.search(r'^/wiki/[a-zA-Z0-9()_\-%]+$', path)
  def url_filter(url):
    #return True
    return \
      url.netloc.lower() == 'en.wikipedia.org' and \
      path_filter(url.path)
  parser = HTMLSpiderParser(
    links=['https://en.wikipedia.org/wiki/United_States'],
    url_filter=url_filter,
    data_filter=data_filter,
    writer=write,
    capacity=None)
  while parser.canparsenext():
    parser.parsenext()
  