from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import ChatRoom, Chat
from .forms import SignInForm
from django.contrib.auth import authenticate, login, get_user_model

User = get_user_model()

class Index(View): 
    def get(self, request): 
        if request.user.is_authenticated: 
            return redirect('chat_home') 
        else:
            form = SignInForm() 
            return render(request, 'chat/sign_in.html', {'form': form}) 
            
    def post(self, request):
        form = SignInForm(request.POST) 
        if form.is_valid():
            email = form.cleaned_data['email'] 
            password = form.cleaned_data['password'] 
            user = authenticate(request, email=email, password=password) 
            if user is not None:
                login(request, user) 
                return redirect('chat_home') 
            else: 
                form.add_error(None, 'Invalid email or password') 
                return render(request, 'chat/sign_in.html', {'form': form})

class ChatHome(View):
    def get(self, request):
        rooms = ChatRoom.objects.filter(participants=request.user)
        return render(request, 'chat/home.html', {'rooms': rooms})

    def post(self, request):
        action = request.POST.get("action")
        if action == "create":
            room_name = request.POST.get("room_name")
            if room_name:
                room = ChatRoom.objects.create(name=room_name, creator=request.user)
                room.participants.add(request.user)
                return redirect('room', room_name=room.name)
        elif action == "select":
            room_name = request.POST.get("room_name")
            room = get_object_or_404(ChatRoom, name=room_name, participants=request.user)
            return redirect('room', room_name=room.name)
        return redirect('chat_home')

class Room(View):
    def get(self, request, room_name):
        room = ChatRoom.objects.filter(name=room_name).first()
        chats = []

        if room:
            chats = Chat.objects.filter(room=room)
        else:
            room = ChatRoom(name=room_name)
            room.save()
        return render(request, 'chat/room.html', {'room_name': room_name, 'chats': chats, 'user_id': request.user.id})
