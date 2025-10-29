from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

intents = {
    "medicine_info": [
        "tell me about this medicine",
        "check expiry date",
        "read my medicine",
        "medicine information",
        "verify my tablet",
        "identify this medicine"
    ]
}

def get_intent(user_text):
    if not user_text:
        return None
    texts = [user_text] + [p for intent in intents.values() for p in intent]
    vec = CountVectorizer().fit_transform(texts)
    similarity = cosine_similarity(vec[0:1], vec[1:]).flatten()
    best_match_index = similarity.argmax()
    best_match_value = similarity[best_match_index]
    print(f"Intent similarity: {best_match_value:.2f}")
    if best_match_value > 0.3:
        return "medicine_info"
    return None
