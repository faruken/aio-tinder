# -*- coding: utf-8 -*-

from unittest import TestCase

import os

from src.models.model import User


class TestUser(TestCase):
    def setUp(self):
        self.male = 0
        self.female = 1
        self._id = os.urandom(16)
        self.attributes = {
            "_id": self._id,
            "bio": "I'm a strong, independent woman who need no Tinder",
            "birth_date": "1982-03-07T11:11:11.411Z",
            "birth_date_info": "fuzzy birthdate active, not displaying real birth_date",
            "common_friend_count": 0,
            "common_friends": [],
            "common_like_count": 0,
            "common_likes": [],
            "connection_count": 12,
            "content_hash": "rz1V11BaiC9slYbm44F1jZW6GNvkrVDz3ysNr7fqpTwKcFP",
            "distance_mi": "6",
            "gender": self.female,
            "jobs": [],
            "name": "MLady",
            "photos": [],
            "ping_time": "2011-02-11T11:11:11.211Z",
            "schools": [],
            "teaser": {'string': ''}
        }
        self.user = User(**self.attributes)

    def test_getattr(self):
        with self.assertRaises(AttributeError):
            self.assertEqual(self.user.some_attr, 1)

    def test_user_age(self):
        self.assertEqual(self.user.age, 34)  # Meh
