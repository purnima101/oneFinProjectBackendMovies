# collections/factories.py
import factory
from django.contrib.auth.models import User
from .models import Movie, Collection, CollectionMap
import uuid


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user_{n}')
    password = factory.PostGenerationMethodCall('set_password', 'password123')


class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movie

    uuid = factory.LazyFunction(uuid.uuid4)
    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('paragraph')
    genres = factory.Faker('word')


class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    uuid = factory.LazyFunction(uuid.uuid4)
    user = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('paragraph')


class CollectionMapFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CollectionMap

    collection_key = factory.SubFactory(CollectionFactory)
    movie_key = factory.SubFactory(MovieFactory)
