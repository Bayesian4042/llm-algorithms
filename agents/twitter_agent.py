from playwright.sync_api import sync_playwright
import time
import logging
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_tweet_id(url):
    """Extract tweet ID from URL"""
    try:
        path = urlparse(url).path
        return path.split('/')[-1]
    except:
        return None

def scrape_replies(page, tweet_url, original_tab):
    """Scrape replies for a specific tweet in a new tab"""
    try:
        logger.info(f"Scraping replies from: {tweet_url}")
        
        # Open tweet in new tab
        new_page = page.context.new_page()
        new_page.goto(tweet_url)
        new_page.wait_for_selector('article', timeout=10000)
        time.sleep(2)  # Wait for replies to load
        
        replies = []
        replies_seen = set()
        scroll_count = 0
        max_reply_scrolls = 2  # Reduced for faster processing
        
        while scroll_count < max_reply_scrolls:
            reply_elements = new_page.query_selector_all('article[data-testid="tweet"]')
            
            for reply in reply_elements[1:]:  # Skip the first article as it's the original tweet
                try:
                    reply_text = reply.query_selector('div[data-testid="tweetText"]')
                    if reply_text:
                        text = reply_text.inner_text()
                        
                        if text not in replies_seen:
                            replies_seen.add(text)
                            
                            # Get reply timestamp
                            time_element = reply.query_selector('time')
                            timestamp = time_element.get_attribute('datetime') if time_element else None
                            
                            # Get username of reply author
                            username_element = reply.query_selector('div[data-testid="User-Name"] span')
                            username = username_element.inner_text() if username_element else None
                            
                            replies.append({
                                'text': text,
                                'timestamp': timestamp,
                                'username': username
                            })
                            
                except Exception as e:
                    logger.error(f"Error processing reply: {e}")
                    continue
            
            new_page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
            scroll_count += 1
            
        logger.info(f"Found {len(replies)} replies for tweet")
        new_page.close()  # Close the replies tab
        return replies
        
    except Exception as e:
        logger.error(f"Error scraping replies: {e}")
        if 'new_page' in locals():
            new_page.close()
        return []

def scrape_twitter_cashtags(username, cashtag):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ]
        )
        
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        context.set_extra_http_headers({
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        })
        
        page = context.new_page()
        
        logger.info("Opening Twitter. Please log in manually...")
        page.goto('https://twitter.com')
        
        input("Press Enter after you've logged in to Twitter...")
        logger.info("Continuing with scraping...")
        
        # Use advanced search to get more relevant results
        search_url = f"https://twitter.com/search?q={cashtag}%20-filter%3Areplies&src=typed_query&f=live"
        logger.info(f"Navigating to: {search_url}")
        page.goto(search_url)
        
        # Wait for content to load
        page.wait_for_selector('article', timeout=10000)
        
        tweets_seen = set()
        tweet_ids_seen = set()
        results = []
        scroll_count = 0
        max_scrolls = 5

        while scroll_count < max_scrolls:
            logger.info(f"Scroll iteration {scroll_count + 1}/{max_scrolls}")
            
            # Wait for tweets to load
            page.wait_for_selector('article', timeout=10000)
            tweets = page.query_selector_all('article[data-testid="tweet"]')
            logger.info(f"Found {len(tweets)} tweets on current page")
            
            for tweet in tweets:
                try:
                    # Get tweet text
                    text_element = tweet.query_selector('div[data-testid="tweetText"]')
                    if not text_element:
                        continue
                        
                    text = text_element.inner_text()
                    
                    # Get tweet URL
                    tweet_link = tweet.query_selector('a[href*="/status/"]')
                    if not tweet_link:
                        continue
                        
                    tweet_url = 'https://twitter.com' + tweet_link.get_attribute('href')
                    tweet_id = extract_tweet_id(tweet_url)
                    
                    # Skip if we've seen this tweet
                    if tweet_id in tweet_ids_seen:
                        continue
                        
                    tweet_ids_seen.add(tweet_id)
                    
                    # Get timestamp
                    time_element = tweet.query_selector('time')
                    timestamp = time_element.get_attribute('datetime') if time_element else None
                    
                    # Get author username
                    username_element = tweet.query_selector('div[data-testid="User-Name"] span')
                    author = username_element.inner_text() if username_element else None
                    
                    # Scrape replies
                    replies = scrape_replies(page, tweet_url, page)
                    
                    tweet_data = {
                        'text': text,
                        'timestamp': timestamp,
                        'url': tweet_url,
                        'author': author,
                        'replies': replies
                    }
                    
                    results.append(tweet_data)
                    logger.info(f"Added tweet from {author}: {text[:50]}...")
                
                except Exception as e:
                    logger.error(f"Error processing tweet: {e}")
                    continue
            
            # Scroll down
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            
            # Check if we've reached the end of the feed
            old_height = page.evaluate("document.body.scrollHeight")
            page.wait_for_timeout(2000)  # Wait for potential new content
            new_height = page.evaluate("document.body.scrollHeight")
            
            if old_height == new_height and scroll_count > 0:
                logger.info("Reached end of feed")
                break
                
            scroll_count += 1
        
        logger.info(f"Scraping complete. Found {len(results)} unique tweets.")
        return results

def main():
    username = "ga89qin"
    cashtag = "$UBER"
    
    tweets = scrape_twitter_cashtags(username, cashtag)
    
    if tweets:
        print(f"\nFound {len(tweets)} tweets with {cashtag}")
        for tweet in tweets:
            print("\nAuthor:", tweet['author'])
            print("Timestamp:", tweet['timestamp'])
            print("Text:", tweet['text'])
            print("URL:", tweet['url'])
            print("\nReplies:")
            for reply in tweet['replies']:
                print(f"\n  Username: {reply['username']}")
                print(f"  Timestamp: {reply['timestamp']}")
                print(f"  Text: {reply['text']}")
            print("-" * 50)
    else:
        print("No tweets were found or an error occurred.")

if __name__ == "__main__":
    main()