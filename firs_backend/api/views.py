from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Incident
from .serializers import IncidentSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'display': user.get_full_name() or user.username,
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.user.auth_token.delete()
    return Response({'message': 'Logged out'})

class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

    def get_queryset(self):
        return Incident.objects.all().order_by('created_at')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_import(request):
    records = request.data.get('records', [])
    created = []
    for rec in records:
        serializer = IncidentSerializer(data={
            'dt':      rec.get('dt', ''),
            'loc':     rec.get('loc', ''),
            'inv':     rec.get('inv', ''),
            'occ':     rec.get('occ', ''),
            'dmg_raw': rec.get('dmgRaw', 0),
            'alarm':   rec.get('alarm', ''),
            'sta':     rec.get('sta', ''),
            'eng':     rec.get('eng', ''),
            'by_user': rec.get('by', ''),
            'inj_c':   rec.get('injC', 0),
            'inj_b':   rec.get('injB', 0),
            'cas_c':   rec.get('casC', 0),
            'cas_b':   rec.get('casB', 0),
            'rem':     rec.get('rem', ''),
        })
        if serializer.is_valid():
            created.append(serializer.save())
    return Response({'imported': len(created)}, status=status.HTTP_201_CREATED)