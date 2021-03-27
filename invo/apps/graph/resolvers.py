import asyncio
from typing import Any, AsyncGenerator, Dict

from ariadne.types import GraphQLResolveInfo
from channels.layers import get_channel_layer
from graph.types import subscription
from graphql.pyutils import EventEmitterAsyncIterator
from waffle.utils import get_setting
from asgiref.sync import async_to_sync, sync_to_async
from ariadne_extended.resolvers import Resolver
from ariadne_extended.contrib.waffle_graph.resolvers import FlagResolver as AEFlagResolver
from ariadne_extended.contrib.waffle_graph.types import waffle_type, waffle_item_interface


@subscription.source("counter")
async def counter_generator(obj, info):
    for i in range(50):
        await asyncio.sleep(0.05)
        yield i


@subscription.field("counter")
def counter_resolver(count, info):
    return count + 1


# subscription.set_field("counter", counter_resolver)
# subscription.set_source("counter", counter_generator)


@subscription.source("waffle")
async def waffle_subscription_generator(
    obj: Any, info: GraphQLResolveInfo
) -> AsyncGenerator[Dict, None]:
    channel_layer = get_channel_layer()
    yield dict()
    while True:
        msg = await channel_layer.receive("waffle_changed")
        yield msg


class FlagResolver(AEFlagResolver):
    def retrieve(self, parent, *args, **kwargs):
        return sync_to_async(self.get_object)()


class ActiveResolver(Resolver):
    def check(self, parent, *args, **kwargs):
        try:
            return sync_to_async(parent.is_active)(self.request)
        except TypeError:
            return sync_to_async(parent.is_active)()


waffle_type.set_field("flag", FlagResolver.as_resolver(method="retrieve"))
waffle_item_interface.set_field("active", ActiveResolver.as_resolver(method="check"))


@subscription.field("waffle")
async def waffle_resolver(obj, info):
    return (
        {
            "flag_default": get_setting("FLAG_DEFAULT"),
            "switch_default": get_setting("SWITCH_DEFAULT"),
            "sample_default": get_setting("SAMPLE_DEFAULT"),
            "flagDefault": get_setting("FLAG_DEFAULT"),
            "switchDefault": get_setting("SWITCH_DEFAULT"),
            "sampleDefault": get_setting("SAMPLE_DEFAULT"),
        },
    )
