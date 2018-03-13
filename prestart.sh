#!/usr/bin/env bash

# Create docker network
docker network create frontend_net
docker network create backend_net

# Prepare mongo container
docker-compose -f mongo/mongo.yml up -d