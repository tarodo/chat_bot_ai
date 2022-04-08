import json
import os

from environs import Env
from google.cloud import dialogflow

FALLBACK_PHRASES = [
    "Sorry, I don't understand you.",
    "Call my manager, please"
]


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )


def create_fallback_intent(project_id, message_texts):
    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)
    intent = dialogflow.Intent(
        display_name="Sorry", is_fallback=True, messages=[message]
    )
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )


if __name__ == "__main__":
    env = Env()
    env.read_env()

    QUESTIONS_PATH = os.getenv("QUESTIONS_FILE")
    PROJECT_ID = os.environ["GOOGLE_PROJECT_ID"]
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as my_file:
        questions = json.load(my_file)
    for question, work_intent_block in questions.items():
        create_intent(
            PROJECT_ID,
            question,
            work_intent_block["questions"],
            [work_intent_block["answer"]],
        )

    create_fallback_intent(PROJECT_ID, FALLBACK_PHRASES)
