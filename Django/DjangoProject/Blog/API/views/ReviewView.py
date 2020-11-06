from rest_framework.views import APIView
from rest_framework.response import Response

from Blog.API.serializer.ReviewSerializer import ReviewCreateSerializer

class ReviewCreateView(APIView):
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)
