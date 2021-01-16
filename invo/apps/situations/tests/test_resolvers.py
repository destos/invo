import json
from unittest.mock import Mock, patch

import pytest
from ariadne import graphql_sync
from django.conf import settings
from django.test import TestCase
from glom import glom
from graph.schema import schema
from model_bakery import baker

active_query = """
    query {
        activeSituation {
            id
            created
            modified
        }
    }
"""

select_entities = """
    mutation doSelectEntities($irns: [IRN!]!) {
        selectEntities(irns: $irns) {
            success
            object {
                ... on Node {
                    id
                }
                items {
                    ... on ItemInterface {
                        id
                    }
                }
                spaces {
                    ... on SpaceInterface {
                        id
                    }
                }
            }
        }
    }
"""

unselect_entities = """
    mutation doUnselectEntities($irns: [IRN!]!) {
        unselectEntities(irns: $irns) {
            success
            object {
                ... on Node {
                    id
                }
                items {
                    ... on ItemInterface {
                        id
                    }
                }
                spaces {
                    ... on SpaceInterface {
                        id
                    }
                }
            }
        }
    }
"""


class TestSituationResolver(TestCase):
    def setUp(self):
        self.user = baker.make(settings.AUTH_USER_MODEL, username="test_user")

        self.context = Mock("MockContext")
        self.context.user = self.user

        self.situation = baker.make("situations.Situation", user=self.user)

    def test_active_new_generated(self):
        # Previous situation is deleted
        self.situation.delete()
        success, result = graphql_sync(
            schema, dict(query=active_query), context_value=self.context
        )

        self.assertTrue(success)
        self.assertNotEqual(int(glom(result["data"], "activeSituation.id")), self.situation.id)

    def test_active_existing(self):
        success, result = graphql_sync(
            schema, dict(query=active_query), context_value=self.context
        )

        self.assertTrue(success)
        self.assertEqual(int(glom(result["data"], "activeSituation.id")), self.situation.id)

    def test_active_no_user(self):
        # Should return no active
        pass

    def test_select_entities_e2e(self):
        item = baker.make("items.Item")
        space = baker.make("spaces.SpaceNode")

        data = dict(
            query=select_entities,
            variables=dict(irns=[item.irn, space.irn]),
            operationName="doSelectEntities",
        )
        success, result = graphql_sync(schema, data, context_value=self.context)

        self.assertTrue(success)
        self.assertEqual(int(glom(result["data"], "selectEntities.object.id")), self.situation.id)
        self.assertEqual(int(glom(result["data"], "selectEntities.object.items.0.id")), item.id)
        self.assertEqual(int(glom(result["data"], "selectEntities.object.spaces.0.id")), space.id)

    def test_unselect_entities_e2e(self):
        item = baker.make("items.Item")
        space = baker.make("spaces.SpaceNode")
        self.situation.items.add(item)
        self.situation.spaces.add(space)
        self.situation.state = self.situation.States.SELECTING
        self.situation.save()
        self.situation.refresh_from_db()

        data = dict(
            query=unselect_entities,
            variables=dict(irns=[item.irn, space.irn]),
            operationName="doUnselectEntities",
        )
        success, result = graphql_sync(schema, data, context_value=self.context)

        self.assertTrue(success)
        self.assertEqual(
            int(glom(result["data"], "unselectEntities.object.id")), self.situation.id
        )
        self.assertEqual(glom(result["data"], "unselectEntities.object.items"), [])
        self.assertEqual(glom(result["data"], "unselectEntities.object.spaces"), [])

    def test_abandon_situation(self):
        "When you need to start your selection over"
        pass
