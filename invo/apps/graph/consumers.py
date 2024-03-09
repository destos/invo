import asyncio
from typing import Any, AsyncGenerator, Dict, List, cast

from ariadne.asgi import (
    GQL_COMPLETE,
    GQL_CONNECTION_ACK,
    GQL_CONNECTION_INIT,
    GQL_CONNECTION_TERMINATE,
    GQL_DATA,
    GQL_ERROR,
    GQL_START,
    GQL_STOP,
)
from ariadne.format_error import format_error
from ariadne.graphql import subscribe
from ariadne.logger import log_error
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from graphql import GraphQLError


class WebSocketGraphQL(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscription_sources = []

    async def connect(self):
        await self.channel_layer.group_add("graphql-ws", self.channel_name)
        await self.accept()

    async def receive_json(self, message: dict, subscriptions: Dict[str, AsyncGenerator] = {}):
        operation_id = cast(str, message.get("id"))
        message_type = cast(str, message.get("type"))

        if message_type == GQL_CONNECTION_INIT:
            await self.send_json({"type": GQL_CONNECTION_ACK})
        elif message_type == GQL_CONNECTION_TERMINATE:
            await self.close()
        elif message_type == GQL_START:
            await self.start_websocket_subscription(
                message.get("payload"), operation_id, subscriptions
            )
        elif message_type == GQL_STOP:
            if operation_id in subscriptions:
                await subscriptions[operation_id].aclose()
                del subscriptions[operation_id]
            if not len(subscriptions):
                await self.close()

    async def start_websocket_subscription(
        self, data: Any, operation_id: str, subscriptions: Dict[str, AsyncGenerator]
    ):
        subscription_source = await self.channel_layer.new_channel()
        self.subscription_sources.append(subscription_source)
        # context_value = await self.get_context_for_request(websocket)
        context_value = {
            "request": self.scope,
            "subscription_source": subscription_source,
        }

        success, results = await subscribe(
            self.schema,
            data,
            context_value=context_value,
            debug=False,
            error_formatter=format_error,
        )
        if not success:
            results = cast(List[dict], results)
            await self.send_json({"type": GQL_ERROR, "id": operation_id, "payload": results[0]})
        else:
            results = cast(AsyncGenerator, results)
            subscriptions[operation_id] = results
            asyncio.ensure_future(self.observe_async_results(results, operation_id))

    async def observe_async_results(self, results: AsyncGenerator, operation_id: str) -> None:
        try:
            async for result in results:
                payload = {}
                if result.data:
                    payload["data"] = result.data
                if result.errors:
                    for error in result.errors:
                        log_error(error, self.logger)
                    payload["errors"] = [
                        format_error(error, self.debug) for error in result.errors
                    ]
                await self.send_json({"type": GQL_DATA, "id": operation_id, "payload": payload})
        except Exception as error:
            if not isinstance(error, GraphQLError):
                error = GraphQLError(str(error), original_error=error)
            log_error(error, self.logger)
            payload = {"errors": [format_error(error, self.debug)]}
            await self.send_json({"type": GQL_DATA, "id": operation_id, "payload": payload})

        await self.send_json({"type": GQL_COMPLETE, "id": operation_id})

    async def disconnect(self, code):
        await self.channel_layer.group_discard("graphql-ws", self.channel_name)
