import openai
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from .models import Lead, LeadPreference
from .scrapers import FacebookScraper, InstagramScraper
from apps.platforms.models import Platform
from apps.targets.models import TargetScrapeLog
from apps.hashtags.models import HashtagScrapeLog
from apps.locations.models import LocationScrapeLog

class LeadGenerationService:
    # Real estate keywords with intent weights
    REAL_ESTATE_KEYWORDS = {
        # High intent keywords
        'buying home': 1.0, 'selling house': 1.0, 'need realtor': 1.0,
        'house hunting': 1.0, 'mortgage approved': 1.0, 'home buyer': 1.0,
        'first time buyer': 1.0, 'looking to buy': 1.0,
        
        # Medium intent keywords  
        'moving': 0.7, 'relocating': 0.7, 'new neighborhood': 0.7,
        'home search': 0.7, 'property investment': 0.7, 'downsizing': 0.7,
        'upgrading home': 0.7,
        
        # Lower intent keywords
        'real estate': 0.4, 'housing market': 0.4, 'home prices': 0.4,
        'rental': 0.4, 'property': 0.4
    }
    
    def __init__(self):
        self.facebook_scraper = FacebookScraper()
        self.instagram_scraper = InstagramScraper()
        openai.api_key = settings.OPENAI_API_KEY
    
    def process_lead_request(self, form_data, user):
        """Main orchestrator for lead generation"""
        platforms = form_data['platforms']
        targets = form_data['targets'] 
        hashtags = form_data['hashtags']
        engagement_threshold = form_data['engagement_threshold']
        
        all_leads = []
        
        # Process target pages
        if targets:
            target_leads = self.scrape_target_pages(targets, platforms, engagement_threshold)
            all_leads.extend(target_leads)
        
        # Process hashtags
        if hashtags:
            hashtag_leads = self.scrape_hashtags(hashtags, platforms, engagement_threshold)
            all_leads.extend(hashtag_leads)
        
        # Filter by location if specified
        location_filtered_leads = self.filter_by_location(
            all_leads, 
            form_data.get('custom_locations', []),
            form_data.get('cities', []),
            form_data.get('provinces', []),
            user
        )
        
        # Save or update leads
        saved_leads = self.save_leads(location_filtered_leads, user)
        
        return {
            'total_processed': len(all_leads),
            'location_filtered': len(location_filtered_leads), 
            'saved_leads': len(saved_leads),
            'leads': saved_leads
        }
    
    def scrape_target_pages(self, targets, platforms, engagement_threshold):
        """Scrape posts from target pages, then analyze their comments"""
        leads = []
        
        for target in targets:
            start_time = datetime.now()
            posts_scraped = 0
            comments_scraped = 0
            target_leads = []
            
            try:
                if target.platform.name == 'facebook':
                    target_leads = self.facebook_scraper.scrape_page_comments(
                        target.username, engagement_threshold
                    )
                elif target.platform.name == 'instagram':
                    target_leads = self.instagram_scraper.scrape_page_comments(
                        target.username, engagement_threshold
                    )
                
                leads.extend(target_leads)
                
                # Update target's last_scraped timestamp
                target.last_scraped = timezone.now()
                target.save()
                
                # Log successful scraping
                TargetScrapeLog.objects.create(
                    target=target,
                    posts_scraped=posts_scraped,
                    comments_scraped=comments_scraped,
                    leads_generated=len(target_leads),
                    status='success',
                    scrape_duration=datetime.now() - start_time
                )
                
            except Exception as e:
                # Log failed scraping
                TargetScrapeLog.objects.create(
                    target=target,
                    posts_scraped=0,
                    comments_scraped=0,
                    leads_generated=0,
                    status='failed',
                    error_message=str(e),
                    scrape_duration=datetime.now() - start_time
                )
                print(f"Error scraping target {target.username}: {e}")
        
        return leads
    
    def scrape_hashtags(self, hashtags, platforms, engagement_threshold):
        """Scrape posts by hashtags and analyze interactions"""
        leads = []
        
        for hashtag in hashtags:
            for platform in platforms:
                start_time = datetime.now()
                posts_scraped = 0
                interactions_scraped = 0
                hashtag_leads = []
                
                try:
                    if platform.name == 'facebook':
                        hashtag_leads = self.facebook_scraper.scrape_hashtag_interactions(
                            hashtag.name, engagement_threshold
                        )
                    elif platform.name == 'instagram':
                        hashtag_leads = self.instagram_scraper.scrape_hashtag_interactions(
                            hashtag.name, engagement_threshold
                        )
                    
                    leads.extend(hashtag_leads)
                    
                    # Log successful hashtag scraping
                    HashtagScrapeLog.objects.create(
                        hashtag=hashtag,
                        platform=platform,
                        posts_scraped=posts_scraped,
                        interactions_scraped=interactions_scraped,
                        leads_generated=len(hashtag_leads),
                        status='success',
                        scrape_duration=datetime.now() - start_time
                    )
                    
                except Exception as e:
                    # Log failed hashtag scraping
                    HashtagScrapeLog.objects.create(
                        hashtag=hashtag,
                        platform=platform,
                        posts_scraped=0,
                        interactions_scraped=0,
                        leads_generated=0,
                        status='failed',
                        error_message=str(e),
                        scrape_duration=datetime.now() - start_time
                    )
                    print(f"Error scraping hashtag #{hashtag.name} on {platform.name}: {e}")
        
        return leads
    
    def qualify_lead(self, user_data, engagement_threshold, text_content=""):
        """Determine if user meets lead criteria"""
        # Calculate engagement score
        engagement_score = self.calculate_engagement_score(
            user_data.get('likes', 0),
            user_data.get('comments', 0), 
            user_data.get('shares', 0)
        )
        
        # Check engagement threshold
        if engagement_score < engagement_threshold:
            return False, 0, 0
        
        # Calculate sentiment score
        sentiment_score = self.calculate_sentiment_score(text_content)
        
        # Check for real estate intent
        intent_score = self.calculate_intent_score(text_content)
        
        # Qualify if has decent engagement and some real estate intent
        is_qualified = engagement_score >= engagement_threshold and intent_score > 0.3
        
        return is_qualified, engagement_score, sentiment_score
    
    def calculate_engagement_score(self, likes, comments, shares):
        """Calculate engagement score based on interactions"""
        # Weighted scoring: comments worth more than likes
        score = (comments * 3) + (likes * 1) + (shares * 5)
        
        # Normalize to 0-100 scale (adjust multiplier based on your data)
        normalized_score = min(score * 2, 100)
        
        return normalized_score
    
    def calculate_sentiment_score(self, text_content):
        """Use OpenAI to analyze sentiment of user's content"""
        if not text_content.strip():
            return 0.5  # Neutral if no content
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "Analyze the sentiment of this real estate related text. Return only a number between 0 and 1, where 0 is very negative, 0.5 is neutral, and 1 is very positive."
                    },
                    {"role": "user", "content": text_content}
                ],
                max_tokens=10,
                temperature=0
            )
            
            sentiment = float(response.choices[0].message.content.strip())
            return max(0, min(1, sentiment))  # Ensure 0-1 range
            
        except Exception as e:
            print(f"Error calculating sentiment: {e}")
            return 0.5  # Default to neutral on error
    
    def calculate_intent_score(self, text_content):
        """Calculate real estate intent based on keywords"""
        if not text_content:
            return 0
        
        text_lower = text_content.lower()
        intent_score = 0
        
        for keyword, weight in self.REAL_ESTATE_KEYWORDS.items():
            if keyword in text_lower:
                intent_score += weight
        
        # Normalize to 0-1 scale
        return min(intent_score, 1.0)
    
    def filter_by_location(self, leads, custom_locations, cities, provinces, user):
        """Filter leads by location criteria with detailed logging"""
        if not (custom_locations or cities or provinces):
            return leads  # No location filtering
        
        total_leads_before = len(leads)
        filtered_leads = []
        
        # Track matches for each location type
        location_matches = {
            'custom': {},
            'city': {},
            'province': {}
        }
        
        for lead_data in leads:
            user_location = lead_data.get('location', '').lower()
            matched = False
            
            # Check custom locations
            for custom_loc in custom_locations:
                if custom_loc.location_text.lower() in user_location:
                    filtered_leads.append(lead_data)
                    location_matches['custom'][custom_loc.location_text] = location_matches['custom'].get(custom_loc.location_text, 0) + 1
                    matched = True
                    break
            
            if not matched:
                # Check cities
                for city in cities:
                    if city.name.lower() in user_location:
                        filtered_leads.append(lead_data)
                        location_matches['city'][city.name] = location_matches['city'].get(city.name, 0) + 1
                        matched = True
                        break
            
            if not matched:
                # Check provinces
                for province in provinces:
                    if province.name.lower() in user_location or province.code.lower() in user_location:
                        filtered_leads.append(lead_data)
                        location_matches['province'][province.name] = location_matches['province'].get(province.name, 0) + 1
                        matched = True
                        break
        
        # Log location filtering results
        for location_type, matches in location_matches.items():
            for location_name, match_count in matches.items():
                LocationScrapeLog.objects.create(
                    user=user,
                    location_type=location_type,
                    location_name=location_name,
                    total_leads_before_filter=total_leads_before,
                    leads_matched=match_count,
                    leads_filtered_out=total_leads_before - len(filtered_leads),
                    status='success'
                )
        
        return filtered_leads
    
    def save_leads(self, leads_data, user):
        """Save or update leads in database"""
        saved_leads = []
        
        for lead_data in leads_data:
            # Check for existing lead (username + platform)
            existing_lead = Lead.objects.filter(
                user=user,
                username=lead_data['username'],
                source__name=lead_data['platform']
            ).first()
            
            if existing_lead:
                # Update existing lead
                existing_lead.engagement_score = lead_data['engagement_score']
                existing_lead.sentiment_score = lead_data['sentiment_score']
                existing_lead.updated_at = timezone.now()
                existing_lead.save()
                saved_leads.append(existing_lead)
            else:
                # Create new lead
                platform = Platform.objects.get(name=lead_data['platform'])
                
                new_lead = Lead.objects.create(
                    user=user,
                    name=lead_data.get('name', ''),
                    username=lead_data['username'],
                    message=lead_data.get('message', ''),
                    profile_url=lead_data.get('profile_url', ''),
                    profile_picture_url=lead_data.get('profile_picture_url', ''),
                    location=lead_data.get('location', ''),
                    sentiment_score=lead_data['sentiment_score'],
                    engagement_score=lead_data['engagement_score'],
                    source=platform,
                    category=self.categorize_lead(lead_data['sentiment_score'], lead_data['engagement_score'])
                )
                saved_leads.append(new_lead)
        
        return saved_leads
    
    def categorize_lead(self, sentiment_score, engagement_score):
        """Automatically categorize lead based on scores"""
        if sentiment_score > 0.8 and engagement_score > 70:
            return 'hot'
        elif sentiment_score > 0.6 and engagement_score > 40:
            return 'warm'
        else:
            return 'cold'