#!/bin/bash
docker build . -t homework:1
docker run -d -p 8000:8000 -v $PWD/vol:/app homework:1
