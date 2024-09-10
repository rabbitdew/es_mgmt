#!/bin/bash

search_oldest(){
  # Find the oldest document in an index.
  curl -s -X GET "$(hostname):9200/${ES_INDEX}/_search?pretty" -H 'Content-Type: application/json' -d'         
  {
     "size": 1,
     "sort": { "date": "desc"},
     "query": {
        "match_all": {}
     }
  }'
}

main(){
 search_oldest
}

main
