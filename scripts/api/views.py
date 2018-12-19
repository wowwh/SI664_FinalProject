from googleapp.models import App, AppGenre
from api.serializers import AppSerializer
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response


class AppViewSet(viewsets.ModelViewSet):
	"""
	This ViewSet provides both 'list' and 'detail' views.
	"""
	queryset = App.objects.order_by('app_name')
	serializer_class = AppSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def delete(self, request, pk, format=None):
		app = self.get_object(pk)
		self.perform_destroy(self, app)

		return Response(status=status.HTTP_204_NO_CONTENT)

	def perform_destroy(self, instance):
		instance.delete()

