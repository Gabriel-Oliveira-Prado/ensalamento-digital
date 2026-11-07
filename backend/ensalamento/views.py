from rest_framework.decorators import api_view
from rest_framework.response import Response

# Teste de status da API
@api_view(["GET"])
def api_status(request):
    return Response({"status": "ok"})