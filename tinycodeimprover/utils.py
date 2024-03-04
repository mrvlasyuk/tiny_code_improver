import traceback

import tiktoken
import prompt_toolkit as pt
from litellm import acompletion, RateLimitError


OPTIONS = {
    "temperature": 0.3,
    "top_p": 1,
}


class Model:
    def __init__(
        self, model_name, max_output_tokens, max_context_tokens, json_mode=False
    ):
        self.model = model_name
        self.max_output_tokens = max_output_tokens
        self.max_context_tokens = max_context_tokens
        self.encoding = self.get_encoding()
        self.json_mode = json_mode

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

    async def get_gpt_reply_stream(self, messages, user=None, min_chunk=100):
        used_tokens = self.get_num_tokens_for_msgs(messages)
        if self.max_context_tokens:
            context_tokens_left = self.max_context_tokens - used_tokens
            tokens_left = min(context_tokens_left, self.max_output_tokens)
            print(f"{used_tokens = }, {context_tokens_left = }")
            assert tokens_left > 0, "Too many tokens in the context"
        else:
            print(f"{used_tokens = }")
            tokens_left = None

        options = {**OPTIONS, "max_tokens": tokens_left}
        if self.json_mode:
            options["response_format"] = {"type": "json_object"}

        try:
            stream = await acompletion(
                model=self.model,
                messages=messages,
                stream=True,
                user=str(user),
                **options,
            )
        except RateLimitError:
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
