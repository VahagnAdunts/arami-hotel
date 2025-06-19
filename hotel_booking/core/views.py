from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils.timezone import now, timezone
from datetime import datetime, timedelta
from .models import Room, Booking, ContactMessage
from django.core.mail import send_mail

def get_seasonal_price(room, check_in_date):
    price_entry = room.seasonal_prices.filter(start_date__lte=check_in_date, end_date__gte=check_in_date).first()
    return price_entry.price_per_night if price_entry else room.price_per_night

def calculate_total_price(room, check_in, check_out):
    total_price = 0
    current_date = check_in
    while current_date < check_out:
        price = get_seasonal_price(room, current_date)
        total_price += price
        current_date += timedelta(days=1)
    return total_price

def home(request):
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')
    guests = request.GET.get('guests')
    rooms = Room.objects.all()
    room_prices = {}

    if check_in and check_out and guests:
        try:
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
            guests = int(guests)
        except (ValueError, TypeError):
            check_in_date = check_out_date = None
            guests = 1

        available_rooms = []
        for room in rooms:
            overlapping_bookings = Booking.objects.filter(
                room=room,
                check_out__gt=check_in_date,
                check_in__lt=check_out_date
            ).count()

            if overlapping_bookings < room.total_count and room.capacity >= guests:
                available_rooms.append(room)
                room_prices[room.id] = calculate_total_price(room, check_in_date, check_out_date)

        rooms = available_rooms

    return render(request, 'core/home.html', {
        'rooms': rooms,
        'room_prices': room_prices,
        'check_in': check_in,
        'check_out': check_out,
        'guests': guests,
        'now': now()
    })

def check_availability(request):
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')
    guests = request.GET.get('guests')

    rooms = Room.objects.all()
    available_rooms = []
    room_prices = {}

    if check_in and check_out and guests:
        try:
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
            guests = int(guests)
        except (ValueError, TypeError):
            check_in_date = check_out_date = None
            guests = 1

        for room in rooms:
            overlapping = Booking.objects.filter(
                room=room,
                check_out__gt=check_in_date,
                check_in__lt=check_out_date
            ).count()

            if overlapping < room.total_count and room.capacity >= guests:
                available_rooms.append(room)
                room_prices[room.id] = calculate_total_price(room, check_in_date, check_out_date)

    return render(request, 'core/availability.html', {
        'rooms': available_rooms,
        'room_prices': room_prices,
        'check_in': check_in,
        'check_out': check_out,
        'guests': guests,
    })

def book_room(request, room_type):
    room = get_object_or_404(Room, type=room_type)

    if request.method == 'POST':
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        guests = request.POST.get('guests') or 1
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        try:
            guests = int(guests)
        except ValueError:
            guests = 1

        overlapping = Booking.objects.filter(
            room=room,
            check_out__gt=check_in,
            check_in__lt=check_out
        ).count()

        if overlapping >= room.total_count:
            return HttpResponse("Sorry, this room is no longer available.")

        Booking.objects.create(
            room=room,
            full_name=full_name,
            email=email,
            phone=phone,
            check_in=check_in,
            check_out=check_out
        )
        # Send booking email
        total_price = calculate_total_price(room, datetime.strptime(check_in, "%Y-%m-%d").date(), datetime.strptime(check_out, "%Y-%m-%d").date())
        send_mail(
            subject='New Room Booking - Arami Hotel',
            message=f'Full Name: {full_name}\nEmail: {email}\nPhone: {phone}\nRoom Type: {room.get_type_display()}\nCheck-in: {check_in}\nCheck-out: {check_out}\nGuests: {guests}\nTotal Price: {total_price} AMD',
            from_email='hotelarami23@gmail.com',
            recipient_list=['hotelarami23@gmail.com'],
            fail_silently=False,
        )
        return redirect('booking_success')

    return render(request, 'core/book_room.html', {
        'room': room,
        'check_in': request.GET.get('check_in'),
        'check_out': request.GET.get('check_out'),
        'guests': request.GET.get('guests') or 1,
    })

def booking_success(request):
    return render(request, 'core/booking_success.html')

def contact_submit(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        message = request.POST.get('message')

        if email and message:
            ContactMessage.objects.create(
                email=email,
                message=message
            )
            send_mail(
                subject='New Contact Message from Arami Hotel Website',
                message=f'From: {email}\n\nMessage:\n{message}',
                from_email='hotelarami23@gmail.com',
                recipient_list=['hotelarami23@gmail.com'],
                fail_silently=False,
            )
            return render(request, 'core/contact_success.html')
    return redirect('/')

def rooms(request):
    rooms = Room.objects.all()
    today = timezone.now().date()
    tomorrow = today + timedelta(days=1)
    return render(request, 'core/rooms.html', {
        'rooms': rooms,
        'today': today,
        'tomorrow': tomorrow
    })

def room_detail(request, room_type):
    room = get_object_or_404(Room, type=room_type)
    room_photos = room.images.all()
    message = None
    total_price = None

    check_in_str = request.GET.get('check_in')
    check_out_str = request.GET.get('check_out')

    if check_in_str and check_out_str:
        try:
            check_in = datetime.strptime(check_in_str, "%Y-%m-%d").date()
            check_out = datetime.strptime(check_out_str, "%Y-%m-%d").date()
            total_price = calculate_total_price(room, check_in, check_out)
        except ValueError:
            pass

    if request.method == 'POST':
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        guests = request.POST.get('guests') or 1
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        try:
            guests = int(guests)
        except ValueError:
            guests = 1

        overlapping = Booking.objects.filter(
            room=room,
            check_out__gt=check_in,
            check_in__lt=check_out
        ).count()

        if overlapping >= room.total_count:
            message = "❌ Sorry, this room is not available for the selected dates."
        else:
            Booking.objects.create(
                room=room,
                full_name=full_name,
                email=email,
                phone=phone,
                check_in=check_in,
                check_out=check_out
            )
            # Send booking email
            total_price = calculate_total_price(room, datetime.strptime(check_in, "%Y-%m-%d").date(), datetime.strptime(check_out, "%Y-%m-%d").date())
            send_mail(
                subject='New Room Booking - Arami Hotel',
                message=f'Full Name: {full_name}\nEmail: {email}\nPhone: {phone}\nRoom Type: {room.get_type_display()}\nCheck-in: {check_in}\nCheck-out: {check_out}\nGuests: {guests}\nTotal Price: {total_price} AMD',
                from_email='hotelarami23@gmail.com',
                recipient_list=['hotelarami23@gmail.com'],
                fail_silently=False,
            )
            return redirect('booking_success')

    return render(request, 'core/room_detail.html', {
        'room': room,
        'room_photos': room_photos,
        'check_in': check_in_str,
        'check_out': check_out_str,
        'guests': request.GET.get('guests') or 1,
        'total_price': total_price,
        'message': message
    })
