#!/usr/bin/bash

docker build --build-arg http_proxy=$http_proxy --build-arg https_proxy=$https_proxy -t provisioning/donk .
