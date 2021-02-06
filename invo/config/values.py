import ast
from datetime import timedelta

from configurations import values


def cast_timedelta(self, value, **params):
    return timedelta(**value)


class TimeDeltaValue(values.CastingMixin, values.Value):
    """Use dict kwargs to get timedelta value"""

    # TODO: assert timedeta type
    caster = cast_timedelta

    def to_python(self, value):
        try:
            evaled_value = ast.literal_eval(value)
        except ValueError:
            raise ValueError(self.message.format(value))
        if not isinstance(evaled_value, dict):
            raise ValueError(self.message.format(value))
        return super().to_python(evaled_value)
