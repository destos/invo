import arrow
import django_fsm
from django.conf import settings
from django.test import TestCase
from model_bakery import baker

from situations.models import Situation


class TestSituationManager(TestCase):
    def setUp(self):
        self.user = baker.make(settings.AUTH_USER_MODEL, email="test@email.com")

    def test_get_active(self):
        situ = baker.make(Situation, user=self.user)
        baker.make(Situation, user=self.user).delete()
        baker.make(Situation, user=self.user, exit_condition=Situation.Exit.ABANDONED)
        baker.make(Situation, user=self.user, exit_condition=Situation.Exit.COMPLETED)

        # The active situation should be an open non-deleted one
        active_situ = Situation.objects.get_active(self.user)
        self.assertEqual(active_situ, situ)
        self.assertEqual(Situation.all_objects.count(), 4)

    def test_get_active_no_deleted(self):
        "More recently deleted situation isn't selected"
        baker.make(Situation, user=self.user).delete()
        baker.make(Situation, user=self.user)
        situ = baker.make(Situation, user=self.user)
        baker.make(Situation, user=self.user).delete()

        active_situ = Situation.objects.get_active(self.user)
        self.assertEqual(active_situ, situ)
        self.assertEqual(active_situ.state, Situation.States.START)
        # Should delete all but active situation
        self.assertEqual(Situation.all_objects.count(), 4)
        self.assertEqual(Situation.deleted_objects.count(), 3)
        self.assertEqual(Situation.objects.count(), 1)

    def test_get_active_past_timeout(self):
        "Active situations that are past the active time range"
        situ1 = baker.make(
            Situation,
            user=self.user,
            state=Situation.States.SELECTING,
            modified=arrow.now().shift(hours=-2).datetime,
            _save_kwargs=dict(update_modified=False),
        )
        situ2 = baker.make(
            Situation,
            user=self.user,
            state=Situation.States.SELECTING,
            modified=arrow.now().shift(days=-3).datetime,
            _save_kwargs=dict(update_modified=False),
        )

        no_situ = Situation.objects.get_active(self.user)
        self.assertIsNone(no_situ)
        self.assertSequenceEqual(Situation.deleted_objects.all(), [situ1, situ2])

    def test_get_active_in_timeout_range(self):
        "Active situations that are past the active time range"
        latest_situ = baker.make(
            Situation,
            user=self.user,
            state=Situation.States.SELECTING,
            modified=arrow.now().shift(minutes=-30).datetime,
            _save_kwargs=dict(update_modified=False),
        )
        extra1 = baker.make(
            Situation,
            user=self.user,
            state=Situation.States.SELECTING,
            modified=arrow.now().shift(days=-3).datetime,
            _save_kwargs=dict(update_modified=False),
        )
        extra2 = baker.make(
            Situation,
            user=self.user,
            state=Situation.States.SELECTING,
            modified=arrow.now().shift(minutes=-60).datetime,
            _save_kwargs=dict(update_modified=False),
        )
        extra3 = baker.make(
            Situation,
            user=self.user,
            state=Situation.States.SELECTING,
            modified=arrow.now().shift(minutes=-59).datetime,
            _save_kwargs=dict(update_modified=False),
        )

        active_situ = Situation.objects.get_active(self.user)

        # most recently created situation it within the timeout range and is returned as active
        # All others are deleted
        self.assertEqual(active_situ, latest_situ)
        self.assertSequenceEqual(Situation.deleted_objects.all(), [extra1, extra2, extra3])

    def test_get_active_not_dirty_past_timeout(self):
        """
        When a situation hasn't been made dirty by actions on it and it is past the timeout,
        still use it as the active
        """
        situ1 = baker.make(
            Situation,
            user=self.user,
            state=Situation.States.START,
            modified=arrow.now().shift(hours=-2).datetime,
            _save_kwargs=dict(update_modified=False),
        )
        situ2 = baker.make(
            Situation,
            user=self.user,
            state=Situation.States.START,
            modified=arrow.now().shift(days=-3).datetime,
            _save_kwargs=dict(update_modified=False),
        )

        situ = Situation.objects.get_active(self.user)
        situ2.refresh_from_db()

        self.assertEqual(situ, situ1)
        self.assertEqual(situ2.exit_condition, Situation.Exit.ABANDONED)
        self.assertSequenceEqual(Situation.deleted_objects.all(), [situ2])
