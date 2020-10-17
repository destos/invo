from django.test import TestCase
from django.conf import settings
import django_fsm
from model_bakery import baker
from .models import Situation


# Create your tests here.
class TestSituation(TestCase):
    def setUp(self):
        self.user = baker.make(settings.AUTH_USER_MODEL)

    def test_selecting_space(self):
        situ = baker.make(Situation, user=self.user)
        space = baker.make("spaces.SpaceNode")

        self.assertEqual(situ.state, Situation.States.START)
        situ.select_space(space)
        self.assertEqual(space, situ.space)
        self.assertEqual(situ.state, Situation.States.SELECTING)

    def test_selecting_item(self):
        situ = baker.make(Situation, user=self.user)
        item = baker.make("items.Item")

        self.assertEqual(situ.state, Situation.States.START)
        situ.select_item(item)
        self.assertEqual(item, situ.item)
        self.assertEqual(situ.state, Situation.States.SELECTING)
    
    def test_selecting_in_bad_state(self):
        situ = baker.make(Situation, user=self.user, state=Situation.States.PLACING)
        item = baker.make("items.Item")
        space = baker.make("spaces.SpaceNode")

        # Select item
        self.assertEqual(situ.state, Situation.States.PLACING)
        with self.assertRaises(django_fsm.TransitionNotAllowed):
            situ.select_item(item)

        self.assertNotEqual(item, situ.item)

        # Select space
        self.assertEqual(situ.state, Situation.States.PLACING)
        with self.assertRaises(django_fsm.TransitionNotAllowed):
            situ.select_space(space)

        self.assertNotEqual(space, situ.space)
        self.assertEqual(situ.state, Situation.States.PLACING)
    
    def test_chose_item(self):
        space = baker.make("spaces.SpaceNode")
        situ = baker.make(Situation, user=self.user, state=Situation.States.SELECTING, space=space)

        self.assertEqual(situ.state, Situation.States.SELECTING)
        situ.chose_item()
        self.assertEqual(situ.state, Situation.States.ADDING)

    def test_chose_item_no_space(self):
        situ = baker.make(Situation, user=self.user, state=Situation.States.SELECTING)

        self.assertEqual(situ.state, Situation.States.SELECTING)
        with self.assertRaises(django_fsm.TransitionNotAllowed):
            situ.chose_item()
        self.assertEqual(situ.state, Situation.States.SELECTING)

    def test_chose_space(self):
        item = baker.make("items.Item")
        situ = baker.make(Situation, user=self.user, state=Situation.States.SELECTING, item=item)

        self.assertEqual(situ.state, Situation.States.SELECTING)
        situ.chose_space()
        self.assertEqual(situ.state, Situation.States.PLACING)

    def test_chose_space_no_item(self):
        situ = baker.make(Situation, user=self.user, state=Situation.States.SELECTING)

        self.assertEqual(situ.state, Situation.States.SELECTING)
        with self.assertRaises(django_fsm.TransitionNotAllowed):
            situ.chose_space()
        self.assertEqual(situ.state, Situation.States.SELECTING)

    def test_chose_item_space_bad_state(self):
        item = baker.make("items.Item")
        space = baker.make("spaces.SpaceNode")
        situ = baker.make(Situation, user=self.user, state=Situation.States.START, item=item)

        self.assertEqual(situ.state, Situation.States.START)
        with self.assertRaises(django_fsm.TransitionNotAllowed):
            situ.chose_item()
        self.assertEqual(situ.state, Situation.States.START)

        situ = baker.make(Situation, user=self.user, state=Situation.States.START, space=space)
        self.assertEqual(situ.state, Situation.States.START)
        with self.assertRaises(django_fsm.TransitionNotAllowed):
            situ.chose_space()
        self.assertEqual(situ.state, Situation.States.START)

    # Can have an item and space re-assigned.
    # Can be replaced with a new situation, abandoned/deleted
    # Deleted situations are still available for lookup/history


class TestSituationQuerySet(TestCase):
    def test_get_active(self):
        pass
