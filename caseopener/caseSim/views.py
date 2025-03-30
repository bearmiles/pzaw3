from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate, login

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
                'user_id': userr.id
            }, status=200)
        else:
            return Response({"error":"Invalid creadentials"}, status=400)
    except Exception as ex:
        return Response({"error": str(ex)}, status=500) 