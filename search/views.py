import json
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import View
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
 
from main.models import TicketForProf
 

class ESearchView(View):
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:
            if not request.user.is_staff:
                raise Http404
        else:
            raise Http404
        question = request.GET.get('q')
        if question is not None:
            search_TicketForProfs = TicketForProf.objects.filter(id_for_use__icontains=question, can_use=True)
            context['last_question'] = '?q=%s' % question
 
            current_page = Paginator(search_TicketForProfs, 10)
 
            page = request.GET.get('page')
            try:
                context['ticket_lists'] = current_page.page(page)
            except PageNotAnInteger:
                context['ticket_lists'] = current_page.page(1)
            except EmptyPage:
                context['ticket_lists'] = current_page.page(current_page.num_pages)
 
        return render(request=request, template_name='index.html', context=context)


class DeleteObject(LoginRequiredMixin, DeleteView):
    model = TicketForProf
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_staff:
                raise Http404
        else:
            raise Http404
        ticket_id = request.GET.get('ticket_id')
        obj = get_object_or_404(TicketForProf, id_for_use=ticket_id)
        # Check for uncompleted tasks
        uncompleted = TicketForProf.objects.filter(id_for_use=ticket_id).count()
        if uncompleted != 0:
            if obj.can_use:
                obj.delete()
        return redirect('search:index')

