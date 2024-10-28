#!/usr/bin/env python3
import requests
OUTPUT_FILE = 'my_file.txt'
ES_URL = '127.0.0.1:9200'
ES_INDEX = 'some_index'
DATE_START = '2020-01-01 00:00:00'
DATE_END = '2020-01-02 12:00:00'
SEARCH_SIZE = 10_000
SCROLL_JSON = {
  "size": str(SEARCH_SIZE),
  "query": {
    "range": {
      "date": {
        "gt": DATE_START,
        "lt": DATE_END
      }
    }
  }
}
COUNT_JSON = {
  "query": {
    "range": {
      "date": {
        "gt": DATE_START,
        "lt": DATE_END
      }
    }
  }
}
return_list = []

def count_it():
  """
  Make query and return integer with total number of documents.
  """
  r = requests.get('http://' + ES_URL + '/' + ES_INDEX + '/_count?',json=COUNT_JSON)
  return(int(r.json()['count']))

def scroll_it_init():
  """
  Initial search and returns scroll_id for next call.
  """
  myparams = {'scroll':'3m'}
  r = requests.post('http://' + ES_URL + '/' + ES_INDEX + '/_search',params=myparams,json=SCROLL_JSON)
  print(r.status_code)
  my_dict = dict(r.json())
  for item in my_dict['hits']['hits']:
    return_list.append(item['_source'])
  return(r.json()['_scroll_id'])

def scroll_next(myScrollID):
  """
  Takes scrollID as argument and returns the next page of results.
  """
  SCROLL_NEXT_JSON = {
    "scroll" : "3m",
    "scroll_id": str(myScrollID)
     }
  r = requests.post('http://' + ES_URL +  '/_search/scroll/',json=SCROLL_NEXT_JSON)
  my_dict = dict(r.json())
  for item in my_dict['hits']['hits']:
    return_list.append(item['_source'])
  return(r.status_code)

def main():
  total_docs = count_it()
  print('count API reports: ' + str(total_docs) + ' total documents.')
  print('Search size is set to: ' + str(SEARCH_SIZE))
  # This is the total number of times to run the search. The 'init' function
  # counts as the first run. 
  total_runs = (total_docs // SEARCH_SIZE) + (total_docs % SEARCH_SIZE > 0)
  print('Will make: ' + str(total_runs) + ' total runs')

  my_id = scroll_it_init()
  for i in range(total_runs - 1):
    print('trying run: ' + str(i))
    print('returned: ' + str(scroll_next(my_id)) + '\n')
  return_list_sorted = sorted(return_list, key=lambda k: k['date']) 
  with open(OUTPUT_FILE,'w') as f:
    for item in return_list_sorted:
      f.write(str(item) + '\n')
  print('completed')
  print('Total items in list: ' + str(len(return_list)))

if __name__ == "__main__":
  main()
