from rest_framework.response import Response

MESSAGE_KEY = 'message'

class ResponseBuilder:
    def get_response(self, message, status):
        return Response(data={MESSAGE_KEY: message}, status=status)
