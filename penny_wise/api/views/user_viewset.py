from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import RegisterSerializer, LoginSerializer
from ..models import User
from drf_spectacular.utils import extend_schema, OpenApiResponse







def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@extend_schema(
    tags=['Authentication'],
    request=RegisterSerializer,
    responses={201: OpenApiResponse(description='User registered successfully')}
)
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({
            'detail': 'User registered successfully',
            'tokens': tokens
        }, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=['Authentication'],
    request=LoginSerializer,
    responses={200: OpenApiResponse(description='User logged in successfully with JWT tokens')}
)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({'detail': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        tokens = get_tokens_for_user(user)
        return Response({
            'detail': 'User logged in successfully',
            'tokens': tokens
        })
