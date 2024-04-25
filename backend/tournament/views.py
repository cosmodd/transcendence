from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import TournamentSerializer

class CreateTournamentView(generics.CreateAPIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, *args, **kwargs):
		serializer = TournamentSerializer(data=request.data)

		try:
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)