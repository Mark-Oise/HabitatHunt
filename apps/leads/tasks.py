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



def calculate_sentiment_score(text):
    """Convert OpenAI's 0-1 score to 0-100 scale"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Analyze the sentiment and return a score between 0 and 1, where 0 is very negative and 1 is very positive."},
                {"role": "user", "content": text}
            ],
            max_tokens=5
        )
        score = float(response.choices[0].message.content.strip())
        return score * 100  # Convert to 0-100 scale
    except:
        return 50  # Return neutral score if analysis fails

def calculate_engagement_score(comment):
    """Calculate engagement score based on likes and replies"""
    likes_score = min(comment.likes * 0.5, 60)  # Max 60 points from likes
    replies_score = min(comment.replies * 2, 40)  # Max 40 points from replies
    return min(likes_score + replies_score, 100)  # Cap at 100


@shared_task
def process_leads():
    # Process scraped comments and qualify potential leads
    for comment in RawComment.objects.filter(processed=False):
        # Calculate scores
        sentiment_score = calculate_sentiment_score(comment.text)
        engagement_score = calculate_engagement_score(comment)
        
        # Determine category
        category = (
            'hot' if sentiment_score >= 80 and engagement_score >= 50
            else 'warm' if sentiment_score >= 50 and engagement_score >= 30
            else 'cold'
        )

        # Save as a Lead
        Lead.objects.create(
            username=comment.username,
            text=comment.text,
            platform=comment.platform,
            sentiment_score=sentiment_score,
            engagement_score=engagement_score,
            category=category,
            source=comment.platform
        )
        
        # Mark as processed
        comment.processed = True
        comment.save()