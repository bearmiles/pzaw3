from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import Profile, Case, UserInventory, Skin
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from django.middleware.csrf import get_token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from .selializer import SkinSerializer
import random

@api_view(['POST'])
def simple_api(request):

    try:
        data = request.data
        fnm = data.get('fnm', '')
        pwd = data.get('pwd', '')

        if not fnm or not pwd:
            return Response({'error': 'Username and password are required'}, status=400)

        if User.objects.filter(username=fnm).exists():
            return Response({'error': 'Username already exists'}, status=400)

        my_user = User.objects.create_user(username=fnm, password=pwd)
        user_model = User.objects.get(username=fnm)
        new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)

        return Response({
            'success': True,
            'message': 'User created successfully',
            'user_id': user_model.id
        }, status=201)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([])  # Login bez potrzeby bycia zalogowanym
@authentication_classes([])  # Token auth też niepotrzebny przy logowaniu
def loginn(request):
    try:
        data = request.data
        fnm = data.get('fnm', '')
        pwd = data.get('pwd', '')

        if not fnm or not pwd:
            return Response({'error': 'Username and Password are required'}, status=400)

        if not User.objects.filter(username=fnm).exists():
            return Response({"error": 'You need to register first'}, status=400)

        userr = authenticate(request, username=fnm, password=pwd)

        if userr is not None:
            # NIE używamy login() tutaj
            token, _ = Token.objects.get_or_create(user=userr)
            return Response({
                'token': token.key,
                'user_id': userr.id,
                'username': userr.username
            }, status=200)
        else:
            return Response({"error": "Invalid credentials"}, status=400)
    except Exception as ex:
        return Response({"error": str(ex)}, status=500)
    

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_login(request):
    return Response({
        "username": request.user.username,
        "user_id": request.user.id
    }, status=200)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logoutt(request):
    try:
        request.user.auth_token.delete()
        return Response({'success': True, "message":"logged out succ"})
    except Exception as ex:
        return Response({'success':False, "message":'logging out has occured erros'})

def open_case(user, case_id):
    case = get_object_or_404(Case, id=case_id)
    skins = Skin.objects.filter(case=case)  # Użyj filter zamiast get

    if not skins.exists():
        return None
    
    chosen_skin = random.choice(list(skins))  # Konwersja QuerySet na listę

    user_inventory = UserInventory.objects.create(user=user, skin=chosen_skin)
    return user_inventory

def get_all_skins(user, case_id):
    case = get_object_or_404(Case, id=case_id)
    skins = Skin.objects.filter(case=case)

    if not skins.exists():
        return None
    
    return skins

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def open_case_api(request, case_id):
    try:
        user = request.user
        user_inventory = open_case(user, case_id)
        
        if user_inventory is None:
            return Response({'error': 'No skins available in this case'}, status=400)
            
        return Response({
            'success': True,
            'skin_name': user_inventory.skin.skin_name,
            'rarity': user_inventory.skin.rarity,
            'skin_src': user_inventory.skin.skin_src,
            'obtained_at': user_inventory.obtained_at
        })
    except Case.DoesNotExist:
        return Response({'error': 'Case not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_inventory(request):
    try:
        user = request.user
        user_skins = UserInventory.objects.filter(user=user)
        data = [{
            'skin_name' : item.skin.skin_name,
            'rarity' : item.skin.rarity
        } for item in user_skins]
        return Response(data)
    except Exception as ex:
        return Response({"bład": str(ex)})
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_skins_api(request, case_id):
    try:
        case = get_object_or_404(Case, id=case_id)
        skins = Skin.objects.filter(case=case)

        if not skins.exists():
            return Response({"error": "No skins found for this case."}, status=404)

        serialized = SkinSerializer(skins, many=True)
        return Response(serialized.data, status=200)

    except Exception as ex:
        return Response({"error": str(ex)}, status=500)