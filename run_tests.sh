#!/bin/bash

docker-compose -f docker-compose-tests.yaml up -d

docker-compose -f docker-compose-tests.yaml logs -f menu-app-tests

docker-compose -f docker-compose-tests.yaml down --volumes
