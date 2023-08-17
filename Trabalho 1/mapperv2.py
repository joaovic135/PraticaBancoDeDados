#!/usr/bin/env python

import sys
import re

class Mapper:
  def __init__(self):
      self.H = {}

  def map(self, line):
    doc = line.strip()
    terms = doc.split()
    for term in terms:
      cleaned_term = re.sub(r'[.,?!()"\'$#]', '', term)
      if re.match(r'^[a-zA-Z]+$', cleaned_term):  # Verifica se a palavra tem apenas letras
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
      mapper.map(line)
  mapper.close()
