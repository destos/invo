import pghistory
from functools import wraps

# TODO: likely can exclude polymorphic ids/fields?
def enable_history(**track_kwargs):
    @wraps(pghistory.track)
    def wrapped(model):
        event = pghistory.Snapshot(("%s_snapshot" % model.__name__).lower())
        model_name = "%sEvent" % model.__name__
        excluded = getattr(model._meta, "exclude_history_fields", [])
        fields = [
            f.name for f in model._meta.fields if f.name not in excluded and f.model is model
        ]
        defaults = dict(model_name=model_name, fields=fields, related_name="+")
        defaults.update(track_kwargs)
        return pghistory.track(event, **defaults)(model)

    return wrapped
