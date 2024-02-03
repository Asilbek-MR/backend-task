
from rest_framework.permissions import IsAuthenticated
from .models import ProfileUser
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from .serializers import FootballFieldUserSerializer,FootballFieldSerializer,ProfileUserCreateSerializer,FootballFieldOwnerSerializer,FootballFieldBronSerializer
from .models import ProfileUser,FootballField
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes



@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = ProfileUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({
        'user_info': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        },
        'token': token.key
    },status=status.HTTP_200_OK)
          
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_view_field(request):
    user = request.user
    if user.is_authenticated:
        if user.role == 'admin':
            # Agar admin bo'lsa, hamma FootballField modellari haqida malumot olish
            fields = FootballField.objects.all()
            serializer = FootballFieldSerializer(fields, many=True)
            return Response(serializer.data, status=200)

        if user.role == 'field_owner':
            # Agar field_owner bo'lsa, faqat o'zining maydonlarini olish
            fields = FootballField.objects.filter(owner=user)
            serializer = FootballFieldSerializer(fields, many=True)
            return Response(serializer.data, status=200)

        if user.role == 'regular_user':
            # Agar regular_user bo'lsa, bron qilingan maydonlarni olish
            booked_fields = FootballField.objects.filter(bron=False)
            serializer = FootballFieldSerializer(booked_fields, many=True)
            return Response(serializer.data, status=200)
    return Response({'error': 'not authenticated'}, status=200)



@api_view(['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_for_admin(request):
    user = request.user
    if user.is_authenticated:
        if user.role == 'admin':
            # Agar admin bo'lsa, hamma FootballField modellari haqida malumot olish
            fields = FootballField.objects.all()
            serializer = FootballFieldSerializer(fields, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({'error': 'You not admin'}, status=200)



@api_view(['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_for_stadum_owner(request):
    user = request.user
    if user.is_authenticated:
        if user.role == 'field_owner':
            # Agar field_owner bo'lsa, faqat o'zining maydonlarini olish
            fields = FootballField.objects.filter(owner=user)
            serializer = FootballFieldOwnerSerializer(fields, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({'error': 'You not owner'}, status=200)
        
from rest_framework import status

@api_view(['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_for_stadum_owner_create(request):
    user = request.user

    if user.is_authenticated:
        if user.role == 'field_owner':
            if request.method == 'GET':
                # Agar GET so'rovi kelsa, faqat o'zining maydonlarini olish
                fields = FootballField.objects.filter(owner=user)
                serializer = FootballFieldOwnerSerializer(fields, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif request.method == 'POST':
                # Agar POST so'rovi kelsa, yangi maydon yaratish
                serializer = FootballFieldOwnerSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(owner=user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return Response({'error': 'You are not the owner'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'error': 'You are not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
@api_view(['GET', 'POST', 'PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_for_stadum_brone(request, pk=None):
    user = request.user

    if user.is_authenticated:
        if user.role == 'regular_user':
            if request.method == 'GET':
                # Agar GET so'rovi kelsa, faqat o'zining maydonlarini olish
                fields = FootballField.objects.filter(bron=False)
                serializer = FootballFieldSerializer(fields, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif request.method == 'PUT' and pk is not None:
                print("Request")
                # Agar PUT so'rovi kelsa, ma'lum bir maydonni yangilash
                try:
                    field = FootballField.objects.get(id=pk)
                    serializer = FootballFieldBronSerializer(field, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except FootballField.DoesNotExist:
                    return Response({'error': 'Field not found or you are not the owner'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return Response({'error': 'You are not the owner'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'error': 'You are not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
  
        
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_for_stadium_owner_update(request, pk):
    user = request.user
    if user.is_authenticated:
        try:
            # Faqat o'zining maydonlarini olish
            field = FootballField.objects.get(id=pk, owner=user)
            if request.method == 'GET':
                serializer = FootballFieldOwnerSerializer(field)
                return Response(serializer.data, status=200)
            elif request.method in ['PUT', 'PATCH']:
                serializer = FootballFieldOwnerSerializer(field, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=200)
                return Response(serializer.errors, status=400)
            elif request.method == 'DELETE' and field:
                field.delete()
            return Response({'message': 'Field deleted successfully'}, status=200)

        except FootballField.DoesNotExist:
            return Response({'error': 'Field not found or you are not the owner'}, status=404)
    else:
        return Response({'error': 'You are not authenticated'}, status=401)


        



from datetime import datetime
from django.utils import timezone

@api_view(['GET', 'POST', 'PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_for_stadum_brone_filter(request, pk=None):
    user = request.user

    if user.is_authenticated:
        if user.role == 'regular_user':
            if request.method == 'GET':
                # Agar GET so'rovi kelsa, faqat o'zining maydonlarini olish
                date_param = request.query_params.get('date', None)
                if date_param:
                    # Agar "date" qiymati kiritilgan bo'lsa, uni o'zgartirish uchun ishlatamiz
                    try:
                        date = datetime.strptime(date_param, '%Y-%m-%d').date()
                        fields = FootballField.objects.filter(bron=False, date=date)
                    except ValueError:
                        return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # "date" qiymati kiritilmagan bo'lsa, umumiy ma'lumotlarni olib kelamiz
                    fields = FootballField.objects.filter(bron=False)

                serializer = FootballFieldSerializer(fields, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            elif request.method == 'PUT' and pk is not None:
                # Agar PUT so'rovi kelsa, ma'lum bir maydonni yangilash
                try:
                    field = FootballField.objects.get(id=pk)
                    serializer = FootballFieldBronSerializer(field, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except FootballField.DoesNotExist:
                    return Response({'error': 'Field not found or you are not the owner'}, status=status.HTTP_404_NOT_FOUND)

            else:
                return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return Response({'error': 'You are not the owner'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'error': 'You are not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
