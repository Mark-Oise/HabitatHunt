import requests
import time
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from apify_client import ApifyClient

class BaseScraper:
    """Base scraper class with common functionality"""
    
    def __init__(self):
        self.client = ApifyClient(settings.APIFY_API_TOKEN)
        self.max_results_per_request = 100  # Reasonable limit
        
    def wait_for_run_completion(self, run, timeout=300):
        """Wait for Apify actor run to complete"""
        start_time = time.time()
        
        while run['status'] in ['READY', 'RUNNING']:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Run {run['id']} timed out after {timeout} seconds")
            
            time.sleep(10)  # Check every 10 seconds
            run = self.client.run(run['id']).get()
        
        if run['status'] != 'SUCCEEDED':
            raise Exception(f"Run failed with status: {run['status']}")
        
        return run
    
    def extract_user_data(self, item, platform):
        """Extract standardized user data from scraped item"""
        return {
            'username': item.get('ownerUsername', ''),
            'name': item.get('ownerFullName', ''),
            'profile_url': item.get('ownerUrl', ''),
            'profile_picture_url': item.get('ownerPictureUrl', ''),
            'location': item.get('locationText', ''),
            'message': item.get('text', ''),
            'likes': item.get('likesCount', 0),
            'comments': item.get('commentsCount', 0),
            'shares': item.get('sharesCount', 0),
            'platform': platform,
            'post_url': item.get('url', ''),
            'created_time': item.get('time', '')
        }


class FacebookScraper(BaseScraper):
    """Facebook scraper using Apify's Facebook scrapers"""
    
    def scrape_page_comments(self, page_username, engagement_threshold):
        """Scrape comments from a Facebook page's recent posts"""
        leads = []
        
        try:
            # First, get recent posts from the page
            posts = self._get_page_posts(page_username)
            
            # Then scrape comments from those posts
            for post in posts[:10]:  # Limit to recent 10 posts
                post_comments = self._get_post_comments(post['url'])
                
                for comment in post_comments:
                    user_data = self.extract_user_data(comment, 'facebook')
                    
                    # Skip if no username (invalid data)
                    if not user_data['username']:
                        continue
                    
                    # Combine post content and comment for analysis
                    combined_text = f"{post.get('text', '')} {comment.get('text', '')}"
                    
                    # Import here to avoid circular imports
                    from .services import LeadGenerationService
                    service = LeadGenerationService()
                    
                    is_qualified, eng_score, sent_score = service.qualify_lead(
                        user_data, engagement_threshold, combined_text
                    )
                    
                    if is_qualified:
                        user_data.update({
                            'engagement_score': eng_score,
                            'sentiment_score': sent_score
                        })
                        leads.append(user_data)
            
        except Exception as e:
            print(f"Error scraping Facebook page {page_username}: {e}")
        
        return leads
    
    def scrape_hashtag_interactions(self, hashtag, engagement_threshold):
        """Scrape posts and interactions for a specific hashtag"""
        leads = []
        
        try:
            # Use Facebook Search Scraper for hashtag posts
            run_input = {
                "search": f"#{hashtag}",
                "searchType": "posts",
                "resultsLimit": self.max_results_per_request,
                "maxPostDate": (datetime.now() - timedelta(days=30)).isoformat(),
            }
            
            run = self.client.actor("apify/facebook-search-scraper").call(run_input=run_input)
            run = self.wait_for_run_completion(run)
            
            # Process results
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                user_data = self.extract_user_data(item, 'facebook')
                
                if not user_data['username']:
                    continue
                
                # Import here to avoid circular imports
                from .services import LeadGenerationService
                service = LeadGenerationService()
                
                is_qualified, eng_score, sent_score = service.qualify_lead(
                    user_data, engagement_threshold, user_data['message']
                )
                
                if is_qualified:
                    user_data.update({
                        'engagement_score': eng_score,
                        'sentiment_score': sent_score
                    })
                    leads.append(user_data)
            
        except Exception as e:
            print(f"Error scraping Facebook hashtag #{hashtag}: {e}")
        
        return leads
    
    def _get_page_posts(self, page_username):
        """Get recent posts from a Facebook page"""
        try:
            run_input = {
                "startUrls": [f"https://www.facebook.com/{page_username}"],
                "resultsLimit": 20,  # Recent posts only
            }
            
            run = self.client.actor("apify/facebook-pages-scraper").call(run_input=run_input)
            run = self.wait_for_run_completion(run)
            
            posts = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                posts.append(item)
            
            return posts
            
        except Exception as e:
            print(f"Error getting posts from Facebook page {page_username}: {e}")
            return []
    
    def _get_post_comments(self, post_url):
        """Get comments from a specific Facebook post"""
        try:
            run_input = {
                "startUrls": [post_url],
                "maxComments": 50,  # Limit comments per post
            }
            
            run = self.client.actor("apify/facebook-comments-scraper").call(run_input=run_input)
            run = self.wait_for_run_completion(run)
            
            comments = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                comments.append(item)
            
            return comments
            
        except Exception as e:
            print(f"Error getting comments from Facebook post {post_url}: {e}")
            return []


