import os

from environs import Env
from google.cloud import dialogflow

env = Env()
env.read_env()
PROJECT_ID = os.environ["GOOGLE_PROJECT_ID"]


def detect_intent_text(session_id, text, language_code="ru") -> str:
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    if not response.query_result.intent.is_fallback:
        return response.query_result.fulfillment_text