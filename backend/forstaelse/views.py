from rest_framework import status, permissions
from .serializers import ForstaelseSerializer
from .models import Forstaelse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist


class ForstaelseView(APIView):
    permission_classes = []

    def get(self, request, pk):
        try:
            getForstaelse = Forstaelse.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        serializer = ForstaelseSerializer(getForstaelse)
        return JsonResponse(serializer.data, safe=False)


class ProtectedForstaelseView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = ForstaelseSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def put(self, request, pk):
        try:
            getForstaelse = Forstaelse.objects.filter(
                owner=self.request.user).get(pk=pk)
        except ObjectDoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        data = JSONParser().parse(request)
        serializer = ForstaelseSerializer(getForstaelse, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            getForstaelse = Forstaelse.objects.filter(
                owner=self.request.user).get(pk=pk)
        except ObjectDoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        getForstaelse.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
