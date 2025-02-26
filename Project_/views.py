from io import BytesIO
import os
from django.http import HttpResponse # type: ignore
from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.urls import reverse # type: ignore
import logging
from DTP_project_first import settings
from Project_.models import DTP
from .forms import DTPForm 
from .models import DTP
from reportlab.pdfgen import canvas
from django.core.files.base import ContentFile
import base64
from django.contrib import messages

def home(request):
    print("Функція home викликається!")
    dtp = DTP.objects.all()
    return render(request, 'index.html', {'dtp': dtp})


def navbar(request):
     return render(request, 'NavBar.html',)


def get_protocol(request):
    return render(request, 'success.html',)
    
def create(request):
    if request.method == "POST":
        form = DTPForm(request.POST, request.FILES)
        if form.is_valid():
            dtp_instance = form.save(commit=False)
            dtp_instance.save()

            if 'image' in request.FILES:
                dtp_instance.image = request.FILES['image']
                dtp_instance.save()

            messages.success(request, "✅ Євро-протокол успішно створений!")  
            return render(request, 'create.html', {'form': DTPForm()})  

        else:
            messages.error(request, "❌ Помилка! Будь ласка, перевірте введені дані.")

    else:
        form = DTPForm()

    return render(request, 'create.html', {'form': form})



def success(request):
    dtp = DTP.objects.all()
    return render(request, 'success.html', {'dtp': dtp})


def get_id(request, pk):
    dtp = get_object_or_404(DTP, pk=pk)
    return render(request, 'getID.html', {'dtp': dtp})

# Оновлена функція для створення PDF з xhtml2pdf
def generate_pdf(protocol):
    html_string = render_to_string('protocol_template.html', {'protocol': protocol})  # type: ignore # Генерація HTML
    response = BytesIO()  # Створюємо пам'ять для PDF
    pisa_status = pisa.CreatePDF(html_string, dest=response)  # type: ignore # Перетворюємо HTML в PDF

    if pisa_status.err:
        return None  # Якщо сталася помилка, повертаємо None

    return response.getvalue()  # Повертаємо PDF у вигляді байтів

# Генерація та скачування PDF
def generate_protocol_pdf(request, protocol_id):
    protocol = get_object_or_404(DTP, id=protocol_id)
    pdf = generate_pdf(protocol)

    if pdf is None:
        return HttpResponse('Помилка при створенні PDF', status=500)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="protocol_{protocol_id}.pdf"'
    return response

# Завантаження PDF у файлову систему
def download_protocol_pdf(request, protocol_id):
    protocol = get_object_or_404(DTP, id=protocol_id)
    pdf = generate_pdf(protocol)

    if pdf is None:
        return HttpResponse('Помилка при створенні PDF', status=500)

    fs = FileSystemStorage() # type: ignore
    filename = f'protocol_{protocol_id}.pdf'
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    with open(file_path, 'wb') as f:
        f.write(pdf)

    file_url = fs.url(filename)
    return render(request, 'success.html', {'protocol': protocol, 'file_url': file_url})


def generate_pdf(request):
    # Створення PDF у пам'яті
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Додаємо текст у PDF
    p.setFont("Helvetica", 12)
    p.drawString(100, 800, "Євро-протокол ДТП")
    p.drawString(100, 780, f"Дата ДТП: {request.GET.get('date', 'Не вказано')}")
    p.drawString(100, 760, f"Місце ДТП: {request.GET.get('location', 'Не вказано')}")
    p.drawString(100, 740, f"Водій 1: {request.GET.get('name_dri1', 'Не вказано')}")
    p.drawString(100, 720, f"Номер авто (Водій 1): {request.GET.get('license_plate1', 'Не вказано')}")
    p.drawString(100, 700, f"Водій 2: {request.GET.get('name_dri2', 'Не вказано')}")
    p.drawString(100, 680, f"Номер авто (Водій 2): {request.GET.get('license_plate2', 'Не вказано')}")
    p.drawString(100, 660, f"Страхування: {request.GET.get('insurance', 'Не вказано')}")

    # Завершуємо PDF
    p.showPage()
    p.save()

    # Повертаємо PDF як відповідь
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="dtp_protocol.pdf"'
    return response