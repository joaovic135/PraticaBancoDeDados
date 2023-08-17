#!/usr/bin/env python

import sys
import re

class Mapper:
  def __init__(self):
    self.H = {}

  def map(self, _, line):
    terms = line.strip().split()
    for term in terms:
      cleaned_term = re.sub(r'[.,?!()"\'$#]', '', term)
      if cleaned_term and cleaned_term != '-':
        if cleaned_term in self.H:
          self.H[cleaned_term] += 1
        else:
          self.H[cleaned_term] = 1

  def close(self):
    for term, count in self.H.items():
      print(f"{term}\t{count}")

if __name__ == "__main__":
  mapper = Mapper()
  for line in sys.stdin:
    mapper.map(None, line)
  mapper.close()