- [ ] ability to take pictures and assign them to spaces/items
- [ ] protocol QR code

Action context idea.
Different steps in the app put specific users into a certain action context.
These action contexts help the user chose their next step or helps filter the actions they can perform that are relevant to what task they are trying to perform.

Context timeouts?

Contexts/Situations:
Are contexts like branches/trees of actions? Is there a logic tree builder we can make? or should it be simpler?

placing
consuming

Notes from conversation with Andrew:
Is there an API for skus for easy populating?

Associating an item with a QR code that exists for a bin.
take a picture of text describe an item in that bin.
When I scan this, I want you to tell me about this.
image recognition of something I want or need. take a picture of a thing, keep it in the box. text+picture.

# When using this app I would like to:

## See contents of inventory for scanned space
trigger actions:
* Scan a space

## Chose a space to place inventory into
trigger actions
* Scan an item
* Scan an item then a space ( confirm )

## Remove an items (float)
trigger actions
* Scan an item
* Scan a space ( see all items )

Ideas:
Scan an item, see what spaces it has belonged to? Where does it need to go?

# Ideas
When using barcodes or non unique ways of identification, allow for lookup of all items that use that serialized code.

# Bits

Make the requirements.txt for github
```bash
poetry export -f requirements.txt --output requirements.txt
```

Run tests with test config:
```bash
DJANGO_CONFIGURATION=Test poetry run ptw -- -s invo/apps
DJANGO_CONFIGURATION=Test poetry run pytest
```

Run black formatting:
```bash
poetry run black ./invo/
```

Start elasticsearch
```bash
docker run -d --name elasticsearch --net bridge -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:5.6.16
```

To org
doctl apps create --spec .do/app.yaml
doctl apps update 8ebdb3cf-70d8-4151-86a0-864257659b54 --spec .do/app.yaml

poetry export -f requirements.txt -o requirements.txt

docker build --rm --tag invo-test --file .docker/django/app . --target test
docker build --rm --tag invo-prod --file .docker/django/app . --target production

poetry run isort invo/apps ./manage.py
ngrok start invo_app invo_api
docker-compose run --name invo_debug_app --rm --service-ports app
docker-compose run --name qmonitor --rm django ./manage.py qmonitor

```bash
# Run the django shell container
docker-compose run --name invo_debug_app_shell --rm --service-ports django_shell

# Isort on app
poetry run isort invo/
```
