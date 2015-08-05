
import redis

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from relationships import Relationship
from relationships.relationship import default_key_list


class RelationshipsTestCase(unittest.TestCase):

    def setUp(self):
        self.redis_connection = redis.StrictRedis(
            host='localhost',
            port=6379,
            db=15)

    def tearDown(self):
        self.redis_connection.flushdb()

    def test_no_redis_connection(self):
        r = Relationship()

        self.assertEqual(r.redis_connection.connection_pool.connection_kwargs.get("host"), "localhost")
        self.assertEqual(r.redis_connection.connection_pool.connection_kwargs.get("db"), 0)
        self.assertEqual(r.redis_connection.connection_pool.connection_kwargs.get("port"), 6379)

    def test_follow(self):
        r = Relationship(redis_connection=self.redis_connection)

        r(1).follow(42)

        self.assertEqual(r(1).is_following(42), True)
        self.assertEqual(r(42).is_follower(1), True)

    def test_unfollow(self):
        r = Relationship(redis_connection=self.redis_connection)

        r(2).follow(42)
        r(2).unfollow(42)

        self.assertEqual(r(2).is_following(42), False)
        self.assertEqual(r(42).is_follower(2), False)

    def test_block(self):

        r = Relationship(redis_connection=self.redis_connection)

        r(1).block(42)

        self.assertEqual(r(1).is_blocked(42), True)
        self.assertEqual(r(42).is_blocked_by(1), True)

    def test_unblock(self):

        r = Relationship(redis_connection=self.redis_connection)

        r(2).block(42)
        r(2).unblock(42)

        self.assertEqual(r(42).is_blocked_by(2), False)
        self.assertEqual(r(2).is_blocked(42), False)

    def test_friends(self):
        r = Relationship(redis_connection=self.redis_connection)

        r(5).follow(1)
        r(1).follow(5)

        r(100).follow(1)
        r(1).follow(100)

        self.assertEqual(r(1).friends(), set(['100', '5']))

    def test_follower_count(self):

        r = Relationship(redis_connection=self.redis_connection)

        r(1000).follow(2000)
        r(1001).follow(2000)
        r(1002).follow(2000)

        self.assertEqual(r(2000).follower_count(), 3)

    def test_following_count(self):

        r = Relationship(redis_connection=self.redis_connection)

        r(1000).follow(2000)
        r(1000).follow(1001)

        self.assertEqual(r(1000).following_count(), 2)

    def test_blocked_by_count(self):

        r = Relationship(redis_connection=self.redis_connection)

        r(1000).block(2000)
        r(1001).block(2000)
        r(1002).block(2000)

        self.assertEqual(r(2000).blocked_count(), 3)

    def test_blocking_count(self):

        r = Relationship(redis_connection=self.redis_connection)

        r(1000).block(2000)
        r(1000).block(2001)

        self.assertEqual(r(1000).block_count(), 2)

    def test_followers(self):

        r = Relationship(redis_connection=self.redis_connection)

        r(10000).follow(100)
        r(10001).follow(100)
        r(10002).follow(100)

        self.assertEqual(r(100).followers(), set(['10000', '10001', '10002']))

    def test_following(self):

        r = Relationship(redis_connection=self.redis_connection)

        r(100).follow(900)
        r(100).follow(901)

        self.assertEqual(r(100).following(), set(['900', '901']))

    def test_blocked(self):

        r = Relationship(redis_connection=self.redis_connection)

        r(100).block(900)
        r(100).block(901)

        self.assertEqual(r(100).blocks(), set(['900', '901']))

    def test_blocked_by(self):

        r = Relationship(redis_connection=self.redis_connection)

        r(10000).block(100)
        r(10001).block(100)
        r(10002).block(100)

        self.assertEqual(r(100).blocked(), set(['10000', '10001', '10002']))


if __name__ == '__main__':
    unittest.main()