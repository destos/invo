from unittest.mock import Mock, patch
import json

import pytest
from glom import glom
from django.test import TestCase
from django.conf import settings
from ariadne import graphql_sync
from model_bakery import baker

from graph.schema import schema

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
    mutation doSelectEntities($input: SelectEntitiesInput!) {
        selectEntities(input: $input) {
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

    def test_select_entities_works(self):
        item = baker.make("items.Item")
        space = baker.make("spaces.SpaceNode")

        data = dict(
            query=select_entities,
            variables=dict(input=dict(irns=[item.irn, space.irn])),
            operationName="doSelectEntities",
        )
        success, result = graphql_sync(schema, data, context_value=self.context)

        self.assertTrue(success)
        self.assertEqual(int(glom(result["data"], "selectEntities.object.id")), self.situation.id)
