from django.core.paginator import Paginator

def view_obituaries(request):
    obituaries_list = Obituary.objects.all().order_by('-submission_date')
    paginator = Paginator(obituaries_list, 10)  # Show 10 obituaries per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'obituaries/view_obituaries.html', {'page_obj': page_obj})
