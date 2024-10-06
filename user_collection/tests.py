from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user_collection.factories import UserFactory, CollectionFactory, MovieFactory  # Make sure to create a MovieFactory
from user_collection.models import Collection


class RegisterUserTests(APITestCase):

    def test_register_user(self):
        url = reverse('register_user')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.data)


class FetchAllMoviesTests(APITestCase):

    def test_fetch_all_movies(self):
        url = reverse('fetch-all-movies')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('result', response.data)
        self.assertEqual(response.data['result'], 'success')


class UserCollectionTests(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_get_user_collection(self):
        url = reverse('user_collection')
        CollectionFactory.create(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)

    def test_post_new_collection(self):
        url = reverse('user_collection')
        data = {
            "title": "My Farrv3",
            "description": "<Description of the collection>",
            "movies": [
                {
                    "title": "Queerama",
                    "description": "50 years after decriminalisation of homosexuality in the UK, director Daisy Asquith mines the jewels of the BFI archive to take us into the relationships, desires, fears and expressions of gay men and women in the 20th century.",
                    "genres": "",
                    "uuid": "57baf4f4-c9ef-4197-9e4f-acf04eae5b4d"
                },
                {
                    "title": "Satana likuyushchiy",
                    "description": "In a small town live two brothers, one a minister and the other one a hunchback painter of the chapel who lives with his wife. One dreadful and stormy night, a stranger knocks at the door asking for shelter. The stranger talks about all the good things of the earthly life the minister is missing because of his puritanical faith. The minister comes to accept the stranger's viewpoint but it is others who will pay the consequences because the minister will discover the human pleasures thanks to, ehem, his sister- in -law… The tormented minister and his cuckolded brother will die in a strange accident in the chapel and later an infant will be born from the minister's adulterous relationship.",
                    "genres": "",
                    "uuid": "163ce013-03e2-47e9-8afd-e7de7688c151"
                },
                {
                    "title": "Betrayal",
                    "description": "When one of her hits goes wrong, a professional assassin ends up with a suitcase full of a million dollars belonging to a mob boss ...",
                    "genres": "Action,Drama,Thriller",
                    "uuid": "720e8796-5397-4e81-9bd7-763789463707"
                },
                {
                    "title": "Siglo ng Pagluluwal",
                    "description": "An artist struggles to finish his work while a storyline about a cult plays in his head.",
                    "genres": "Drama",
                    "uuid": "e9548ee7-6a95-4917-893e-1fa1d3a6de40"
                },
                {
                    "title": "رگ خواب",
                    "description": "Rising and falling between a man and woman.",
                    "genres": "Drama,Family",
                    "uuid": "9b0a4aa2-9ec7-4a3d-98ab-622275f44ea5"
                },
                {
                    "title": "Robin Hood",
                    "description": "Yet another version of the classic epic, with enough variation to make it interesting. The story is the same, but some of the characters are quite different from the usual, in particular Uma Thurman's very special maid Marian. The photography is also great, giving the story a somewhat darker tone.",
                    "genres": "Drama,Action,Romance",
                    "uuid": "73399935-2165-41f0-a6a4-1336ef5e5c20"
                },
                {
                    "title": "Caged Heat 3000",
                    "description": "It's the year 3000 AD. The world's most dangerous women are banished to a remote asteroid 45 million light years from earth. Kira Murphy doesn't belong; wrongfully accused of a crime she did not commit, she's thrown in this interplanetary prison and left to her own defenses. But Kira's a fighter, and soon she finds herself in the middle of a female gang war; where everyone wants a piece of the action... and a piece of her! \"Caged Heat 3000\" takes the Women-in-Prison genre to a whole new level... and a whole new galaxy!",
                    "genres": "Science Fiction",
                    "uuid": "129cf5d9-827c-4e42-843e-1f87ef99452f"
                },
                {
                    "title": "The Burkittsville 7",
                    "description": "A film archivist revisits the story of Rustin Parr, a hermit thought to have murdered seven children while under the possession of the Blair Witch.",
                    "genres": "Horror",
                    "uuid": "5e904ce8-91b7-42b4-84d9-5b53f4cb8c74"
                },
                {
                    "title": "Shadow of the Blair Witch",
                    "description": "In this true-crime documentary, we delve into the murder spree that was the inspiration for Joe Berlinger's \"Book of Shadows: Blair Witch 2\".",
                    "genres": "Mystery,Horror",
                    "uuid": "bcacfa33-a886-4ecb-a62a-6bbcb9d9509d"
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('collection_uuid', response.data)


#
class CollectionDetailViewTests(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.collection = CollectionFactory(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_get_collection_detail(self):
        url = reverse('collection-detail', args=[self.collection.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)

    def test_update_collection(self):
        url = reverse('collection-detail', args=[self.collection.uuid])
        data = {
            'title': 'Updated Collection',
            'description': 'Updated description.'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)

    def test_delete_collection(self):
        url = reverse('collection-detail', args=[self.collection.uuid])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
