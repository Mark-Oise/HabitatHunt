from celery import shared_task
import openai
from .models import RawComment, Lead

@shared_task
def clean_scraped_data():
    # Remove duplicate and spam comments
    unique_comments = {}
    for comment in RawComment.objects.all():
        key = (comment.text.lower(), comment.platform)
        if key not in unique_comments:
            unique_comments[key] = comment
        else:
            comment.delete()

    print('Data cleaned successfully')


@shared_task
def process_leads():
    # Process scraped comments and qualify potential leads
    for comment in RawComment.objects.all():
        # Run sentiment analysis using OpenAI
        response = openai.Completion.create(
            model="gpt-4",
            prompt=f'Analyze the sentiment of the following comment: {comment.text}',
            max_tokens=5,
        )
        sentiment_score = float(response['choices'][0]['text'])
        
        # Lead Scoring
        engagement_score = comment.engagement_score
        category = 'hot' if sentiment_score > 0.8 and engagement_score > 50 else 'warm' if sentiment_score > 0.5 and engagement_score > 0.5 else 'cold'
        

        # Save as a Lead
        Lead.objects.create(
            comment=comment.text,
            platform=comment.platform,
            sentiment_score=sentiment_score,
            engagement_score=engagement_score,
            category=category
        )