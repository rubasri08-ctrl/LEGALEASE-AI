import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()


class GeminiDocumentGenerator:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        )

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model_name = model_name

    def generate_document(
        self,
        document_type,
        parties,
        terms,
        dates
    ):

        prompt = f"""
You are a legal document drafting assistant.

Create a professional draft for the following document.

Document Type:
{document_type}

Parties Involved:
{parties}

Terms and Conditions:
{terms}

Effective Date:
{dates}

Requirements:
- Use clear professional legal language.
- Include a suitable document title.
- Include the parties involved.
- Include the effective date.
- Organize the terms and conditions clearly.
- Add suitable general clauses where appropriate.
- Do not invent specific personal information.
- Do not claim that the document provides legal advice.
- Return only the document content.
"""

        max_attempts = 4

        for attempt in range(max_attempts):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )

                if not response or not response.text:
                    raise ValueError(
                        "Gemini returned an empty response."
                    )

                return response.text.strip()

            except errors.ServerError as e:
                if attempt == max_attempts - 1:
                    raise RuntimeError(
                        "Gemini is temporarily unavailable. "
                        "Please try generating the document again."
                    ) from e

                wait_time = 2 ** attempt
                time.sleep(wait_time)

        raise RuntimeError(
            "Unable to generate the document."
        )