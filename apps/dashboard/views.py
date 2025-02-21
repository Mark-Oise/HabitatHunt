from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, F, ExpressionWrapper, FloatField
from django.db.models.functions import ExtractMonth
from django.utils import timezone
from datetime import timedelta
from apps.leads.models import Lead

# Create your views here.


@login_required
def dashboard(request):
    # Get current user's leads
    current_month = timezone.now()
    last_month = current_month - timedelta(days=30)
    
    # Total leads count and growth
    total_leads = Lead.objects.filter(user=request.user).count()
    last_month_leads = Lead.objects.filter(
        user=request.user,
        created_at__lte=last_month
    ).count()
    
    lead_growth = 0
    if last_month_leads > 0:
        lead_growth = ((total_leads - last_month_leads) / last_month_leads) * 100

    # Average sentiment score and growth
    current_sentiment = Lead.objects.filter(
        user=request.user,
        created_at__gte=last_month
    ).aggregate(avg=Avg('sentiment_score'))['avg'] or 0
    
    last_month_sentiment = Lead.objects.filter(
        user=request.user,
        created_at__lte=last_month
    ).aggregate(avg=Avg('sentiment_score'))['avg'] or 0
    
    sentiment_growth = 0
    if last_month_sentiment > 0:
        sentiment_growth = ((current_sentiment - last_month_sentiment) / last_month_sentiment) * 100

    # Average engagement score and growth
    current_engagement = Lead.objects.filter(
        user=request.user,
        created_at__gte=last_month
    ).aggregate(avg=Avg('engagement_score'))['avg'] or 0
    
    last_month_engagement = Lead.objects.filter(
        user=request.user,
        created_at__lte=last_month
    ).aggregate(avg=Avg('engagement_score'))['avg'] or 0
    
    engagement_growth = 0
    if last_month_engagement > 0:
        engagement_growth = ((current_engagement - last_month_engagement) / last_month_engagement) * 100

    context = {
        'total_leads': total_leads,
        'lead_growth': round(lead_growth, 1),
        'avg_sentiment': round(current_sentiment, 1),
        'sentiment_growth': round(sentiment_growth, 1),
        'avg_engagement': round(current_engagement, 1),
        'engagement_growth': round(engagement_growth, 1),
    }
    
    return render(request, 'dashboard/dashboard.html', context)