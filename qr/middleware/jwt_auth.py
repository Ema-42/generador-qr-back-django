from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.contrib.auth.models import User
from qr.utils import decode_jwt_token
import json

def _parse_register_flag(request):
    try:
        if request.method in ('POST', 'PUT', 'PATCH'):
            ct = request.META.get('CONTENT_TYPE', '')
            if ct.startswith('application/json'):
                body = request.body
                if body:
                    data = json.loads(body.decode('utf-8'))
                    v = data.get('register_as_official', None)
                    if isinstance(v, bool):
                        return v
                    if isinstance(v, str):
                        lv = v.strip().lower()
                        if lv in ('true', '1', 'yes', 'y'):
                            return True
                        if lv in ('false', '0', 'no', 'n'):
                            return False
                    if isinstance(v, int):
                        return v != 0
            else:
                v = request.POST.get('register_as_official')
                if v is not None:
                    lv = str(v).strip().lower()
                    if lv in ('true', '1', 'yes', 'y'):
                        return True
                    if lv in ('false', '0', 'no', 'n'):
                        return False
    except Exception:
        pass
    return None

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        public_paths = ['/api/login/', '/api/register/']
        
        if any(request.path.startswith(path) for path in public_paths):
            return None
        
        register_flag = _parse_register_flag(request)
        if register_flag is False:
            return None
        
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
        
        try:
            request.user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Usuario no encontrado'
            }, status=401)
        
        return None
