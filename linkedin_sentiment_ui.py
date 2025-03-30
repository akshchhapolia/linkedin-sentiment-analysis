import flask
from flask import Flask, render_template, request, jsonify
import os
import datetime
import json

# Import our modules
from linkedin_sentiment_analysis import analyze_sentiment, generate_report, generate_company_reviews
from linkedin_scraper import scrape_linkedin_for_company

app = Flask(__name__, template_folder='templates')

# Add the datetime.now function to templates
@app.context_processor
def inject_now():
    return {'now': datetime.datetime.now}

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Generate sentiment analysis report based on form data and real LinkedIn scraping."""
    company_name = request.form.get('company_name', 'Company')
    post_count = int(request.form.get('post_count', 30))
    
    # First attempt to scrape real LinkedIn data for the company
    try:
        # This will try to scrape LinkedIn, and fall back to mock data if needed
        posts, is_mock_data = scrape_linkedin_for_company(company_name, post_count, use_mock_data=False)
        data_source = "LinkedIn" if not is_mock_data else "generated mock data"
    except Exception as e:
        # If anything goes wrong, fall back to mock data
        posts = generate_company_reviews(company_name, post_count)
        data_source = "generated mock data (scraping failed)"
    
    # Sort posts by date to find newest and oldest
    sorted_by_date = sorted(posts, key=lambda x: x.get("date", ""), reverse=True)
    newest_date = sorted_by_date[0]["date"] if sorted_by_date else "Unknown"
    oldest_date = sorted_by_date[-1]["date"] if sorted_by_date else "Unknown"
    
    # Analyze sentiment
    analyzed_posts = analyze_sentiment(posts)
    
    # Generate report
    report = generate_report(company_name, analyzed_posts, newest_date, oldest_date)
    
    # Count sentiments
    sentiments = {"positive": 0, "neutral": 0, "negative": 0}
    for post in analyzed_posts:
        sentiments[post["sentiment"]] += 1
    
    # Prepare data for charts
    chart_data = {
        'sentiment_distribution': {
            'labels': ['Positive', 'Neutral', 'Negative'],
            'values': [sentiments['positive'], sentiments['neutral'], sentiments['negative']]
        }
    }
    
    # Prepare monthly trend data if available
    from collections import defaultdict
    import datetime as dt
    
    month_sentiments = defaultdict(lambda: {"positive": 0, "neutral": 0, "negative": 0, "total": 0})
    for post in analyzed_posts:
        try:
            post_date = dt.datetime.strptime(post["date"], "%Y-%m-%d")
            month_key = f"{post_date.year}-{post_date.month:02d}"
            month_sentiments[month_key][post["sentiment"]] += 1
            month_sentiments[month_key]["total"] += 1
        except:
            pass  # Skip if date parsing fails
    
    # Convert to chart format
    months = sorted(month_sentiments.keys())
    trend_data = {
        'labels': months,
        'positive': [month_sentiments[m]['positive'] for m in months],
        'neutral': [month_sentiments[m]['neutral'] for m in months],
        'negative': [month_sentiments[m]['negative'] for m in months]
    }
    
    chart_data['sentiment_trend'] = trend_data
    
    # Extract top features and issues
    from collections import Counter
    
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
    
    # Industry-specific feature and issue extraction
    positive_features_mentioned = []
    negative_issues_mentioned = []
    
    # Define keywords for different industries
    feature_keywords = {
        "fintech": {
            "zero forex markup": ["forex", "international", "currency", "exchange rate"],
            "smart deposit features": ["smart deposit", "savings", "interest", "fd", "rd"],
            "user interface": ["interface", "ui", "ux", "user experience", "design"],
            "customer service": ["customer service", "support", "help", "assistance"],
            "ATM benefits": ["atm", "withdraw", "cash"],
            "interest rates": ["interest", "rate", "return"],
            "quick KYC process": ["kyc", "verification", "onboarding"]
        },
        "tech": {
            "user interface": ["interface", "ui", "ux", "user experience", "design"],
            "performance": ["fast", "performance", "speed", "responsive"],
            "feature updates": ["update", "feature", "new"],
            "cross-platform": ["platform", "cross-platform", "device"],
            "data security": ["security", "privacy", "data", "encryption"],
            "customer support": ["support", "help", "service", "assistance"],
            "documentation": ["documentation", "guide", "tutorial"]
        },
        "food": {
            "taste quality": ["delicious", "tasty", "flavor", "taste"],
            "delivery speed": ["delivery", "quick", "fast", "on time"],
            "freshness": ["fresh", "quality", "ingredients"],
            "value for money": ["price", "value", "worth", "affordable"],
            "portion size": ["portion", "size", "quantity", "amount"],
            "menu variety": ["menu", "variety", "options", "selection"],
            "customer service": ["service", "staff", "waiter", "waitress"]
        },
        "travel": {
            "booking experience": ["booking", "reservation", "easy"],
            "pricing transparency": ["price", "fee", "transparent", "hidden"],
            "customer support": ["support", "service", "help", "assistance"],
            "accommodation quality": ["hotel", "stay", "room", "accommodation"],
            "cancellation policy": ["cancel", "refund", "policy", "flexible"],
            "loyalty program": ["loyalty", "rewards", "points", "miles"],
            "travel planning": ["planning", "itinerary", "schedule"]
        },
        "retail": {
            "product quality": ["quality", "product", "well-made", "durable"],
            "shipping speed": ["shipping", "delivery", "fast", "quick"],
            "return policy": ["return", "refund", "exchange", "policy"],
            "customer service": ["service", "support", "help", "assistance"],
            "website usability": ["website", "site", "online", "interface"],
            "product selection": ["selection", "variety", "range", "options"],
            "pricing": ["price", "affordable", "value", "discount"]
        }
    }
    
    issue_keywords = {
        "fintech": {
            "customer service": ["customer service", "support", "wait time", "unresponsive"],
            "app stability": ["crash", "bug", "freeze", "not working", "issue", "problem"],
            "KYC process": ["kyc", "verification", "document", "reject"],
            "transaction issues": ["transaction", "payment", "fail", "error", "decline"],
            "notification system": ["notification", "alert", "notify", "miss"]
        },
        "tech": {
            "app crashes": ["crash", "freeze", "unresponsive", "hang"],
            "poor performance": ["slow", "lag", "performance", "battery"],
            "missing features": ["missing", "lack", "need", "without"],
            "poor support": ["support", "service", "help", "unresponsive"],
            "user interface issues": ["confusing", "complex", "difficult", "hard to use"]
        },
        "food": {
            "late delivery": ["late", "slow", "delay", "wait"],
            "incorrect orders": ["wrong", "mistake", "incorrect", "missing"],
            "food quality": ["cold", "stale", "quality", "bad", "taste"],
            "high prices": ["expensive", "overpriced", "cost", "price"],
            "small portions": ["small", "tiny", "portion", "size"]
        },
        "travel": {
            "hidden fees": ["hidden", "fee", "extra", "charge", "unexpected"],
            "cancellation issues": ["cancel", "refund", "policy", "difficult"],
            "poor customer service": ["service", "support", "unhelpful", "unresponsive"],
            "inaccurate listings": ["inaccurate", "misleading", "not as advertised", "different"],
            "booking problems": ["booking", "reservation", "problem", "error", "mistake"]
        },
        "retail": {
            "shipping delays": ["delay", "late", "shipping", "delivery"],
            "product quality": ["quality", "poor", "cheap", "break", "damage"],
            "customer service": ["service", "support", "unhelpful", "unresponsive"],
            "return difficulties": ["return", "refund", "difficult", "policy", "hassle"],
            "website issues": ["website", "site", "error", "crash", "problem"]
        }
    }
    
    # Extract features and issues based on company type
    current_feature_keywords = feature_keywords.get(company_type, feature_keywords["tech"])
    current_issue_keywords = issue_keywords.get(company_type, issue_keywords["tech"])
    
    for post in analyzed_posts:
        text = post["text"].lower()
        
        if post["sentiment"] == "positive":
            for feature, keywords in current_feature_keywords.items():
                if any(keyword in text for keyword in keywords):
                    positive_features_mentioned.append(feature)
        
        elif post["sentiment"] == "negative":
            for issue, keywords in current_issue_keywords.items():
                if any(keyword in text for keyword in keywords):
                    negative_issues_mentioned.append(issue)
    
    # Count occurrences
    positive_counts = Counter(positive_features_mentioned)
    negative_counts = Counter(negative_issues_mentioned)
    
    # Get top features/issues
    top_positive = positive_counts.most_common(3)
    top_negative = negative_counts.most_common(3)
    
    # Handle empty results
    if not top_positive:
        top_positive = [("No specific features mentioned", 0)]
    
    if not top_negative:
        top_negative = [("No specific issues mentioned", 0)]
    
    chart_data['top_features'] = {
        'labels': [feature for feature, _ in top_positive],
        'values': [count for _, count in top_positive]
    }
    
    chart_data['top_issues'] = {
        'labels': [issue for issue, _ in top_negative],
        'values': [count for _, count in top_negative]
    }
    
    # Sort posts for samples
    sorted_posts = sorted(analyzed_posts, key=lambda x: x.get("compound_score", 0), reverse=True)
    most_positive = sorted_posts[:3]
    most_negative = sorted_posts[-3:] if len(sorted_posts) >= 3 else sorted_posts[-len(sorted_posts):]
    
    sample_posts = {
        'positive': most_positive,
        'negative': list(reversed(most_negative))
    }
    
    # Generate priority areas based on company type and negative issues
    priority_areas = []
    
    if company_type == "fintech":
        priority_areas = [
            {
                "icon": "bi-headset",
                "title": "Customer Service Enhancement",
                "items": [
                    "Implement 24/7 customer support or at least extended hours",
                    "Improve response time to under 24 hours for all queries",
                    "Better train support staff on common technical issues",
                    "Add more support channels like WhatsApp or in-app chat"
                ]
            },
            {
                "icon": "bi-phone",
                "title": "Technical Reliability",
                "items": [
                    "Comprehensive quality assurance before app updates",
                    "Reduce app crashes through improved error handling",
                    "Simplify the user interface in areas causing confusion",
                    "Implement better offline functionality for basic features"
                ]
            },
            {
                "icon": "bi-credit-card",
                "title": "Transaction System Improvements",
                "items": [
                    "Audit and fix the transaction processing pipeline",
                    "Provide clearer error messages for failed transactions",
                    "Implement real-time transaction status updates",
                    "Create a simplified dispute resolution process"
                ]
            }
        ]
    elif company_type == "tech":
        priority_areas = [
            {
                "icon": "bi-speedometer",
                "title": "Performance Optimization",
                "items": [
                    "Improve application speed and responsiveness",
                    "Reduce resource usage and battery consumption",
                    "Optimize for low-end devices",
                    "Implement better caching mechanisms"
                ]
            },
            {
                "icon": "bi-headset",
                "title": "Customer Support Improvements",
                "items": [
                    "Expand technical support availability",
                    "Develop better knowledge base and self-help resources",
                    "Improve response times for technical issues",
                    "Provide clear escalation paths for complex problems"
                ]
            },
            {
                "icon": "bi-shield-check",
                "title": "Reliability and Security",
                "items": [
                    "Enhance error handling and crash reporting",
                    "Improve data security and privacy controls",
                    "Implement more robust backup and recovery options",
                    "Conduct regular security audits and updates"
                ]
            }
        ]
    elif company_type == "food":
        priority_areas = [
            {
                "icon": "bi-stopwatch",
                "title": "Delivery Experience",
                "items": [
                    "Improve delivery time accuracy and tracking",
                    "Ensure food arrives at the optimal temperature",
                    "Enhance packaging to maintain food quality",
                    "Implement better delivery staff training"
                ]
            },
            {
                "icon": "bi-egg-fried",
                "title": "Food Quality Consistency",
                "items": [
                    "Implement stricter quality control measures",
                    "Maintain consistency across all locations",
                    "Source higher quality ingredients",
                    "Regular review of food preparation processes"
                ]
            },
            {
                "icon": "bi-currency-dollar",
                "title": "Value Optimization",
                "items": [
                    "Review pricing strategies",
                    "Introduce more value meal options",
                    "Enhance portion size consistency",
                    "Develop better loyalty and rewards programs"
                ]
            }
        ]
    elif company_type == "travel":
        priority_areas = [
            {
                "icon": "bi-info-circle",
                "title": "Transparency Improvements",
                "items": [
                    "Clear disclosure of all fees upfront",
                    "Accurate descriptions of accommodations and services",
                    "Better communication about changes or disruptions",
                    "Detailed information about cancellation policies"
                ]
            },
            {
                "icon": "bi-headset",
                "title": "Customer Support Enhancements",
                "items": [
                    "24/7 support availability for travelers",
                    "Better emergency assistance protocols",
                    "Multilingual support options",
                    "Improved response times for urgent issues"
                ]
            },
            {
                "icon": "bi-arrow-repeat",
                "title": "Booking Process Refinement",
                "items": [
                    "Streamline the reservation process",
                    "Implement better error checking for bookings",
                    "Provide more flexible modification options",
                    "Enhance the user experience on mobile devices"
                ]
            }
        ]
    elif company_type == "retail":
        priority_areas = [
            {
                "icon": "bi-truck",
                "title": "Shipping and Delivery",
                "items": [
                    "Improve delivery time accuracy",
                    "Enhance package tracking capabilities",
                    "Implement better handling procedures to reduce damage",
                    "Expand delivery options and timeframes"
                ]
            },
            {
                "icon": "bi-arrow-counterclockwise",
                "title": "Return Process Simplification",
                "items": [
                    "Streamline the return authorization process",
                    "Provide clearer return instructions",
                    "Offer more convenient return options",
                    "Faster processing of refunds"
                ]
            },
            {
                "icon": "bi-headset",
                "title": "Customer Service Improvement",
                "items": [
                    "Reduce response times for customer inquiries",
                    "Better training for service representatives",
                    "Implement more contact channels",
                    "Improve issue resolution processes"
                ]
            }
        ]
    else:
        # Generic priority areas for any other company type
        priority_areas = [
            {
                "icon": "bi-headset",
                "title": "Customer Experience Enhancement",
                "items": [
                    "Improve response times for customer inquiries",
                    "Enhance training for customer-facing staff",
                    "Develop better self-service options",
                    "Implement regular customer feedback reviews"
                ]
            },
            {
                "icon": "bi-gear",
                "title": "Product/Service Optimization",
                "items": [
                    "Address common quality issues",
                    "Improve reliability and consistency",
                    "Enhance user experience design",
                    "Implement more rigorous testing procedures"
                ]
            },
            {
                "icon": "bi-graph-up",
                "title": "Value Proposition Improvement",
                "items": [
                    "Review pricing and value perception",
                    "Develop more competitive offerings",
                    "Enhance unique selling points",
                    "Better communicate benefits to customers"
                ]
            }
        ]
    
    # Render template with data
    return render_template(
        'report.html',
        company_name=company_name,
        report=report,
        post_count=post_count,
        date_range=f"{oldest_date} to {newest_date}",
        sentiments=sentiments,
        chart_data=json.dumps(chart_data),
        sample_posts=sample_posts,
        data_source=data_source,
        priority_areas=priority_areas,
        company_type=company_type
    )

@app.route('/export_report', methods=['POST'])
def export_report():
    """Export the report to a file."""
    report = request.form.get('report', '')
    company_name = request.form.get('company_name', 'Company').replace(' ', '_').replace('(', '').replace(')', '')
    
    report_filename = f"{company_name}_sentiment_report.txt"
    with open(report_filename, "w") as f:
        f.write(report)
    
    return jsonify({'success': True, 'filename': report_filename})

if __name__ == "__main__":
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 5006))
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=port) 