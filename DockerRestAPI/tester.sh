#!/bin/bash
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker rmi dockerrestapi_laptop-service
docker rmi dockerrestapi_web

