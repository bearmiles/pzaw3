from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token

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
def loginn(request):
    try:
        data = request.data
        fnm = data.get('fnm', '')
        pwd = data.get('pwd', '')
        nick = data.get('nick', '')

        if not fnm or not pwd:
            return Response({'error': 'Username and Password are required'}, status=400)

        if not User.objects.filter(username=fnm).exists():
            return Response({"error": 'You need to register first'}, status=400)

        userr = authenticate(request, username = fnm, password = pwd)

        if userr is not None:
            login(request, userr)
            return Response({
                'success': True,
                'message': 'Login successful',
                'user_id': userr.id,
                'nick' : nick
            }, status=200)
        else:
            return Response({"error":"Invalid creadentials"}, status=400)
    except Exception as ex:
        return Response({"error": str(ex)}, status=500)

# views.py
@api_view(['GET'])
def check_login(request):
    if request.user.is_authenticated:
        return Response({
            "username": request.user.nick,
            "email": request.user.username,
            "user_id": request.user.id
        })
    return Response({"error": "Not authenticated"}, status=401)

@api_view(['GET'])
def logoutt(request):
    if request.user.is_authenticated:
        logout(request)
        return Response({ "success": True, "message": "wylogowywanie git"})
    else:
        return Response({"success": False, "message": "wylogowywanie nie git"})
    return Response({"success": True})
