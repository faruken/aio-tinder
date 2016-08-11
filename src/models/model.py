# -*- coding: utf-8 -*-

"""Models
"""

from datetime import datetime
from typing import AnyStr, List, Any, Dict


class User:
    """User model
    """

    def __init__(self, *args: List[Any], **kwargs: Dict[Any, Any]) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getattr__(self, item) -> Any:
        """
        """
        try:
            return self.__dict__[item]
        except KeyError:
            raise AttributeError

    def __str__(self) -> AnyStr:
        """
        """
        return "{0}: {1}".format(self.name, self.age)

    def __repr__(self) -> AnyStr:
        """
        """
        return "<User ({0} - {1})>".format(self._id, self.name)

    @property
    def age(self) -> int:
        """Calculate user's age.
        :return: User's age
        """
        user_year = datetime.strptime(self.birth_date, "%Y-%m-%dT%H:%M:%S.%fZ").year
        current_year = datetime.utcnow().year
        return current_year - user_year
