
import requests
import json
import uuid


class LangflowExtractor:

    def __init__(
        self,
        api_url,
        api_key
    ):

        self.api_url = api_url
        self.api_key = api_key

    def extract_fields(
        self,
        markdown_text
    ):

        payload = {

            "output_type": "text",

            "input_type": "text",

            "session_id": str(
                uuid.uuid4()
            ),

            "tweaks": {

                "TextInput-DF7jm": {

                    "input_value":
                        markdown_text
                }
            }
        }

        headers = {

            "x-api-key":
                self.api_key
        }

        response = requests.post(
            self.api_url,
            json=payload,
            headers=headers,
            timeout=120
        )

        print(response.status_code)
        print(response.text)

        response.raise_for_status()

        data = response.json()

        return self.extract_output(data)

    @staticmethod
    def extract_output(response_json):

        text = (
            response_json["outputs"][0]
            ["outputs"][0]
            ["results"]["text"]["data"]
            ["text"]
        )

        text = (
            text.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(text)