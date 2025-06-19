from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import PlateSession
from .camera import process_camera_feed
from django.db.models import Sum
from datetime import timedelta, datetime
from django.http import HttpResponse
import csv
from django.db.models.functions import TruncDate
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import ManualEntryForm, UpdateSessionForm
from .utils import calculate_charge
from django.contrib.auth.decorators import login_required
from .utils import calculate_charge
from .decorators import employee_required


@employee_required
def dashboard(request):
    query = request.GET.get('q', '')
    payment_filter = request.GET.get('status', '')

    # Base queryset
    sessions = PlateSession.objects.all().order_by('-entry_time')

    # Search by plate number
    if query:
        sessions = sessions.filter(plate_number__icontains=query)

    # Filter by payment status
    if payment_filter == 'paid':
        sessions = sessions.filter(is_paid=True)
    elif payment_filter == 'unpaid':
        sessions = sessions.filter(is_paid=False)

    # Parking slot availability logic
    total_slots = {'Car': 25, 'Bike': 20, 'Bus': 5}
    current_occupancy = {
        'Car': PlateSession.objects.filter(vehicle_type='Car', exit_time__isnull=True).count(),
        'Bike': PlateSession.objects.filter(vehicle_type='Bike', exit_time__isnull=True).count(),
        'Bus': PlateSession.objects.filter(vehicle_type='Bus', exit_time__isnull=True).count()
    }
    available_slots = {vt: total_slots[vt] - current_occupancy[vt] for vt in total_slots}
    no_slots_available = all(v == 0 for v in available_slots.values())
    context = {
    'sessions': sessions,
    'available_slots': available_slots,
    'query': query,
    'payment_filter': payment_filter,
    'no_slots_available': no_slots_available,
    }

    return render(request, 'dashboard.html', context)

def detect_redirect_page(request):
    plate_number = process_camera_feed()

    if plate_number:
        session = PlateSession.objects.filter(plate_number=plate_number, exit_time__isnull=False).last()
        if session:
            return redirect('receipt', session_id=session.id)
        else:
            return redirect('dashboard')
    else:
        return redirect('dashboard')


def receipt(request, session_id):
    session = get_object_or_404(PlateSession, id=session_id)
    return render(request, 'receipt.html', {'session': session})


@employee_required
def earnings_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    sessions = PlateSession.objects.filter(is_paid=True)

    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        sessions = sessions.filter(exit_time__date__range=(start_date, end_date))

    total_earnings = sessions.aggregate(Sum('charge'))['charge__sum'] or 0

    type_summary = sessions.values('vehicle_type').annotate(total=Sum('charge')).order_by('vehicle_type')

    last_7_days = timezone.now().date() - timedelta(days=6)
    daily_data = PlateSession.objects.filter(
        is_paid=True,
        exit_time__date__gte=last_7_days
    ).annotate(
        date=TruncDate('exit_time')
    ).values('date').annotate(total=Sum('charge')).order_by('date')

    chart_labels = [d['date'].strftime('%b %d') for d in daily_data]
    chart_values = [float(d['total']) for d in daily_data]

    return render(request, 'earnings_report.html', {
        'sessions': sessions.order_by('-exit_time'),
        'total_earnings': total_earnings,
        'type_summary': type_summary,
        'start_date': start_date,
        'end_date': end_date,
        'chart_labels': chart_labels,
        'chart_values': chart_values
    })

@employee_required
def export_earnings_csv(request):
    sessions = PlateSession.objects.filter(is_paid=True).order_by('-exit_time')

    # Create response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="earnings_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Plate Number', 'Vehicle Type', 'Entry Time', 'Exit Time', 'Charge (₹)'])

    for s in sessions:
        writer.writerow([
            s.plate_number,
            s.vehicle_type,
            s.entry_time.strftime('%Y-%m-%d %H:%M'),
            s.exit_time.strftime('%Y-%m-%d %H:%M') if s.exit_time else '',
            s.charge
        ])

    return response


def generate_pdf_receipt(request, session_id):
    session = get_object_or_404(PlateSession, id=session_id)
    template_path = 'receipt_pdf.html'
    context = {'session': session}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{session.plate_number}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error while generating PDF', status=500)
    
    return response



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')

@employee_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


@employee_required
def manual_entry_view(request):
    if request.method == 'POST':
        form = ManualEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.entry_time = timezone.now()
            entry.save()
            return redirect('dashboard')
    else:
        form = ManualEntryForm()
    return render(request, 'entry.html', {'form': form})



@employee_required
def session_update_view(request, session_id):
    session = get_object_or_404(PlateSession, id=session_id)

    if request.method == 'POST':
        form = UpdateSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UpdateSessionForm(instance=session)

    return render(request, 'update_session.html', {'form': form, 'session': session})


@employee_required
def manual_entry_view(request):
    if not hasattr(request.user, 'employeeprofile') or not request.user.employeeprofile.is_employee:
        return render(request, 'access_denied.html')

    if request.method == 'POST':
        form = ManualEntryForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            if session.exit_time:
                duration = session.exit_time - session.entry_time
                session.charge = round((duration.total_seconds() / 3600) * 50)  # ₹50/hr
            session.save()
            return redirect('dashboard')
    else:
        form = ManualEntryForm()
    
    return render(request, 'manual_entry.html', {'form': form})