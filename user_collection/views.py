from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from user_collection.manager import UserManagement, CollectionManagement
from user_collection.models import Collection, Movie
from user_collection.serializers import UserSerializer
from rest_framework import status


class RegisterUser(APIView):
    @staticmethod
    def post(request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access_token': str(refresh.access_token)
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"result": "failure", "message": str(e)}, 500)


class FetchAllMovies(APIView):
    @staticmethod
    def get(request):
        try:
            data = UserManagement.get_movies_list()
            return Response({"result": "success", "data": data}, 200)
        except Exception as e:
            return Response({"result": "failure", "message": str(e)}, 500)


class UserCollection(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            response_data = UserManagement.get_user_collection(request)
            return Response(response_data, 200)
        except Exception as e:
            return Response({"result": "failure", "message": str(e)}, 500)

    @staticmethod
    def post(request):
        try:
            data = request.data
            get_movies = CollectionManagement.add_new_collection(request, data)
            return Response({"collection_uuid": get_movies}, 200)
        except ValidationError as ve:
            return Response({"result": "failure", "message": ve.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"result": "failure", "message": str(e)}, 500)


class CollectionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, *args, **kwargs):
        try:
            collection_uuid = kwargs.get('collection_uuid')
            user_id = request.user.id
            response_data = CollectionManagement.get_collection_data_for_a_user(collection_uuid, user_id)
            return Response({"is_success": True, "data": response_data}, status=status.HTTP_200_OK)
        except Collection.DoesNotExist:
            return Response({"result": "failure", "message": "Collection not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"result": "failure", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def put(request, *args, **kwargs):
        try:
            collection_uuid = kwargs.get('collection_uuid')
            user_id = request.user.id

            response_data = CollectionManagement.update_collection_data_for_a_user(request, collection_uuid, user_id)
            return Response({"is_success": True, "data": response_data}, status=status.HTTP_200_OK)

        except Collection.DoesNotExist:
            return Response({"result": "failure", "message": "Collection not found."}, status=status.HTTP_404_NOT_FOUND)
        except Movie.DoesNotExist:
            return Response({"result": "failure", "message": "One or more movies not found."},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"result": "failure", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def delete(request, *args, **kwargs):
        try:
            CollectionManagement.delete_collection(request, kwargs)
            return Response({"is_success": True, "message": "Collection deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Collection.DoesNotExist:
            return Response({"result": "failure", "message": "Collection not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"result": "failure", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RequestCountView(APIView):
    @staticmethod
    def get(request):
        count = cache.get('counter', 0)
        return Response({'requests': count})


class ResetRequestCountView(APIView):

    @staticmethod
    def post(request):
        cache.set('counter', 0)
        return Response({'message': 'Request count reset successfully'})