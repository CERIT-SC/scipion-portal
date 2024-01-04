
from typing import Any, List, Callable
from datetime import datetime, timedelta

class CacheEntry:
    def __init__(self, expiration, id, object) -> None:
        self.expiration = expiration
        self.id = id
        self.object = object

class CacheMachine:
    def __init__(self) -> None:
        self.entries: List[CacheEntry] = list()

    def obtain_value(self, item_id, function: Callable) -> Any:
        # TODO it returns info about cached items without token verification!

        # Check the cache entries
        for cs in self.entries:
            if cs.id != item_id:
                continue

            # Item found in cache
            # Check expiration time
            if cs.expiration > datetime.now():
                # Entry still actual > return content
                return cs.object

            # Entry expired > remove from cache
            self.entries.remove(cs)
            break

        # Entry not found in cache or alredy expired > call the function
        result = function()

        # Save the data just acquired into the cache
        self.entries.append(
            CacheEntry(
                datetime.now() + timedelta(hours=1),
                item_id,
                result
            )
        )

        return result
