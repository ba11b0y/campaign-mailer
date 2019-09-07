import redis
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        r = redis.StrictRedis(host='localhost', port=6379)
        p = r.pubsub()
        p.psubscribe('tasks')
        while True:
            for message in p.listen():
                if message:
                    print(message)
