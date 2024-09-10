#!/bin/bash

search_newest(){
  # Find the newest document in an index.
  curl -s -X GET "$(hostname):9200/${ES_INDEX}/_search?pretty" -H 'Content-Type: application/json' -d'         
  {
     "size": 1,
     "sort": { "date": "asc"},
     "query": {
        "match_all": {}
     }
  }'
}

main(){
 search_newest
}

main