class InstagramScraper(BaseScraper):
    """Instagram scraper using Apify's Instagram scrapers"""
    
    def scrape_page_comments(self, page_username, engagement_threshold):
        """Scrape comments from an Instagram profile's recent posts"""
        leads = []
        
        try:
            # Get recent posts from the profile
            posts = self._get_profile_posts(page_username)
            
            # Scrape comments from those posts
            for post in posts[:10]:  # Limit to recent 10 posts
                post_comments = self._get_post_comments(post['url'])
                
                for comment in post_comments:
                    user_data = self.extract_user_data(comment, 'instagram')
                    
                    if not user_data['username']:
                        continue
                    
                    # Combine post caption and comment for analysis
                    combined_text = f"{post.get('caption', '')} {comment.get('text', '')}"
                    
                    # Import here to avoid circular imports
                    from .services import LeadGenerationService
                    service = LeadGenerationService()
                    
                    is_qualified, eng_score, sent_score = service.qualify_lead(
                        user_data, engagement_threshold, combined_text
                    )
                    
                    if is_qualified:
                        user_data.update({
                            'engagement_score': eng_score,
                            'sentiment_score': sent_score
                        })
                        leads.append(user_data)
            
        except Exception as e:
            print(f"Error scraping Instagram profile {page_username}: {e}")
        
        return leads
    
    def scrape_hashtag_interactions(self, hashtag, engagement_threshold):
        """Scrape posts and interactions for a specific hashtag"""
        leads = []
        
        try:
            run_input = {
                "search": hashtag,
                "searchType": "hashtag",
                "searchLimit": 1,
                "resultsType": "posts",
                "resultsLimit": self.max_results_per_request,
            }
            
            run = self.client.actor("apify/instagram-scraper").call(run_input=run_input)
            run = self.wait_for_run_completion(run)
            
            # Process hashtag posts
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                user_data = self.extract_user_data(item, 'instagram')
                
                if not user_data['username']:
                    continue
                
                # Import here to avoid circular imports
                from .services import LeadGenerationService
                service = LeadGenerationService()
                
                is_qualified, eng_score, sent_score = service.qualify_lead(
                    user_data, engagement_threshold, user_data['message']
                )
                
                if is_qualified:
                    user_data.update({
                        'engagement_score': eng_score,
                        'sentiment_score': sent_score
                    })
                    leads.append(user_data)
            
        except Exception as e:
            print(f"Error scraping Instagram hashtag #{hashtag}: {e}")
        
        return leads
    
    def _get_profile_posts(self, username):
        """Get recent posts from an Instagram profile"""
        try:
            run_input = {
                "directUrls": [f"https://www.instagram.com/{username}/"],
                "resultsType": "posts",
                "resultsLimit": 20,
            }
            
            run = self.client.actor("apify/instagram-scraper").call(run_input=run_input)
            run = self.wait_for_run_completion(run)
            
            posts = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                posts.append(item)
            
            return posts
            
        except Exception as e:
            print(f"Error getting posts from Instagram profile {username}: {e}")
            return []
    
    def _get_post_comments(self, post_url):
        """Get comments from a specific Instagram post"""
        try:
            run_input = {
                "directUrls": [post_url],
                "resultsType": "comments",
                "resultsLimit": 50,
            }
            
            run = self.client.actor("apify/instagram-comment-scraper").call(run_input=run_input)
            run = self.wait_for_run_completion(run)
            
            comments = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                comments.append(item)
            
            return comments
            
        except Exception as e:
            print(f"Error getting comments from Instagram post {post_url}: {e}")
            return []
