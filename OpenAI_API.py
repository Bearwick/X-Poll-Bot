import json
import os
from openai import OpenAI
from Storage import get_questions, read_json

# Set up the API client
api_key = os.environ.get("Poll_Bot_OpenAI_API_Key")
client = OpenAI(api_key=api_key)

def fetch_polls_openAI(polls_to_fetch):
    poll_questions = get_questions()
    questions_json = read_json()
    # Base prompt for generating polls
    base_prompt = f'Generate {polls_to_fetch} polls in the theme of "Smarter than a Fifth Grader" in JSON format. Each poll should contain a question and between two to four answer options. Questions should be a maximum of 280 characters, and each answer should be a maximum of 25 characters.'

    # Complete prompt with formatting instructions
    base_prompt += '\n\nThe format should be:\n{{"polls": [\n  {{"text": "question to answer", "options":["answer1", "answer2", "answer3", "answer4"]}},\n  {{"text": "another question to answer", "options":["answer1", "answer2"]}},\n  ...\n]}}\n\nPlease create diverse questions on topics like science, history, math, geography, social studies, general knowledge, health and physical educatin, and literature that are challenging for both children and adults. Remember to include questions with two, three or four answer options. The provided json object includes questions already asked, do not create duplicates.'

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system", 
                "content": json.dumps(questions_json)
            },
            {
                "role": "user",
                "content": base_prompt,
                }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "polls_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "polls": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "text": {
                                        "description": "The question text",
                                        "type": "string",
                                        "maxLength": 280
                                    },
                                    "options": {
                                        "description": "The answer options for the question",
                                        "type": "array",
                                        "minItems": 2,
                                        "maxItems": 4,
                                        "items": {
                                            "type": "string",
                                            "maxLength": 25
                                        }
                                    }
                                },
                                "required": ["text", "options"],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": ["polls"],
                    "additionalProperties": False
                }
            }
        }
    )

    return json.loads(response.choices[0].message.content)

