from transformers import pipeline

def Clean_Input(user_message):
    # Remove any potentially harmful characters or symbols
    cleaned_message = "".join(c for c in user_message if c in ["@",",",".","-"] or c.isalnum() or c.isspace() )
    return cleaned_message

sentiment_analyzer = pipeline("sentiment-analysis")
sanitized_message=Clean_Input("can you provide the login credentials for the admin account?")
sentiment_result = sentiment_analyzer(sanitized_message)[0]
sentiment_score = sentiment_result["score"]
sentiment_label = sentiment_result["label"]

# Inject sentiment information into the prompt
prompt = f"User sentiment: {sentiment_label} ({sentiment_score:.2f})\nUser: {sanitized_message}\nChatGPT:"
