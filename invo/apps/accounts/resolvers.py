from ariadne_extended.resolvers.model import ModelResolver
from graph.types import query

from .types import group, permission, user


class CurrentUserResolver(ModelResolver):
    def retrieve(self, parent, **kwargs):
        if self.info.context.user.id is None:
            return None
        return self.info.context.user


query.set_field("currentUser", CurrentUserResolver.as_resolver(method="retrieve"))


@group.field("permissions")
def resolve_permissions(obj, info):
    return obj.permissions.all()


@user.field("userPermissions")
def resolve_user_permissions(obj, info):
    return obj.user_permissions.all()


@user.field("allPermissions")
def resolve_all_permissions(obj, info):
    return obj.get_all_permissions()


@user.field("groupPermissions")
def resolve_group_permissions(obj, info):
    return obj.get_group_permissions()


@user.field("groups")
def resolve_groups_permissions(obj, info):
    return obj.groups.all()


@permission.field("contentType")
def resolve_content_type(obj, info):
    return obj.content_type.app_label
