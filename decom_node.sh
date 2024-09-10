#!/bin/bash

decom_node(){
  # In order to stop allocating shards to some node, you can POST this.
  # It will move shards off of it and allow you to remove the node
  # without impacting the cluster. Remove the config by setting it to 
  # 'null'
  
  Arg="${1}"
  
  if [[ "${Arg}" =~ ^[[:digit:]*][[:digit:]*,.]*$|null ]] ; then
    [[ "${Arg}" != "null" ]] && Arg="\"${Arg}\"" # "null" shouldnt' be quoted
    echo curl -X PUT "`hostname`:9200/_cluster/settings?pretty" -H 'Content-Type: application/json' -d'{"transient":{"cluster.routing.allocation.exclude._ip" : '"${Arg}"'}}'
  else
    echo "Usage: ${0} null|ip[,ip,...]"
    echo "Examples:"
    echo "${0} null"
    echo "${0} 1.2.3.4"
    echo "${0} 1.2.3.4,1.2.3.5"
    echo "${0} 1.2.3.*"
  fi
}

main(){
  decom_node
}
main
