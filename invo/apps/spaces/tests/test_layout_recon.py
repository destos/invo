import pytest
from measurement.measures import Distance, Volume
from spaces.layouts import Layout, LayoutReconciler

from rich import print
from rich.table import Table
from rich.panel import Panel


def print_layouts(layouts):
    # print_layouts =
    bare = layouts.values()
    max_x = max([b.x + b.h for b in bare])
    max_y = max([b.y + b.w for b in bare])
    table = Table.grid(expand=True, padding=0)

    for x in range(max_x):
        table.add_column()

    print(f"table: {max_x} {max_y}")
    for x in range(max_x):
        row = []
        for y in range(max_y):
            found = None
            for key, layout in layouts.items():
                l = layout
                if layout.inside(x, y):
                    found = key
                    # For each point only one location is valid
                    break
            if found:
                row.append(Panel(found))
            else:
                row.append(Panel(f"x:{x} y:{y}"))
        table.add_row(*row)
    print(table)


# @pytest.mark.django_db()
def test_layout_grid_reconciliation():
    """
    Grid reconciliation

    How does it work? takes a list of existing space nodes and applies a scaling that makes sure

    if the scaling factor produces an un-even layout we need to resolve that invalid positioning with all siblings.
    # Layout must maintain integer values for layout positioning
    """
    layouts = dict(
        # Full top width, should always scale without issue
        a=Layout(0, 0, 5, 1),
        # Offset by one on the left, floating
        b=Layout(1, 1, 1, 1),
        # Next to floating one by one, a 2x2
        c=Layout(1, 2, 2, 2),
    )

    print_layouts(layouts)

    container = dict(scale=Distance(cm=10), width=Distance(m=50), height=Distance(cm=50))
    recon = LayoutReconciler(layouts, container=container)
    # scale up
    recon.scale(Distance(cm=50))
    print_layouts(layouts)

    # scale down
    recon.scale(Distance(cm=25))
    print_layouts(layouts)
    # new_layouts = recon.scale_to(Distance(cm=20))
    # assert new_layouts != layouts
