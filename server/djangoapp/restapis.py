import os
from urllib.parse import quote
import requests
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv("backend_url", "http://localhost:3030").rstrip("/")
sentiment_analyzer_url = os.getenv("sentiment_analyzer_url", "http://localhost:5050").rstrip("/")


def get_request(endpoint, **kwargs):
    """
    Send GET to the backend service (dealers/reviews microservice backend).
    """
    endpoint = endpoint if endpoint.startswith("/") else f"/{endpoint}"
    request_url = f"{backend_url}{endpoint}"

    try:
        resp = requests.get(request_url, params=kwargs if kwargs else None, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print("Network exception occurred in get_request:", e)
        return []


def analyze_review_sentiments(text):
    """
    Send GET to sentiment analyzer microservice.
    Expected: {"sentiment":"positive"|"neutral"|"negative"}
    """
    # IMPORTANT: matches your Flask route: /analyze/<input_txt>
    request_url = f"{sentiment_analyzer_url.rstrip('/')}/analyze/{quote(text)}"

    try:
        resp = requests.get(request_url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print("Network exception occurred in analyze_review_sentiments:", e)
        return {"sentiment": "neutral"}


def post_review(data_dict):
    """
    Send POST to backend to insert a review.
    """
    request_url = f"{backend_url}/insert_review"

    try:
        resp = requests.post(request_url, json=data_dict, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print("Network exception occurred in post_review:", e)
        return {"status": 500, "message": "Network exception occurred"}
