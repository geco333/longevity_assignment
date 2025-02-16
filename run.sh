#!/usr/bin/bash

docker build . -t health_score:latest

docker run -p 5000:5000 health_score:latest
