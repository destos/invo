#!/bin/bash

set -e

docker build --rm --tag invo-build --file .docker/django/Dockerfile . --target production
