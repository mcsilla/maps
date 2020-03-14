#!/usr/bin/env python3

import csv
import io
import json
import pathlib
import sys

HEADER_TRANSLATION = {
  'Ter\u00fclet': 'name',
  'magyar': 'hungarian',
  'bolg\u00e1r': 'bulgarian',
  'cig\u00e1ny (romani, be\u00e1s)': 'gypsy',
  'g\u00f6r\u00f6g': 'greek',
  'horv\u00e1t': 'croatian',
  'lengyel': 'polish',
  'n\u00e9met': 'german',
  '\u00f6rm\u00e9ny': 'armenian',
  'rom\u00e1n': 'romanian',
  'ruszin': 'rusyn',
  'szerb': 'serbian',
  'szlov\u00e1k': 'slovakian',
  'szlov\u00e9n': 'slovenian',
  'ukr\u00e1n': 'ukrainian',
  'hazai nemzetis\u00e9gek egy\u00fctt': 'sum of national minorities',
  'arab': 'arabic',
  'k\u00ednai': 'chinese',
  'orosz': 'russian',
  'vietnami': 'vietnamese',
  'egy\u00e9b': 'other',
  '\u00d6sszesen': 'sum',
  'N\u00e9pess\u00e9g ': 'population'  
}

IGNORED_NAMES = {
  'Megyeszékhely',
  'Többi város',
  'Községek, nagyközségek',
  'Megye összesen',
}

def merge_header_lines(line1, line2):
  reader_0 = csv.DictReader([line1])
  reader_1 = csv.DictReader([line2])

  header_fields = []
  for i, field in enumerate(reader_1.fieldnames):
    if field == '':
      header_fields.append(reader_0.fieldnames[i])
    else:
      header_fields.append(field)

  header_fields = [HEADER_TRANSLATION.get(field, field)
                   for field in header_fields]
  header_row = io.StringIO()
  writer = csv.DictWriter(header_row, header_fields)
  writer.writeheader()
  return header_row.getvalue()

def format_csv(f):
  for i, line in enumerate(f):
    if i == 0:
      first_line = line
      continue
    if i == 1:
      yield merge_header_lines(first_line, line)
      continue
    yield line

def filter_ignored_names(data):
  for row in data:
    if row['name'] not in IGNORED_NAMES:
      yield row

def add_county_to_dict(d, filename):
  d['county'] = pathlib.Path(filename).stem
  return d

def main():
  if len(sys.argv) < 3:
    print('Usage: population_data_to_json.py <input_file_names...> <output_file_name>')
    exit(1)
  result = []
  for input_file_name in sys.argv[1:-1]: 
    with open(input_file_name) as f:
      reader = csv.DictReader(format_csv(f))
      result += [add_county_to_dict(row, input_file_name)
       for row in filter_ignored_names(reader)]
  with open(sys.argv[-1], 'w') as f:
    json.dump(result, f, indent=2)

main()