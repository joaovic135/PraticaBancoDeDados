#!/usr/bin/env python

import sys

class Mapper:
  def __init__(self):
    self.H = {}

  def map(self, docid, doc):
    for term in doc.split():
      if term in self.H:
        self.H[term] += 1
      else:
        self.H[term] = 1

  def close(self):
    for term, count in self.H.items():
      print(f"{term}\t{count}")

if __name__ == "__main__":
  mapper = Mapper()
  for line in sys.stdin:
    docid, doc = line.strip().split("\t")
    mapper.map(docid, doc)
  mapper.close()