from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Sum
from royalties.models import Payment, Artist, RoyaltyRecord
from django.shortcuts import get_object_or_404
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
import json
from datetime import date
from django.contrib.auth.decorators import login_required

def pending_payments(request):
    payments = Payment.objects.filter(status='pending').select_related('artist')
    data = [
        {
            "artist": p.artist.name,
            "amount": float(p.amount),
            "due_date": p.due_date.strftime("%Y-%m-%d"),
            "status": p.status
        }
        for p in payments
    ]
    return JsonResponse(data, safe=False)

def artist_payments(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    payments = Payment.objects.filter(artist=artist).order_by('-due_date')
    
    data = [
        {
            "amount": float(p.amount),
            "status": p.status,
            "due_date": p.due_date.strftime("%Y-%m-%d"),
            "paid_date": p.paid_date.strftime("%Y-%m-%d") if p.paid_date else None
        }
        for p in payments
    ]

    return JsonResponse({
        "artist": artist.name,
        "payments": data
    })

def artist_summary(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)

    # Total royalties
    all_records = RoyaltyRecord.objects.filter(track__artist=artist)
    total_earned = sum(r.stream_count * float(r.payout_per_stream) for r in all_records)

    # Payments (paid & pending)
    payments = Payment.objects.filter(artist=artist)
    total_paid = sum(float(p.amount) for p in payments if p.status == 'paid')
    total_pending = sum(float(p.amount) for p in payments if p.status == 'pending')

    return JsonResponse({
        "artist": artist.name,
        "total_earned": round(total_earned, 2),
        "total_paid": round(total_paid, 2),
        "total_pending": round(total_pending, 2)
    })

@csrf_exempt
def mark_payment_as_paid(request, payment_id):
    if request.method == "PATCH":
        payment = get_object_or_404(Payment, id=payment_id)

        if payment.status == "paid":
            return JsonResponse({"message": "Already marked as paid."}, status=400)

        payment.status = "paid"
        payment.paid_date = date.today()
        payment.save()

        return JsonResponse({"message": "Payment marked as paid!"})

    return JsonResponse({"error": "Only PATCH method allowed."}, status=405)

@login_required
def artist_dashboard(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    if request.user != artist.user:
        return HttpResponseForbidden("You do not have access to this artist's dashboard.")
    
    records = RoyaltyRecord.objects.filter(track__artist=artist)
    payments = Payment.objects.filter(artist=artist).order_by('-due_date')

    total_earned = sum(r.stream_count * float(r.payout_per_stream) for r in records)
    total_paid = sum(float(p.amount) for p in payments if p.status == 'paid')
    total_pending = sum(float(p.amount) for p in payments if p.status == 'pending')

    return render(request, 'royalties/artist_dashboard.html', {
        'artist': artist,
        'total_earned': round(total_earned, 2),
        'total_paid': round(total_paid, 2),
        'total_pending': round(total_pending, 2),
        'payments': payments
    })

@login_required
def my_dashboard_redirect(request):
    artist = get_object_or_404(Artist, user=request.user)
    return redirect('artist_dashboard', artist_id=artist.id)

def home_page(request):
    return render(request, 'royalties/home.html')