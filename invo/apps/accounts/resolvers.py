from ariadne_extended.resolvers.model import ModelResolver

from .serializers import UserSerializer
from .types import group, permission, user
from graph.types import mutation, query


class UserResolver(ModelResolver):
    serializer_class = UserSerializer
    # TODO: rate limit/block user creates

    def current(self, parent, **kwargs):
        # TODO: should this check that user belongs to current site? likely
        if self.request.user.id is None:
            return None
        return self.request.user


query.set_field("currentUser", UserResolver.as_resolver(method="current"))
mutation.set_field("createUser", UserResolver.as_resolver(method="create"))


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
