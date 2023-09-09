from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Family_Member
from .forms import MemberForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    """Site's index page"""
    return render(request, 'trees/index.html')

@login_required
def create_member(request):
    """Creates a new family member"""
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('trees:create_member'))
    else:
        form = MemberForm()
    context = {'form': form}
    return render(request, 'trees/create_member.html', context)

@login_required
def search_member(request):
    """Searches for a member"""
    query = request.GET.get('query', '') #Default to an empty string if query is None
    if query:
        results = Family_Member.objects.filter(first_name__icontains=query) | Family_Member.objects.filter(last_name__icontains=query)
    else:
        results = []
    context = {'results': results}
    return render(request, 'trees/search_member.html', context)
