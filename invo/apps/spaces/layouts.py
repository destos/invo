from numbers import Number
from decimal import Decimal
from measurement.measures import Distance, Volume
from typing import NamedTuple, Union


class Layout(NamedTuple):
    """
    Layout object used to represent grid layout and positioning for a space
    """

    x: int
    y: int
    w: int
    h: int

    def inside(self, x, y):
        return (self.x <= x <= (self.x + self.h - 1)) and (self.y <= y <= (self.y + self.w - 1))

    def __mul__(self, value):
        "Iterate and apply delta to all layout values"

        def check(final):
            if final == int(final):
                return int(final)
            # if isinstance(final, int):
            #     return final
            raise TypeError(f"delta of: {value} produced a non-integer: {final}")

        if isinstance(value, Number):
            return self._make([check(i * value) for i in self])
        else:
            raise NotImplementedError

    def __truediv__(self, value):
        "Iterate and apply delta to all layout values"

        def check(final):
            if final == int(final):
                return int(final)
            # if isinstance(final, int):
            #     return final
            raise TypeError(f"delta of: {value} produced a non-integer: {final}")

        if isinstance(value, Number):
            return self._make([check(i / value) for i in self])
        else:
            raise NotImplementedError


class LayoutReconciler:
    def __init__(self, layouts, container=None, **kwargs):
        self.container = container
        self.layouts = layouts

    def validate(self):
        # Checks total dimensions
        pass

    def scale(self, distance, throw_if_collision=False):
        scale = Decimal(distance / self.container.get("scale"))
        self.container["scale"] = distance
        # self.container
        # If we aren't scaling, don't do anything
        if scale == 1:
            return None

        # If increasing scale layout is easy
        if scale > 1:
            for k, l in self.layouts.items():
                self.layouts[k] = l * scale
        # if decreasing scale make sure we can scale down properly
        else:
            for k, l in self.layouts.items():
                self.layouts[k] = l * scale

    def reconcile(self):
        pass
