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
```

Run black formattings:
```bash
poetry run black ./invo/apps
```