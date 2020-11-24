from graph.types import query


@query.field("getIrnEntity")
def get_irn_entity(root, info, irn=None, *args, **kwargs):
    return irn.get_instance()
