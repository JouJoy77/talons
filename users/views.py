# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import User

from users.models import Profile
from main.models import TicketForProf
from .forms import UserRegisterForm
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if not request.user.is_staff:    
        prof = Profile.objects.order_by('id')
        user_id = request.user.pk
        ticks = TicketForProf.objects.filter(user_id=user_id).all().values()
        context = {
            'Name': 'Профиль',
            'profiles': prof,
            'tickets': ticks
        }
        return render(request, 'users/profile.html', context)
    else:
        return redirect('search:index')


class ConfirmUseTicket(LoginRequiredMixin, DeleteView):
    model = TicketForProf
 
    def post(self, request, *args, **kwargs):
        ticket_id = request.GET.get('ticket_id')
        obj = get_object_or_404(TicketForProf, id_for_use=ticket_id)
        # Check for uncompleted tasks
        uncompleted = TicketForProf.objects.filter(id_for_use=ticket_id).count()
        if uncompleted != 0:
            obj.can_use=True
            obj.save()
        obj = get_object_or_404(TicketForProf, id_for_use=ticket_id)
        return redirect('profile')