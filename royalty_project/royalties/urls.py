from django.urls import path
from .views import pending_payments, artist_payments, artist_summary, mark_payment_as_paid, artist_dashboard, my_dashboard_redirect,home_page


urlpatterns = [
    path('api/payments/pending/', pending_payments, name='pending_payments'),
    path('api/payments/<int:artist_id>/', artist_payments),
    path('api/artist/<int:artist_id>/summary/', artist_summary),
    path('api/payments/<int:payment_id>/mark_paid/', mark_payment_as_paid, name='mark_paid'),
    path('artist/<int:artist_id>/dashboard/', artist_dashboard, name='artist_dashboard'),
    path('dashboard/', my_dashboard_redirect, name='my_dashboard'),
    path('', home_page, name='home'),
]
