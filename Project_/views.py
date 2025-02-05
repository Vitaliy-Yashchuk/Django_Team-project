from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import DTP
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from weasyprint import HTML
import os

def add_protocol(request):
    if request.method == 'POST':
        title = request.POST.get('title')  
        description = request.POST.get('description')
        new_protocol = DTP(title=title, description=description)
        new_protocol.save()
        return redirect('home') 
    return render(request, 'add_protocol.html')

def add_photo_to_protocol(request, protocol_id):
    protocol = get_object_or_404(DTP, id=protocol_id)
    
    if request.method == 'POST' and request.FILES['photo']:
        photo = request.FILES['photo']  
        fs = FileSystemStorage()  
        filename = fs.save(photo.name, photo)  
        file_url = fs.url(filename) 
        
        protocol.photo = file_url 
        protocol.save()
        return redirect('protocol_detail', protocol_id=protocol.id)  
    return render(request, 'add_photo.html', {'protocol': protocol}) 

def generate_protocol_pdf(request, protocol_id):
    protocol = get_object_or_404(DTP, id=protocol_id)
    
    html_string = render_to_string('protocol_template.html', {'protocol': protocol})
    html = HTML(string=html_string)
    
    pdf = html.write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="protocol_{protocol_id}.pdf"'
    return response

def download_protocol_pdf(request, protocol_id):
    protocol = get_object_or_404(DTP, id=protocol_id)
    
    html_string = render_to_string('protocol_template.html', {'protocol': protocol})
    html = HTML(string=html_string)
    
    pdf = html.write_pdf()
    
    fs = FileSystemStorage()
    filename = f'protocol_{protocol_id}.pdf'
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    with open(file_path, 'wb') as f:
        f.write(pdf)
    
    file_url = fs.url(filename)
    return render(request, 'download_pdf.html', {'file_url': file_url})

def protocol_detail(request, protocol_id):
    try:
        protocol = DTP.objects.get(id=protocol_id)
    except ObjectDoesNotExist:
        return render(request, '404.html', {'message': 'Protocol not found!'})
    
    return render(request, 'protocol_detail.html', {'protocol': protocol})

def home(request):
    dtp_protocols = DTP.objects.all() 
    return render(request, 'index.html', {'dtp_protocols': dtp_protocols})

def create_protocol_page(request, protocol_id):
    protocol = get_object_or_404(DTP, id=protocol_id)
    
    return render(request, 'protocol_page.html', {'protocol': protocol})

def search_protocols(request):
    query = request.GET.get('q', '') 
    if query:
        protocols = DTP.objects.filter(title__icontains=query)  
    else:
        protocols = DTP.objects.all()  
    
    return render(request, 'search_results.html', {'protocols': protocols, 'query': query})

def delete_protocol(request, protocol_id):
    protocol = get_object_or_404(DTP, id=protocol_id)
    
    if request.method == 'POST':
        protocol.delete()  
        return redirect('home')  
    
    return render(request, 'confirm_delete.html', {'protocol': protocol})  

def update_protocol(request, protocol_id):
    protocol = get_object_or_404(DTP, id=protocol_id)
    
    if request.method == 'POST':
        protocol.title = request.POST.get('title')
        protocol.description = request.POST.get('description')
        protocol.save()
        return redirect('protocol_detail', protocol_id=protocol.id) 
    
    return render(request, 'update_protocol.html', {'protocol': protocol})  

