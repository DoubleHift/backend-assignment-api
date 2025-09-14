import requests
from dataLayers.NoteDataLayer import NoteDataLayer
from core.config import settings
from prompts.notesummaryprompt import create_prompt
from core.Database import SessionLocal

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"


class AISummaryService:
    noteDataLayer = NoteDataLayer()

    def get_ai_response(self, text: str) -> str:
        request_url = f"{GEMINI_API_URL}?key={settings.GEMINI_API_KEY}"

        payload = {"contents": [{"parts": [{"text": create_prompt(text)}]}]}

        headers = {"Content-Type": "application/json"}

        print(f"Sending REST request to Gemini API for text: '{text[:50]}...'")

        try:
            response = requests.post(request_url, json=payload, headers=headers)
            response.raise_for_status()

            data = response.json()
            if "candidates" in data and data["candidates"]:
                content = data["candidates"][0].get("content", {})
                if "parts" in content and content["parts"]:
                    answer = content["parts"][0].get("text", "")
                    print("Response received from Gemini API via REST.")
                    return answer.strip()

            print(f"Unexpected API response format: {data}")
            raise Exception("Unexpected response format from Gemini API.")

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err} - {response.text}")
            raise Exception("Gemini API returned an error.")
        except Exception as e:
            print(f"An error occurred with Gemini API REST call: {e}")
            raise Exception("Gemini API failed to generate response.")

    def process_ai_request(self, note_id: int):
        db = SessionLocal()
        try:
            note = self.noteDataLayer.getNoteById(db, note_id)
            if not note:
                print(f"Note {note_id} not found for processing.")
                return

            print(f"Processing note {note_id} with Gemini (REST)...")
            self.noteDataLayer.updateNote(db, note, {"status": "processing"})

            ai_answer = self.get_ai_response(note.raw_text)

            print(f"Note {note_id} processed successfully by Gemini (REST).")

            self.noteDataLayer.updateNote(
                db, note, {"status": "done", "summary": ai_answer}
            )

        except Exception as e:
            print(f"Failed to process note {note_id}. Error: {e}")

            note = self.noteDataLayer.getNoteById(db, note_id)
            if note:
                self.noteDataLayer.updateNote(db, note, {"status": "failed"})
        finally:
            db.close()
