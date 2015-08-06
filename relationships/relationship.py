
import redis

from keys import key_list as default_key_list


class Relationship(object):

    def __init__(self, redis_connection=None, key_list=None, actor=None):

        if key_list:
            self.key_list = default_key_list.copy()
            self.key_list.update(key_list)
        else:
            self.key_list = default_key_list

        if redis_connection:
            self.redis_connection = redis_connection
        else:
            self.redis_connection = redis.StrictRedis(
                host='localhost',
                port=6379,
                db=0
            )

        self.actor = actor

    def __call__(self, *args, **kwargs):

        self.actor = args[0]

        return self

    def _action_call(self, command, from_id, to_id, operation_key):
        command_values = ':'.join(('user', str(from_id), operation_key)), to_id
        return getattr(self.redis_connection, command)(*command_values)

    def _list_call(self, operation_key):
        return self.redis_connection.smembers(
            'user:{}:{}'.format(self._get_actor(), operation_key)
        )

    def _count_call(self, operation_key):
        return self.redis_connection.scard(
            'user:{}:{}'.format(
                self._get_actor(),
                operation_key
            )
        )

    def _get_actor(self):
        if hasattr(self, 'actor'):
            return self.actor

        raise ValueError("actor is not defined")

    def block(self, to_id):

        self._action_call('sadd', self._get_actor(), to_id, self.key_list["blocked"])
        self._action_call('sadd', to_id, self._get_actor(), self.key_list["blocked_by"])

    def unblock(self, to_id):

        self._action_call('srem', self._get_actor(), to_id, self.key_list["blocked"])
        self._action_call('srem', to_id, self._get_actor(), self.key_list["blocked_by"])

    def follow(self, to_id):

        self._action_call('sadd', self._get_actor(), to_id, self.key_list["following"])
        self._action_call('sadd', to_id, self._get_actor(), self.key_list["followers"])

    def unfollow(self, to_id):

        self._action_call('srem', self._get_actor(), to_id, self.key_list["following"])
        self._action_call('srem', to_id, self._get_actor(), self.key_list["followers"])

    def friends(self):

        return self.redis_connection.sinter(
            "user:{}:{}".format(self._get_actor(), self.key_list["following"]),
            "user:{}:{}".format(self._get_actor(), self.key_list["followers"]),
        )

    def followers(self):
        return self._list_call(self.key_list["followers"])

    def following(self):
        return self._list_call(self.key_list["following"])

    def blocks(self):
        return self._list_call(self.key_list["blocked"])

    def blocked(self):
        return self._list_call(self.key_list["blocked_by"])

    def follower_count(self):
        return self._count_call(self.key_list["followers"])

    def following_count(self):
        return self._count_call(self.key_list["following"])

    def block_count(self):
        return self._count_call(self.key_list["blocked"])

    def blocked_count(self):
        return self._count_call(self.key_list["blocked_by"])

    def is_follower(self, follower_id):
        return self._action_call('sismember', self._get_actor(), follower_id, self.key_list["followers"])

    def is_following(self, following_id):
        return self._action_call('sismember', self._get_actor(), following_id, self.key_list["following"])

    def is_blocked(self, blocked_id):
        return self._action_call('sismember', self._get_actor(), blocked_id, self.key_list["blocked"])

    def is_blocked_by(self, blocked_by_id):
        return self._action_call('sismember',  self._get_actor(), blocked_by_id,self.key_list["blocked_by"])

    def get_network(self, output):

        user_id = self._get_actor()

        try:
            import pydot
        except ImportError:
            raise ImportError("You need pydot library to get network functionality.")

        graph = pydot.Dot('network_of_user_{}'.format(user_id), graph_type='digraph')
        target_node = pydot.Node(user_id)

        for _id in self(user_id).following():
            user_node = pydot.Node(_id)
            graph.add_edge(pydot.Edge(target_node, user_node))

        for _id in self(user_id).followers():
            user_node = pydot.Node(_id)
            graph.add_edge(pydot.Edge(user_node, target_node))

        graph.write_png(output)

