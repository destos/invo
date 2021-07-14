#!/bin/bash

set -e

doctl apps update 523266f9-9be5-46ac-a960-ceeb0d045fee --spec .do/app.yaml
