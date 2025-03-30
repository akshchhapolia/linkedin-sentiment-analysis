import datetime
import random
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download VADER lexicon if not already downloaded
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

def generate_company_reviews(company_name, count=30):
    """Generate realistic user reviews for any company."""
    
    # Determine company characteristics based on name
    company_type = "fintech"  # Default assumption
    
    # Check company name for hints about industry
    company_name_lower = company_name.lower()
    if any(term in company_name_lower for term in ["bank", "finance", "fi", "pay", "money", "wealth", "invest"]):
        company_type = "fintech"
    elif any(term in company_name_lower for term in ["tech", "software", "app", "digital", "ai", "data", "microsoft", "apple", "google"]):
        company_type = "tech"
    elif any(term in company_name_lower for term in ["food", "restaurant", "eat", "kitchen", "meal", "coffee", "cafe", "dining", "starbucks", "pizza", "zomato", "swiggy", "doordash", "uber eats"]):
        company_type = "food"
    elif any(term in company_name_lower for term in ["travel", "trip", "hotel", "flight", "vacation", "booking", "airbnb"]):
        company_type = "travel"
    elif any(term in company_name_lower for term in ["retail", "shop", "store", "market", "mall", "mart", "amazon", "walmart"]):
        company_type = "retail"
    
    # Industry-specific features and issues
    features_by_type = {
        "fintech": [
            "zero forex markup on international transactions",
            "digital savings accounts that are easy to open",
            "FD/RD creation and management",
            "mutual fund investments",
            "user-friendly interface",
            "smart deposit features",
            "responsive customer service",
            "no minimum balance requirements",
            "free ATM withdrawals",
            "instant money transfers",
            "cashback rewards",
            "useful expense tracking",
            "beautiful minimal card design",
            "interest rates better than traditional banks",
            "quick KYC process"
        ],
        "tech": [
            "intuitive user interface",
            "smooth performance even with heavy usage",
            "regular feature updates",
            "cross-platform compatibility",
            "excellent data security measures",
            "responsive support team",
            "great documentation and tutorials",
            "customizable settings",
            "excellent collaboration tools",
            "seamless integration with other tools",
            "advanced AI features",
            "innovative problem-solving approach",
            "simplified workflow automation",
            "powerful analytics dashboard",
            "clean and modern design"
        ],
        "food": [
            "delicious menu options",
            "quick delivery times",
            "fresh ingredients",
            "accommodating dietary restrictions",
            "generous portion sizes",
            "consistent food quality",
            "excellent value for money",
            "friendly service staff",
            "clean and welcoming atmosphere",
            "interesting seasonal specials",
            "authentic flavors",
            "thoughtful presentation",
            "innovative fusion concepts",
            "reliable online ordering system",
            "responsive to customer feedback"
        ],
        "travel": [
            "seamless booking experience",
            "transparent pricing with no hidden fees",
            "detailed destination information",
            "personalized travel recommendations",
            "excellent customer support during trips",
            "flexible cancellation policies",
            "high-quality accommodation options",
            "exclusive travel deals",
            "comprehensive travel insurance",
            "real-time flight tracking",
            "useful travel tips and guides",
            "easy itinerary management",
            "loyalty rewards program",
            "multi-currency support",
            "emergency assistance services"
        ],
        "retail": [
            "high-quality products",
            "competitive pricing",
            "fast shipping options",
            "hassle-free returns policy",
            "excellent customer service",
            "user-friendly website",
            "wide product selection",
            "detailed product descriptions",
            "accurate inventory information",
            "secure payment processing",
            "regular discounts and promotions",
            "loyalty rewards program",
            "personalized recommendations",
            "sustainable packaging",
            "easy order tracking"
        ]
    }
    
    issues_by_type = {
        "fintech": [
            "delayed customer support responses",
            "app crashes occasionally",
            "confusing investment options",
            "limited credit card features",
            "trouble with transactions sometimes",
            "difficulty updating KYC information",
            "international transactions getting declined",
            "limited customer service hours",
            "occasional notification glitches",
            "limited integration with other financial services",
            "high fees for certain premium features",
            "account statement issues",
            "long wait times for customer service",
            "unhelpful customer service representatives",
            "difficulty closing accounts"
        ],
        "tech": [
            "frequent unexplained crashes",
            "confusing user interface",
            "slow performance on older devices",
            "excessive battery drain",
            "intrusive update notifications",
            "inadequate documentation",
            "unresponsive customer support",
            "inconsistent cross-platform experience",
            "excessive permissions required",
            "data privacy concerns",
            "sync issues between devices",
            "limited offline functionality",
            "steep learning curve",
            "missing critical features",
            "buggy latest release"
        ],
        "food": [
            "inconsistent food quality",
            "long wait times for delivery",
            "incorrect orders",
            "limited menu options",
            "overpriced for the quality",
            "small portion sizes",
            "unresponsive customer service",
            "food arriving cold",
            "limited vegetarian/vegan options",
            "unclear allergen information",
            "website/app ordering issues",
            "limited delivery area",
            "poor packaging for delivery",
            "canceled orders without notice",
            "unprofessional delivery staff"
        ],
        "travel": [
            "hidden fees added at checkout",
            "misleading property descriptions",
            "unresponsive customer service",
            "complicated cancellation process",
            "unexpected itinerary changes",
            "inaccurate availability information",
            "poor mobile app experience",
            "payment processing issues",
            "limited destination options",
            "unhelpful in emergency situations",
            "ignored special requests",
            "poor coordination for multi-leg journeys",
            "missing loyalty points after trips",
            "unreliable transfer services",
            "outdated destination information"
        ],
        "retail": [
            "items arriving damaged",
            "long delivery times",
            "poor quality products",
            "difficult return process",
            "unresponsive customer service",
            "website technical issues",
            "incorrect product information",
            "out-of-stock items still available to order",
            "incorrect billing",
            "canceled orders without notification",
            "poor packaging",
            "delivery tracking inaccuracies",
            "unauthorized subscription enrollment",
            "inflated original prices for 'discounts'",
            "misleading product images"
        ]
    }
    
    # Select the appropriate feature and issue lists based on company type
    positive_features = features_by_type.get(company_type, features_by_type["tech"]).copy()
    negative_issues = issues_by_type.get(company_type, issues_by_type["tech"]).copy()
    
    # Store original lists for replenishment
    original_positive_features = positive_features.copy()
    original_negative_issues = negative_issues.copy()
    
    # Common neutral observations that can apply to any industry
    neutral_observations = [
        f"similar features to other {company_type} companies",
        "standard service quality",
        "typical user experience",
        "average industry offerings",
        "usual onboarding process",
        "comparable to competitors",
        "neither outstanding nor poor"
    ]
    
    # Industry-specific templates
    templates_by_type = {
        "fintech": {
            "positive": [
                f"I've been using {company_name} for {{duration}} now, and I'm impressed with their {{feature}}. Definitely recommend for anyone looking to upgrade their banking experience!",
                f"{company_name} has completely transformed how I manage my finances. The {{feature}} is a game-changer!",
                f"Just switched to {company_name} from my traditional bank and I'm loving the {{feature}} and {{feature2}}. Such a refreshing change!",
                f"{company_name}'s {{feature}} is simply outstanding. I've tried other neo-banks but {company_name} stands out for its user experience.",
                f"My experience with {company_name} has been excellent. The {{feature}} works flawlessly, and their customer service is prompt whenever I've needed help."
            ],
            "negative": [
                f"Having issues with {company_name} lately. Their {{issue}} is really frustrating and making me consider switching.",
                f"Not happy with {company_name}'s {{issue}}. Expected better from a modern fintech company.",
                f"{company_name} needs to fix their {{issue}} asap. It's been a problem for {{duration}} now with no resolution.",
                f"Disappointed with {company_name}'s {{issue}}. Customer service hasn't been helpful in resolving this either.",
                f"{company_name} was great initially, but their {{issue}} has become increasingly problematic."
            ],
            "neutral": [
                f"{company_name} offers {{observation}} like most other neo-banks. Works fine for basic banking needs.",
                f"Been using {company_name} for {{duration}}. It has {{observation}}, not particularly impressive but gets the job done.",
                f"{company_name}'s {{observation}} is adequate. Nothing exceptional but no major complaints either."
            ]
        },
        "tech": {
            "positive": [
                f"{company_name}'s platform has the best {{feature}} I've encountered. Makes my workflow so much more efficient!",
                f"After trying several alternatives, {company_name}'s {{feature}} and {{feature2}} have made it my go-to solution.",
                f"I've been using {company_name} for {{duration}} now, and their {{feature}} keeps getting better with each update.",
                f"My team switched to {company_name} last quarter and we've seen significant productivity improvements thanks to the {{feature}}.",
                f"{company_name} has nailed the user experience with their {{feature}}. It's intuitive and powerful at the same time."
            ],
            "negative": [
                f"The latest {company_name} update completely broke the {{issue}}. Had to switch to an alternative temporarily.",
                f"{company_name}'s {{issue}} is becoming a deal-breaker for our team. Looking at alternatives now.",
                f"I want to love {company_name}, but the {{issue}} and {{issue2}} make it hard to justify the cost.",
                f"Been a {company_name} user for {{duration}}, but might switch due to persistent {{issue}} that support won't address.",
                f"{company_name} needs to prioritize fixing their {{issue}} instead of adding new features that nobody asked for."
            ],
            "neutral": [
                f"{company_name} is similar to other tools in this space with {{observation}}. Works for basic needs.",
                f"Used {company_name} for {{duration}}. It's got {{observation}} - nothing special but gets the job done.",
                f"{company_name} vs competitors? They all have their pros and cons. {company_name} has {{observation}}, which works for some workflows."
            ]
        },
        "food": {
            "positive": [
                f"Had the most amazing meal at {company_name} last night! Their {{feature}} exceeded all my expectations.",
                f"{company_name} has become my go-to for dinner. The {{feature}} and {{feature2}} keep me coming back!",
                f"First time ordering from {company_name} and I'm impressed! The {{feature}} was exceptional.",
                f"If you're looking for {{feature}}, {company_name} is unbeatable. Been a regular customer for {{duration}} now.",
                f"{company_name}'s new menu showcasing their {{feature}} is absolutely worth trying. Some of the best food I've had recently!"
            ],
            "negative": [
                f"Disappointed with my recent order from {company_name}. The {{issue}} was a letdown compared to previous experiences.",
                f"Used to love {company_name}, but their {{issue}} has become unacceptable over the past {{duration}}.",
                f"Waited over an hour for my {company_name} delivery only to find {{issue}} when it finally arrived. Not ordering again.",
                f"{company_name} needs to address their {{issue}} and {{issue2}}. Food quality has declined significantly.",
                f"Had a terrible experience at {company_name} yesterday. The {{issue}} was appalling and management didn't seem to care."
            ],
            "neutral": [
                f"{company_name} is average at best. The food has {{observation}} - nothing to rave about but satisfies hunger.",
                f"Tried {company_name} for lunch today. It's got {{observation}} like most places in this price range.",
                f"{company_name} vs other similar restaurants? Pretty comparable with {{observation}}. Depends what you're in the mood for."
            ]
        },
        "travel": {
            "positive": [
                f"Just booked my third trip through {company_name} and I'm always impressed by their {{feature}}!",
                f"{company_name} made planning my vacation so easy with their {{feature}} and {{feature2}}. Highly recommend!",
                f"After a stressful experience with another travel site, {company_name}'s {{feature}} was a breath of fresh air.",
                f"Been using {company_name} for all my travel needs for {{duration}} now. Their {{feature}} is unmatched in the industry.",
                f"My recent trip booked through {company_name} was flawless thanks to their {{feature}}. Will definitely use them again!"
            ],
            "negative": [
                f"Avoid {company_name} at all costs! Their {{issue}} ruined what should have been a relaxing vacation.",
                f"Had the worst experience with {company_name}'s {{issue}} during my recent trip. Still waiting for a resolution {{duration}} later.",
                f"{company_name}'s {{issue}} and {{issue2}} made for a nightmarish travel experience. Never again.",
                f"Warning to fellow travelers: {company_name}'s {{issue}} caused me to miss my connection and their support was useless.",
                f"Been trying to get a refund from {company_name} for {{duration}} due to their {{issue}}. Looking into legal options now."
            ],
            "neutral": [
                f"{company_name} offers {{observation}} like most travel sites. Got me where I needed to go without any special perks.",
                f"Used {company_name} for my business trip. Service was {{observation}} - nothing memorable but no issues either.",
                f"Comparing {company_name} to other travel services - they all offer {{observation}}. Price was the main differentiator for me."
            ]
        },
        "retail": {
            "positive": [
                f"Just received my order from {company_name} and I'm impressed with their {{feature}}! Will definitely shop here again.",
                f"{company_name} has the best {{feature}} I've experienced from an online retailer. Makes shopping so much easier!",
                f"Been a loyal {company_name} customer for {{duration}} because of their {{feature}} and {{feature2}}. Always a pleasant experience.",
                f"My recent purchase from {company_name} arrived earlier than expected and the {{feature}} was outstanding as usual.",
                f"{company_name}'s {{feature}} sets them apart from other retailers. Always my first choice when shopping for this category."
            ],
            "negative": [
                f"Disappointed with my recent {company_name} purchase. The {{issue}} makes me hesitant to order from them again.",
                f"{company_name}'s {{issue}} is frustrating. Had to spend {{duration}} trying to sort out a simple return.",
                f"Warning to potential {company_name} shoppers: their {{issue}} and {{issue2}} make the experience more trouble than it's worth.",
                f"Placed an order with {company_name} over {{duration}} ago and still dealing with their {{issue}}. Shop elsewhere!",
                f"{company_name} has gone downhill lately. Their {{issue}} has become increasingly problematic with each order."
            ],
            "neutral": [
                f"{company_name} is just like most online retailers with {{observation}}. Nothing special but gets the job done.",
                f"Ordered from {company_name} last week. The experience was {{observation}} - reasonable prices and standard delivery times.",
                f"{company_name} vs other similar stores? They all offer {{observation}}. I usually just go with whoever has the best price."
            ]
        }
    }
    
    # Use specific templates if available, otherwise use general ones
    post_templates = templates_by_type.get(company_type, {
        "positive": [
            f"I've been using {company_name} for {{duration}} now, and I'm really impressed with their {{feature}}. Definitely recommend!",
            f"{company_name} has completely transformed my experience. The {{feature}} is a game-changer!",
            f"Just switched to {company_name} and I'm loving the {{feature}} and {{feature2}}. Such a refreshing change!",
            f"{company_name}'s {{feature}} is simply outstanding. I've tried other options but {company_name} stands out.",
            f"My experience with {company_name} has been excellent. The {{feature}} works flawlessly."
        ],
        "negative": [
            f"Having issues with {company_name} lately. Their {{issue}} is really frustrating and making me consider alternatives.",
            f"Not happy with {company_name}'s {{issue}}. Expected better from a modern company.",
            f"{company_name} needs to fix their {{issue}} asap. It's been a problem for {{duration}} now with no resolution.",
            f"Disappointed with {company_name}'s {{issue}}. Customer service hasn't been helpful in resolving this either.",
            f"{company_name} was great initially, but their {{issue}} has become increasingly problematic."
        ],
        "neutral": [
            f"{company_name} offers {{observation}} like most other companies. Works fine for basic needs.",
            f"Been using {company_name} for {{duration}}. It has {{observation}}, not particularly impressive but gets the job done.",
            f"{company_name}'s {{observation}} is adequate. Nothing exceptional but no major complaints either."
        ]
    })
    
    # Time periods
    durations = ["a month", "3 months", "6 months", "over a year", "a few weeks", "several months"]
    
    # Generate posts with sentiment distribution
    # For fintech: 60% negative, 30% positive, 10% neutral
    # For other industries: 50% positive, 40% negative, 10% neutral
    sentiment_distribution = []
    
    if company_type == "fintech":
        # More negative sentiment for fintech
        for _ in range(count):
            rand = random.random()
            if rand < 0.3:
                sentiment_distribution.append("positive")
            elif rand < 0.9:
                sentiment_distribution.append("negative")
            else:
                sentiment_distribution.append("neutral")
    else:
        # More positive sentiment for other industries
        for _ in range(count):
            rand = random.random()
            if rand < 0.5:
                sentiment_distribution.append("positive")
            elif rand < 0.9:
                sentiment_distribution.append("negative")
            else:
                sentiment_distribution.append("neutral")
    
    posts = []
    for sentiment in sentiment_distribution:
        template = random.choice(post_templates[sentiment])
        
        # Replace placeholders with actual content
        post_text = template
        
        if "{duration}" in post_text:
            post_text = post_text.replace("{duration}", random.choice(durations))
            
        if "{feature}" in post_text:
            # Replenish the list if empty
            if not positive_features:
                positive_features = original_positive_features.copy()
            feature = random.choice(positive_features)
            positive_features.remove(feature)  # Avoid repetition
            post_text = post_text.replace("{feature}", feature)
            
        if "{feature2}" in post_text:
            # Replenish the list if empty
            if not positive_features:
                positive_features = original_positive_features.copy()
            feature2 = random.choice(positive_features)
            post_text = post_text.replace("{feature2}", feature2)
            
        if "{issue}" in post_text:
            # Replenish the list if empty
            if not negative_issues:
                negative_issues = original_negative_issues.copy()
            issue = random.choice(negative_issues)
            negative_issues.remove(issue)  # Avoid repetition
            post_text = post_text.replace("{issue}", issue)
            
        if "{issue2}" in post_text:
            # Replenish the list if empty
            if not negative_issues:
                negative_issues = original_negative_issues.copy()
            issue2 = random.choice(negative_issues)
            post_text = post_text.replace("{issue2}", issue2)
            
        if "{observation}" in post_text:
            post_text = post_text.replace("{observation}", random.choice(neutral_observations))
        
        # Generate random dates within last 6 months
        days_ago = random.randint(1, 180)
        post_date = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        # Create post dictionary with proper LinkedIn URL format
        post = {
            "text": post_text,
            "date": post_date,
            "author": f"User_{random.randint(1000, 9999)}",
            "url": f"https://www.linkedin.com/posts/user-name_{random.randint(10000, 99999)}-activity-{random.randint(6800000000000000000, 6999999999999999999)}",
            "sentiment": sentiment  # We know the actual sentiment for generated data
        }
        
        posts.append(post)
    
    # Add some specific realistic posts about the company
    specific_posts = []
    
    # Industry-specific realistic posts
    if company_type == "fintech":
        specific_posts = [
            {
                "text": f"{company_name}'s international transactions are amazing - zero forex markup saved me thousands on my recent trip abroad!",
                "date": (datetime.datetime.now() - datetime.timedelta(days=15)).strftime("%Y-%m-%d"),
                "author": "TravelEnthusiast_3456",
                "url": f"https://www.linkedin.com/posts/travel-enthusiast-3456_{random.randint(10000, 99999)}-activity-{random.randint(6800000000000000000, 6999999999999999999)}",
                "sentiment": "positive"
            },
            {
                "text": f"The new {company_name} app update is causing crashes every time I try to check my investments. Please fix this asap @{company_name}!",
                "date": (datetime.datetime.now() - datetime.timedelta(days=3)).strftime("%Y-%m-%d"),
                "author": "TechSavvy_6789",
                "url": f"https://www.linkedin.com/posts/tech-savvy-6789_{random.randint(10000, 99999)}-activity-{random.randint(6800000000000000000, 6999999999999999999)}",
                "sentiment": "negative"
            }
        ]
    elif company_type == "tech":
        specific_posts = [
            {
                "text": f"Just implemented {company_name}'s API across our enterprise systems. The documentation is so comprehensive it made integration a breeze!",
                "date": (datetime.datetime.now() - datetime.timedelta(days=12)).strftime("%Y-%m-%d"),
                "author": "DevTeamLead_8765",
                "url": f"https://www.linkedin.com/posts/dev-team-lead-8765_{random.randint(10000, 99999)}-activity-{random.randint(6800000000000000000, 6999999999999999999)}",
                "sentiment": "positive"
            },
            {
                "text": f"Week 3 of trying to get {company_name}'s customer support to help with our enterprise account issues. Still no resolution. This is unacceptable for a mission-critical service.",
                "date": (datetime.datetime.now() - datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
                "author": "FrustratedCTO_2468",
                "url": f"https://www.linkedin.com/posts/frustrated-cto-2468_{random.randint(10000, 99999)}-activity-{random.randint(6800000000000000000, 6999999999999999999)}",
                "sentiment": "negative"
            }
        ]
    elif company_type == "food":
        specific_posts = [
            {
                "text": f"Had the most incredible dining experience at {company_name} last night! The chef's tasting menu was innovative and perfectly executed. Worth every penny!",
                "date": (datetime.datetime.now() - datetime.timedelta(days=8)).strftime("%Y-%m-%d"),
                "author": "FoodCritic_7890",
                "url": f"https://www.linkedin.com/posts/food-critic-7890_{random.randint(10000, 99999)}-activity-{random.randint(6800000000000000000, 6999999999999999999)}",
                "sentiment": "positive"
            },
            {
                "text": f"Ordered delivery from {company_name} for a client lunch. Food arrived over an hour late and cold. Extremely embarrassing professional situation. Won't be using their service again.",
                "date": (datetime.datetime.now() - datetime.timedelta(days=11)).strftime("%Y-%m-%d"),
                "author": "EventPlanner_1357",
                "url": f"https://www.linkedin.com/posts/event-planner-1357_{random.randint(10000, 99999)}-activity-{random.randint(6800000000000000000, 6999999999999999999)}",
                "sentiment": "negative"
            }
        ]
    elif company_type == "travel":
        specific_posts = [
            {
                "text": f"Just returned from a trip booked through {company_name}. Their attention to detail made everything seamless - from flight upgrades to personalized excursions. 10/10 would recommend!",
                "date": (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d"),
                "author": "GlobeTrotter_9753",
                "url": f"https://www.linkedin.com/posts/globe-trotter-9753_{random.randint(10000, 99999)}-activity-{random.randint(6800000000000000000, 6999999999999999999)}",
                "sentiment": "positive"
            },
            {
                "text": f"Stranded at the airport after {company_name} canceled our reservation without notice. No rebooking assistance, no refund, and customer service keeps putting me on hold. Vacation ruined.",
                "date": (datetime.datetime.now() - datetime.timedelta(days=4)).strftime("%Y-%m-%d"),
                "author": "DisappointedTraveler_4826",
                "url": f"https://www.linkedin.com/posts/disappointed-traveler-4826_{random.randint(10000, 99999)}-activity-{random.randint(6800000000000000000, 6999999999999999999)}",
                "sentiment": "negative"
            }
        ]
    elif company_type == "retail":
        specific_posts = [
            {
                "text": f"The customer service at {company_name} is exceptional! Had an issue with my order and they not only resolved it immediately but also sent a complimentary gift as an apology. This is how you build customer loyalty!",
                "date": (datetime.datetime.now() - datetime.timedelta(days=9)).strftime("%Y-%m-%d"),
                "author": "SatisfiedShopper_6543",
                "url": f"https://www.linkedin.com/posts/satisfied-shopper-6543_{random.randint(10000, 99999)}-activity-{random.randint(6800000000000000000, 6999999999999999999)}",
                "sentiment": "positive"
            },
            {
                "text": f"Ordered a high-value item from {company_name} during their sale. They canceled my order two weeks later saying it was 'out of stock' then immediately relisted it at a higher price. Blatant bait and switch tactics.",
                "date": (datetime.datetime.now() - datetime.timedelta(days=6)).strftime("%Y-%m-%d"),
                "author": "ConsumerAdvocate_2581",
                "url": f"https://www.linkedin.com/posts/consumer-advocate-2581_{random.randint(10000, 99999)}-activity-{random.randint(6800000000000000000, 6999999999999999999)}",
                "sentiment": "negative"
            }
        ]
    
    # Create generic positive and negative posts if no industry-specific posts
    if not specific_posts:
        specific_posts = [
            {
                "text": f"I've had consistently positive experiences with {company_name}. Their attention to customer satisfaction really sets them apart from competitors.",
                "date": (datetime.datetime.now() - datetime.timedelta(days=14)).strftime("%Y-%m-%d"),
                "author": "SatisfiedCustomer_4321",
                "url": f"https://www.linkedin.com/posts/satisfied-customer-4321_{random.randint(10000, 99999)}-activity-{random.randint(6800000000000000000, 6999999999999999999)}",
                "sentiment": "positive"
            },
            {
                "text": f"Really disappointed with my recent experience with {company_name}. Multiple issues and customer support was unresponsive. Expected much better.",
                "date": (datetime.datetime.now() - datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
                "author": "DisappointedUser_8765",
                "url": f"https://www.linkedin.com/posts/disappointed-user-8765_{random.randint(10000, 99999)}-activity-{random.randint(6800000000000000000, 6999999999999999999)}",
                "sentiment": "negative"
            }
        ]
    
    # Ensure the post list is refreshed for each call to the function
    # Replace some of the generated posts with specific ones
    for specific_post in specific_posts:
        if len(posts) > len(specific_posts):
            posts[random.randint(0, len(posts)-1)] = specific_post
        else:
            posts.append(specific_post)
    
    # Limit to the requested count
    if len(posts) > count:
        posts = posts[:count]
    
    return posts

def analyze_sentiment(posts):
    """Analyze sentiment of posts using VADER."""
    analyzer = SentimentIntensityAnalyzer()
    
    analyzed_posts = []
    for post in posts:
        # If post already has sentiment assigned (from our mock data)
        if "sentiment" in post:
            # Still run the analyzer to get the compound score
            sentiment_scores = analyzer.polarity_scores(post["text"])
            post["compound_score"] = sentiment_scores["compound"]
            analyzed_posts.append(post)
            continue
            
        sentiment_scores = analyzer.polarity_scores(post["text"])
        compound_score = sentiment_scores["compound"]
        
        # Determine sentiment category
        if compound_score >= 0.05:
            sentiment = "positive"
        elif compound_score <= -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        post["sentiment"] = sentiment
        post["compound_score"] = compound_score
        analyzed_posts.append(post)
    
    return analyzed_posts

def generate_report(company_name, analyzed_posts, newest_date="Unknown", oldest_date="Unknown"):
    """Generate a sentiment analysis report."""
    # Count sentiments
    sentiments = {"positive": 0, "neutral": 0, "negative": 0}
    for post in analyzed_posts:
        sentiments[post["sentiment"]] += 1
    
    total_posts = len(analyzed_posts)
    
    # Sort posts by compound score
    sorted_posts = sorted(analyzed_posts, key=lambda x: x.get("compound_score", 0), reverse=True)
    most_positive = sorted_posts[:3]  # Top 3 positive posts
    most_negative = sorted_posts[-3:] if len(sorted_posts) >= 3 else sorted_posts[-len(sorted_posts):]  # Bottom 3 negative posts
    
    # Determine company type based on name
    company_type = "fintech"  # Default assumption
    company_name_lower = company_name.lower()
    
    if any(term in company_name_lower for term in ["bank", "finance", "fi", "pay", "money", "wealth", "invest"]):
        company_type = "fintech"
    elif any(term in company_name_lower for term in ["tech", "software", "app", "digital", "ai", "data", "microsoft", "apple", "google"]):
        company_type = "tech"
    elif any(term in company_name_lower for term in ["food", "restaurant", "eat", "kitchen", "meal", "coffee", "cafe", "dining", "starbucks", "pizza", "zomato", "swiggy", "doordash", "uber eats"]):
        company_type = "food"
    elif any(term in company_name_lower for term in ["travel", "trip", "hotel", "flight", "vacation", "booking", "airbnb"]):
        company_type = "travel"
    elif any(term in company_name_lower for term in ["retail", "shop", "store", "market", "mall", "mart", "amazon", "walmart"]):
        company_type = "retail"
    
    print(f"DEBUG: Detected company_type='{company_type}' for company_name='{company_name}'")
    
    # Create time-based analysis
    from collections import defaultdict
    import datetime as dt
    
    # Group posts by month for trend analysis
    month_sentiments = defaultdict(lambda: {"positive": 0, "neutral": 0, "negative": 0, "total": 0})
    
    for post in analyzed_posts:
        # Track sentiment by month
        try:
            post_date = dt.datetime.strptime(post["date"], "%Y-%m-%d")
            month_key = f"{post_date.year}-{post_date.month:02d}"
            month_sentiments[month_key][post["sentiment"]] += 1
            month_sentiments[month_key]["total"] += 1
        except:
            pass  # Skip if date parsing fails
    
    # Generate actionable insights based on industry type and sentiment analysis
    # Customize the recommendations based on company type
    if company_type == "fintech":
        strengths = "financial services" if sentiments["positive"] > sentiments["negative"] else "areas that need improvement"
        recommendations = [
            f"Highlight {company_name}'s positive customer experiences in marketing materials, particularly around user interface and customer service.",
            f"Consider addressing app stability and transaction processing issues which were mentioned in negative reviews.",
            f"Develop more transparent communication regarding fees and charges to address customer concerns."
        ]
    elif company_type == "tech":
        strengths = "technological solutions" if sentiments["positive"] > sentiments["negative"] else "technical aspects that need improvement"
        recommendations = [
            f"Showcase {company_name}'s product reliability and performance in marketing materials.",
            f"Consider improving documentation and user guides based on customer feedback.",
            f"Address customer support response times and technical issue resolution processes."
        ]
    elif company_type == "food":
        strengths = "culinary offerings" if sentiments["positive"] > sentiments["negative"] else "dining aspects that need improvement"
        recommendations = [
            f"Feature {company_name}'s food quality and customer favorites in marketing campaigns.",
            f"Review delivery processes to address timeliness concerns mentioned in reviews.",
            f"Consider expanding menu options based on customer preferences and feedback."
        ]
    elif company_type == "travel":
        strengths = "travel services" if sentiments["positive"] > sentiments["negative"] else "travel aspects that need improvement"
        recommendations = [
            f"Highlight {company_name}'s seamless booking experience and customer satisfaction in promotions.",
            f"Address transparency issues around pricing and hidden fees mentioned in reviews.",
            f"Improve customer communication during travel disruptions and reservation changes."
        ]
    elif company_type == "retail":
        strengths = "retail offerings" if sentiments["positive"] > sentiments["negative"] else "retail aspects that need improvement"
        recommendations = [
            f"Feature {company_name}'s product quality and customer service excellence in advertising.",
            f"Review shipping and delivery processes to address delays mentioned in reviews.",
            f"Improve return processes and policy communication based on customer feedback."
        ]
    else:
        strengths = "products and services" if sentiments["positive"] > sentiments["negative"] else "areas that need improvement"
        recommendations = [
            f"Highlight {company_name}'s strengths in customer testimonials and marketing materials.",
            f"Address the most commonly mentioned issues in negative feedback.",
            f"Develop a response strategy for addressing customer concerns in public forums."
        ]
    
    # Build the report
    report = f"""
LINKEDIN SENTIMENT ANALYSIS REPORT: {company_name}
Date: {dt.datetime.now().strftime("%Y-%m-%d")}
Period Analyzed: {oldest_date} to {newest_date}

SUMMARY
=======
Total posts analyzed: {total_posts}
Positive posts: {sentiments["positive"]} ({sentiments["positive"]/total_posts*100:.1f}%)
Neutral posts: {sentiments["neutral"]} ({sentiments["neutral"]/total_posts*100:.1f}%)
Negative posts: {sentiments["negative"]} ({sentiments["negative"]/total_posts*100:.1f}%)

SENTIMENT TREND
==============
"""
    
    # Add trend data if available
    if month_sentiments:
        for month in sorted(month_sentiments.keys()):
            total_month = month_sentiments[month]["total"]
            pos_pct = month_sentiments[month]["positive"] / total_month * 100 if total_month > 0 else 0
            neu_pct = month_sentiments[month]["neutral"] / total_month * 100 if total_month > 0 else 0
            neg_pct = month_sentiments[month]["negative"] / total_month * 100 if total_month > 0 else 0
            
            report += f"{month}: {total_month} posts - Positive: {pos_pct:.1f}%, Neutral: {neu_pct:.1f}%, Negative: {neg_pct:.1f}%\n"
    
    # Add actionable insights
    report += f"""
ACTIONABLE INSIGHTS
==================
Based on the sentiment analysis of LinkedIn posts about {company_name}, we recommend:

"""
    
    for i, recommendation in enumerate(recommendations, 1):
        report += f"{i}. {recommendation}\n"
    
    # Add sample posts
    report += f"""
SAMPLE POSTS
===========

Most Positive:
"""
    
    for i, post in enumerate(most_positive, 1):
        report += f"\n{i}. Score: {post.get('compound_score', 0):.2f} | Date: {post.get('date', 'Unknown')} | Author: {post.get('author', 'Unknown')}\n"
        report += f"   {post.get('text', '')}\n"
        report += f"   URL: {post.get('url', '')}\n"
    
    report += f"\nMost Negative:"
    
    for i, post in enumerate(reversed(most_negative), 1):
        report += f"\n{i}. Score: {post.get('compound_score', 0):.2f} | Date: {post.get('date', 'Unknown')} | Author: {post.get('author', 'Unknown')}\n"
        report += f"   {post.get('text', '')}\n"
        report += f"   URL: {post.get('url', '')}\n"
    
    report += f"""
CONCLUSION
==========
This report provides insights based on {total_posts} LinkedIn posts about {company_name}. The overall sentiment is """ 
    
    if sentiments["positive"] > sentiments["negative"] + sentiments["neutral"]:
        report += "predominantly positive. "
    elif sentiments["negative"] > sentiments["positive"] + sentiments["neutral"]:
        report += "predominantly negative. "
    else:
        report += "mixed. "
        
    report += f"We recommend focusing on the identified {strengths} to guide marketing strategy and product improvements."
    
    return report

def main():
    """Run a demo of the sentiment analysis."""
    # Generate sample company reviews
    company_name = "Demo Company"
    count = 30
    
    print(f"Generating {count} sample reviews for {company_name}...")
    posts = generate_company_reviews(company_name, count)
    
    print("Analyzing sentiment...")
    analyzed_posts = analyze_sentiment(posts)
    
    print("Generating report...")
    report = generate_report(company_name, analyzed_posts)
    
    # Save report to file
    report_filename = f"{company_name.replace(' ', '_')}_sentiment_report.txt"
    with open(report_filename, "w") as f:
        f.write(report)
    
    print(f"Report saved to {report_filename}")
    
if __name__ == "__main__":
    main() 