from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Obituary
from .forms import ObituaryForm

def submit_obituary(request):
    if request.method == 'POST':
        form = ObituaryForm(request.POST)
        if form.is_valid():
            obituary = form.save()
            messages.success(request, 'Obituary submitted successfully!')
            return redirect('view_obituaries')
    else:
        form = ObituaryForm()
    
    return render(request, 'obituaries/obituary_form.html', {'form': form})
