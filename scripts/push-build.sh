#!/bin/bash

set -e

docker build --rm --tag invo-build --file .docker/django/app . --target production
docker tag invo-build registry.digitalocean.com/invo/invo-build
docker push registry.digitalocean.com/invo/invo-build
