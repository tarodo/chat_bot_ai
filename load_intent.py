import json
import os
from environs import Env

from google.cloud import dialogflow


def read_phrases(json_path, question_type) -> dict:
    with open(json_path, "r", encoding="utf-8") as my_file:
        questions = json.load(my_file)
    return questions[question_type]


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


if __name__ == "__main__":
    env = Env()
    env.read_env()

    QUESTIONS_PATH = os.getenv("QUESTIONS_FILE")
    PROJECT_ID = os.environ["GOOGLE_PROJECT_ID"]
    work_intent_block = read_phrases(QUESTIONS_PATH, "Устройство на работу")
    create_intent(PROJECT_ID, "Устройство на работу", work_intent_block["questions"], [work_intent_block["answer"]])
