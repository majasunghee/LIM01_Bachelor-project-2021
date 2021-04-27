from rest_framework import status, permissions
from .serializers import SetsSerializer, GetSetsSerializer, SavedSerializer, CommentSerializer, RatingSerializer, CompletedSerializer, GetSavedSerializer, GetCompletedSerializer
from .models import Sets, Saved, Comment, Rating, Completed
from accounts.models import UserAccount
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response

"""
Set view without permission class meaning it is accessible to anyone. 
Only allows get requests.
"""


class SetsView(APIView):
    permission_classes = []
    # receives a primary key in the url and returns the chat object with the corresponding key or 404 error.

    def get(self, request, pk):
        try:
            getSet = Sets.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        serializer = SetsSerializer(getSet)
        return JsonResponse(serializer.data, safe=False)


"""
Protected set view which means requests need to include a valid token. 
allows post, put and delete requests.
"""


class ProtectedSetsView(APIView):
    # adds new set object to the database model based on request body if it can be serialized correctly.
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = SetsSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    # updates an existing set object if it exists and it can be serialized
    def put(self, request, pk):
        try:
            getSets = Sets.objects.filter(owner=self.request.user).get(pk=pk)
        except ObjectDoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        data = JSONParser().parse(request)
        serializer = SetsSerializer(getSets, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    # deletes an existing set object if it exists, else 404 error is returned
    def delete(self, request, pk):
        try:
            getSets = Sets.objects.filter(owner=self.request.user).get(pk=pk)
        except ObjectDoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        getSets.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


# protected get view which returns a list of all the sets the user has made.

class UserSetsView(APIView):
    def get(self, request):
        getSet = Sets.objects.filter(owner=self.request.user)
        serializer = GetSetsSerializer(getSet, many=True)
        return JsonResponse(serializer.data, safe=False)


# protected view for getting, posting and deleting saved sets.

class SavedView(APIView):
    def get(self, request):
        getSaved = Saved.objects.filter(owner=self.request.user)
        serializer = GetSavedSerializer(getSaved, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = SavedSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            getSaved = Saved.objects.filter(
                owner=self.request.user).get(sets=pk)
        except ObjectDoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        getSaved.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

# protected view for checking whether user has saved set with given primary key.


class UserSavedView(APIView):
    def get(self, request, pk):
        try:
            getSaved = Saved.objects.filter(
                owner=self.request.user).get(sets=pk)
        except ObjectDoesNotExist:
            content = {'saved': False}
            return Response(content)
        content = {'saved': True}
        return Response(content)

# view accessible for anyone. returns a list of all comments related to a given set.


class CommentView(APIView):
    permission_classes = []

    def get(self, request, pk):
        getComment = Comment.objects.filter(sets=pk)
        serializer = CommentSerializer(getComment, many=True)
        return JsonResponse(serializer.data, safe=False)

# protected view for getting, posting and deleting comments for a given set.


class UserCommentView(APIView):
    def get(self, request, pk):
        try:
            getComment = Comment.objects.filter(
                owner=self.request.user).get(sets=pk)
        except ObjectDoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(getComment, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            getComment = Comment.objects.filter(
                owner=self.request.user).get(pk=pk)
        except ObjectDoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        getComment.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

# view accessible to all for getting total rating for a given set.


class getRatingView(APIView):
    permission_classes = []

    def get(self, request, pk):
        getRatings = Rating.objects.filter(sets=pk)
        ratingCount = getRatings.count()
        upvotes = getRatings.filter(rating=True).count()
        downvotes = getRatings.filter(rating=False).count()
        # json object with data about rating based on django aggregation functions.
        content = {'ratings': ratingCount,
                   'upvotes': upvotes, 'downvotes': downvotes}
        return Response(content)

# protected view for CRUD requests for modifying ratings for a set.


class RatingView(APIView):
    # get request to check whether user has rated the set or not
    def get(self, request, pk):
        try:
            getRating = Rating.objects.filter(
                owner=self.request.user).get(sets=pk)
        except ObjectDoesNotExist:
            content = {'rating': None}
            return Response(content)
        content = {'rating': getRating.rating}
        return Response(content)

    def post(self, request):
        """
        adds, changes or deletes user rating for a set.

        If a user has not rated this set, the post request will make a new rating.
        If a user has rated the set before and a new rating is sent it will either
        be deleted or changed.
        """
        data = JSONParser().parse(request)
        setId = data["sets"]
        rating = data["rating"]
        try:
            getRating = Rating.objects.filter(
                owner=self.request.user).get(sets=setId)
        except ObjectDoesNotExist:
            serializer = RatingSerializer(data=data)
            if serializer.is_valid():
                serializer.save(owner=self.request.user)
                return JsonResponse(serializer.data, status=201)
        if (getRating.rating == rating):
            getRating.delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = RatingSerializer(getRating, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

# protected view for posting, getting and updating completed view.


class CompletedView(APIView):
    # get request which returns whether a set has been completed and the score.
    def get(self, request, pk):
        try:
            getCompleted = Completed.objects.filter(
                owner=self.request.user).get(sets=pk)
        except ObjectDoesNotExist:
            content = {'completed': False, 'score': '0'}
            return Response(content)
        content = {'completed': True,
                   'score': getCompleted.score, 'id': getCompleted.id}
        return Response(content)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = CompletedSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def put(self, request, pk):
        try:
            getCompleted = Completed.objects.filter(
                owner=self.request.user).get(pk=pk)
        except ObjectDoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        data = JSONParser().parse(request)
        serializer = CompletedSerializer(getCompleted, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

# protected view which returns a list of the users completed sets.


class UserCompletedView(APIView):
    def get(self, request):
        getCompleted = Completed.objects.filter(owner=self.request.user)
        serializer = GetCompletedSerializer(getCompleted, many=True)
        return JsonResponse(serializer.data, safe=False)
