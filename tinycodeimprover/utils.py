import traceback

import openai
import tiktoken
import prompt_toolkit as pt


OPENAI_OPTIONS = {
    "temperature": 0.3,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}


class Model:
    def __init__(self, model_name, max_tokens):
        self.model = model_name
        self.max_tokens = max_tokens
        self.encoding = self.get_encoding()
        self.api = openai.AsyncOpenAI(api_key=openai.api_key)

    def get_encoding(self):
        """Returns the encoding used by a model."""
        try:
            return tiktoken.encoding_for_model(self.model)
        except KeyError:
            return tiktoken.get_encoding("cl100k_base")

    def get_num_tokens_for_msgs(self, msgs):
        """Returns the number of tokens used by a list of msgs."""
        num_tokens = 0
        for message in msgs:
            num_tokens += (
                4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            )
            for key, value in message.items():
                num_tokens += len(self.encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens

    def get_num_tokens_for_text(self, text):
        return len(self.encoding.encode(text))

    ##########

    async def get_gpt_reply_stream(
        self, messages, user=None, min_chunk=100, max_tokens=None
    ):
        used_tokens = self.get_num_tokens_for_msgs(messages)
        tokens_left = self.max_tokens - used_tokens
        print(f"{used_tokens = }, {tokens_left = }")
        if max_tokens is not None:
            tokens_left = min(tokens_left, max_tokens)
        options = {**OPENAI_OPTIONS, "max_tokens": tokens_left}
        assert tokens_left > 0, "Too many tokens in the context"

        try:
            stream = await self.api.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
                user=str(user),
                **options,
            )
        except openai.RateLimitError:
            traceback.print_exc()
            yield "(Sorry, that model is currently overloaded. Try later)"
            return

        prev_text = new_text = ""
        collected_answer = ""

        async for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            collected_answer += delta
            new_text = collected_answer.strip()
            if len(new_text) - len(prev_text) < min_chunk:
                continue

            prev_text = new_text
            yield new_text

        if prev_text != new_text:
            yield new_text


def get_prompt_session(cmds):
    return pt.PromptSession(
        history=pt.history.FileHistory(".history"),
        auto_suggest=pt.auto_suggest.AutoSuggestFromHistory(),
        completer=pt.completion.WordCompleter(cmds),
        message="\nUser: ",
    )
