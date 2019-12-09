import nltk

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

nltk.download('gutenberg')


class FirstApi(APIView):
    """
    A view that returns the count of active users in JSON.
    """
    renderer_classes = [JSONRenderer]

    def get(self, request):
        data = request.data
        content = {'your_data': data}
        return Response(content)
