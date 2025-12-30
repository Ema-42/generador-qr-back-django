from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.contrib.auth.models import User
from qr.utils import decode_jwt_token

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Rutas públicas que no requieren autenticación
        public_paths = ['/api/login/', '/api/register/']
        
        if any(request.path.startswith(path) for path in public_paths):
            return None
        
        # Obtener token del header Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Bearer '):
            return JsonResponse({
                'status': 'error',
                'message': 'Token no proporcionado'
            }, status=401)
        
        token = auth_header.split(' ')[1]
        payload = decode_jwt_token(token)
        
        if not payload:
            return JsonResponse({
                'status': 'error',
                'message': 'Token inválido o expirado'
            }, status=401)
        
        # Agregar usuario al request
        try:
            request.user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Usuario no encontrado'
            }, status=401)
         
        return None
