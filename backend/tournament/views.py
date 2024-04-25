from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import TournamentSerializer
import traceback
import logging
logger = logging.getLogger('django')


class FillTournamentView(generics.CreateAPIView):
	serializer_class = TournamentSerializer
	# permission_classes = [permissions.IsAuthenticated]
	permission_classes = [permissions.AllowAny]

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)

		try:
			if serializer.is_valid():
				serializer.save()
				return Response({
					"name": request.data['name'],
					"size": request.data['size'],
					"active_player": request.data['active_player']
				}, status=status.HTTP_201_CREATED)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			logger.debug(f"An exception of type {type(e).__name__} occurred (in tournament.views)")
			traceback.print_exc()
			return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)