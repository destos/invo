import arrow
import django_fsm
import ipdb
from django.conf import settings
from django.test import TestCase
from model_bakery import baker
import pytest

from situations.models import Situation


# Create your tests here.
class TestSituation(TestCase):
    def setUp(self):
        self.user = baker.make(settings.AUTH_USER_MODEL, email="test@user.com")

    def test_attr(self):
        situ = baker.make(Situation, user=self.user)
        self.assertEqual(str(situ), "test@user.com (Start, Open)")
        self.assertEqual(repr(situ), "<Situation: test@user.com (Start, Open)>")
        self.assertEqual(situ._meta.get_latest_by, "modified")
        self.assertEqual(situ._meta.ordering, ("created",))
        self.assertEqual(situ._meta.abstract, False)

    def test_does_not_delete_related_site_or_user_when_deleted(self):
        pass

    def test_select(self):
        "Select a space and item"
        situ = baker.make(Situation, user=self.user)
        space = baker.make("spaces.SpaceNode")
        item = baker.make("items.Item")
        self.assertEqual(situ.state, Situation.States.START)

        situ.select(space, item)

        self.assertEqual(situ.state, Situation.States.SELECTING)
        self.assertSequenceEqual(situ.spaces.all(), [space])
        self.assertSequenceEqual(situ.items.all(), [item])

    def test_unselect(self):
        space1 = baker.make("spaces.SpaceNode", name="space1")
        space2 = baker.make("spaces.SpaceNode", name="space2")
        baker.make("spaces.SpaceNode", name="extra_space")
        item1 = baker.make("items.Item", name="item1")
        item2 = baker.make("items.Item", name="item2")
        baker.make("items.Item", name="extra_item")
        space1._meta.model.objects.rebuild()

        situ = baker.make(
            Situation,
            user=self.user,
            items=[item1, item2],
            spaces=[space1, space2],
            state=Situation.States.SELECTING,
        )

        self.assertEqual(situ.state, Situation.States.SELECTING)

        self.assertSequenceEqual(situ.spaces.all(), [space1, space2])
        self.assertSequenceEqual(situ.items.all(), [item1, item2])

        situ.unselect(space1, item1)

        self.assertEqual(situ.state, Situation.States.SELECTING)
        self.assertSequenceEqual(situ.spaces.all(), [space2])
        self.assertSequenceEqual(situ.items.all(), [item2])

    def test_selecting_space(self):
        situ = baker.make(Situation, user=self.user)
        space = baker.make("spaces.SpaceNode")

        self.assertEqual(situ.state, Situation.States.START)
        situ.select(space)
        self.assertSequenceEqual([space], situ.spaces.all())
        self.assertEqual(situ.state, Situation.States.SELECTING)

    def test_selecting_item(self):
        situ = baker.make(Situation, user=self.user)
        item = baker.make("items.Item")

        self.assertEqual(situ.state, Situation.States.START)
        situ.select(item)
        self.assertSequenceEqual([item], situ.items.all())
        self.assertEqual(situ.state, Situation.States.SELECTING)

    def test_select_in_bad_start_state(self):
        situ = baker.make(Situation, user=self.user, state=Situation.States.PLACING)
        item = baker.make("items.Item")
        space = baker.make("spaces.SpaceNode")

        # Select item
        self.assertEqual(situ.state, Situation.States.PLACING)
        with self.assertRaises(django_fsm.TransitionNotAllowed):
            situ.select(item)

        self.assertSequenceEqual(situ.items.all(), [])

        # Select space
        self.assertEqual(situ.state, Situation.States.PLACING)
        with self.assertRaises(django_fsm.TransitionNotAllowed):
            situ.select(space)

        self.assertSequenceEqual(situ.spaces.all(), [])
        self.assertEqual(situ.state, Situation.States.PLACING)

    # def test_chose_item(self):
    #     space = baker.make("spaces.SpaceNode")
    #     situ = baker.make(Situation, user=self.user, state=Situation.States.SELECTING, space=space)

    #     self.assertEqual(situ.state, Situation.States.SELECTING)
    #     situ.chose_item()
    #     self.assertEqual(situ.state, Situation.States.ADDING)

    # def test_chose_item_no_space(self):
    #     situ = baker.make(Situation, user=self.user, state=Situation.States.SELECTING)

    #     self.assertEqual(situ.state, Situation.States.SELECTING)
    #     with self.assertRaises(django_fsm.TransitionNotAllowed):
    #         situ.chose_item()
    #     self.assertEqual(situ.state, Situation.States.SELECTING)

    # def test_chose_space(self):
    #     item = baker.make("items.Item")
    #     situ = baker.make(Situation, user=self.user, state=Situation.States.SELECTING, item=item)

    #     self.assertEqual(situ.state, Situation.States.SELECTING)
    #     situ.chose_space()
    #     self.assertEqual(situ.state, Situation.States.PLACING)

    # def test_chose_space_no_item(self):
    #     situ = baker.make(Situation, user=self.user, state=Situation.States.SELECTING)

    #     self.assertEqual(situ.state, Situation.States.SELECTING)
    #     with self.assertRaises(django_fsm.TransitionNotAllowed):
    #         situ.chose_space()
    #     self.assertEqual(situ.state, Situation.States.SELECTING)

    # def test_chose_item_space_bad_state(self):
    #     item = baker.make("items.Item")
    #     space = baker.make("spaces.SpaceNode")
    #     situ = baker.make(Situation, user=self.user, item=item)

    #     self.assertEqual(situ.state, Situation.States.START)
    #     with self.assertRaises(django_fsm.TransitionNotAllowed):
    #         situ.chose_item()
    #     self.assertEqual(situ.state, Situation.States.START)

    #     situ = baker.make(Situation, user=self.user, space=space)
    #     self.assertEqual(situ.state, Situation.States.START)
    #     with self.assertRaises(django_fsm.TransitionNotAllowed):
    #         situ.chose_space()
    #     self.assertEqual(situ.state, Situation.States.START)

    # Can have an item and space re-assigned.
    # Can be replaced with a new situation, abandoned/deleted
    # Deleted situations are still available for lookup/history


class TestSituationScenarios(TestCase):
    def setUp(self):
        self.user = baker.make(settings.AUTH_USER_MODEL, email="test@email.com")

    def test_adding_new_part(self):
        item = baker.make("items.Item")
        space = baker.make("spaces.SpaceNode")
        situ = baker.make(Situation, user=self.user)

        # When a space is selected first
        situ.select(space)
        situ.select(item)

        # situ.available_transitions

    # only item selected is inside space selected, remove item
    # selecting many items in a space and one item in another space suggests moving items to other space
    #


@pytest.mark.django_db()
def test_selection():