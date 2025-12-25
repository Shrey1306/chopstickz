"""Application state management for the Chopstickz web interface."""

import json
import os

import openai
import reflex as rx
import requests

openai.api_key = os.getenv("OPENAI_API_KEY", "")
openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

BAIDU_API_KEY = os.getenv("BAIDU_API_KEY")
BAIDU_SECRET_KEY = os.getenv("BAIDU_SECRET_KEY")


def get_baidu_access_token() -> str:
    """Get Baidu API access token."""
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": BAIDU_API_KEY,
        "client_secret": BAIDU_SECRET_KEY,
    }
    return str(requests.post(url, params=params).json().get("access_token"))


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str


DEFAULT_CHATS = {
    "Edit 1": [QA(question="Upload an Image and Type to Edit.", answer="Go on!")],
}


class State(rx.State):
    """The application state."""

    chats: dict[str, list[QA]] = DEFAULT_CHATS
    current_chat: str = "Edit 1"
    question: str
    processing: bool = False
    new_chat_name: str = ""
    drawer_open: bool = False
    modal_open: bool = False
    api_type: str = "baidu" if BAIDU_API_KEY else "openai"
    video_segments: list[str] = []

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle video file upload."""
        for file in files:
            upload_data = await file.read()
            assets_dir = os.path.join(os.getcwd(), "assets")
            outfile = os.path.join(assets_dir, file.filename)

            with open(outfile, "wb") as file_object:
                file_object.write(upload_data)

            self.video_segments.append(file.filename)

    def create_chat(self):
        """Create a new chat session."""
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = []
        self.modal_open = False

    def toggle_modal(self):
        """Toggle the new chat modal."""
        self.modal_open = not self.modal_open

    def toggle_drawer(self):
        """Toggle the sidebar drawer."""
        self.drawer_open = not self.drawer_open

    def delete_chat(self):
        """Delete the current chat session."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[0]
        self.toggle_drawer()

    def set_chat(self, chat_name: str):
        """Set the active chat session."""
        self.current_chat = chat_name
        self.toggle_drawer()

    @rx.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles."""
        return list(self.chats.keys())

    async def process_question(self, form_data: dict[str, str]):
        """Process a user question through the appropriate API."""
        question = form_data["question"]
        if question == "":
            return

        if self.api_type == "openai":
            model = self.openai_process_question
        else:
            model = self.baidu_process_question

        async for value in model(question):
            yield value

    async def openai_process_question(self, question: str):
        """Process question using OpenAI API."""
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)
        self.processing = True
        yield

        messages = [
            {
                "role": "system",
                "content": "You are a friendly chatbot named prod.ai, a language powered video editing tool to simplify content creation.",
            }
        ]
        for qa in self.chats[self.current_chat]:
            messages.append({"role": "user", "content": qa.question})
            messages.append({"role": "assistant", "content": qa.answer})

        messages = messages[:-1]

        session = openai.ChatCompletion.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            messages=messages,
            stream=True,
        )

        for item in session:
            if hasattr(item.choices[0].delta, "content"):
                answer_text = item.choices[0].delta.content
                self.chats[self.current_chat][-1].answer += answer_text
                self.chats = self.chats
                yield

        self.processing = False

    async def baidu_process_question(self, question: str):
        """Process question using Baidu API."""
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)
        self.processing = True
        yield

        messages = []
        for qa in self.chats[self.current_chat]:
            messages.append({"role": "user", "content": qa.question})
            messages.append({"role": "assistant", "content": qa.answer})

        messages_json = json.dumps({"messages": messages[:-1]})

        session = requests.request(
            "POST",
            "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token="
            + get_baidu_access_token(),
            headers={"Content-Type": "application/json"},
            data=messages_json,
        )

        json_data = json.loads(session.text)
        if "result" in json_data.keys():
            answer_text = json_data["result"]
            self.chats[self.current_chat][-1].answer += answer_text
            self.chats = self.chats
            yield

        self.processing = False
