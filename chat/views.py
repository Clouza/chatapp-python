from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Message

# realtime deps
from django.http import JsonResponse
from django.utils.timezone import now
from django.core.serializers import serialize

@login_required
def home(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/home.html', {'users': users})

@login_required
def chat_view(request, user_id):
    other_user = User.objects.get(id=user_id)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    if request.method == 'POST':
        msg_text = request.POST.get('message', '')
        uploaded_file = request.FILES.get('file')

        Message.objects.create(
            sender=request.user,
            receiver=other_user,
            content=msg_text,
            file=uploaded_file
        )
        return redirect('chat', user_id=other_user.id)

    return render(request, 'chat/chat.html', {
        'messages': messages,
        'other_user': other_user
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'chat/register.html', {'form': form})

# fungsi realtime
@login_required
def fetch_messages(request, user_id):
    other_user = User.objects.get(id=user_id)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    data = []
    for m in messages:
        message_data = {
            'sender': m.sender.username,
            'content': m.content,
            'timestamp': m.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        }

        if m.file:
            message_data['file_url'] = m.file.url
            message_data['file_name'] = m.file.name.split('/')[-1] 

        data.append(message_data)

    return JsonResponse({'messages': data})