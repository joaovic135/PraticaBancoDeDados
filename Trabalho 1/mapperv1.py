#!/usr/bin/env python

import sys
import re

class Mapper:
  def __init__(self):
    self.H = {}

  def map(self, docid, doc):
    docid, doc = line.strip().split('\t')
    terms = doc.split()
    for term in terms:
      if term in self.H:
        cleaned_term = re.sub(r'[.,?!]','',term.lower())
        self.H[term] += 1
      else:
        self.H[term] = 1

  def close(self):
    for term, count in self.H.items():
      print(f"{term}\t{count}")

if __name__ == "__main__":
  mapper = Mapper()
  for line in sys.stdin:
    mapper.map(None, line)
  mapper.close()