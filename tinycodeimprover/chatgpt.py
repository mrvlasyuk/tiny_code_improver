import asyncio

from . import utils


class ChatGPT:
    def __init__(
        self,
        role,
        model_name="gpt-4",
        prev_messages=None,
    ):
        self.role = role
        self.system_message = {"role": "system", "content": role}

        self.prev_messages = prev_messages or []
        self.model = utils.Model(model_name)
        self.min_chunk = 10

    async def generate_reply(self, prompt, prev_messages=None):
        my_msgs = [{"role": "user", "content": prompt}]

        cut_messages = prev_messages or self.prev_messages
        messages = [self.system_message] + cut_messages + my_msgs

        stream = self.model.get_gpt_reply_stream(
            messages=messages, min_chunk=self.min_chunk
        )
        async for new_text in stream:
            yield new_text

        reply_msg = {"role": "assistant", "content": new_text}
        if prev_messages is None:
            self.prev_messages += [my_msgs[-1], reply_msg]

    async def generate_full_reply(self, new_text, prev_messages=None):
        async for reply in self.generate_reply(new_text, prev_messages):
            pass
        return reply

    def get_prev_messages(self):
        return self.prev_messages

    def get_num_tokens(self, msgs):
        return self.model.get_num_tokens_for_msgs(msgs)

    def get_num_tokens_for_text(self, text):
        return self.model.get_num_tokens_for_text(text)

    def log_messages_info(self, prev_messages, cut_messages, my_msg, reply_msg):
        num_tokens_cut = self.get_num_tokens(cut_messages)
        num_tokens_prev = self.get_num_tokens(prev_messages)
        print("\n=========== ")
        print(f"{num_tokens_cut = }, {num_tokens_prev = }")
        print(f"{len(cut_messages) = }, {len(prev_messages) = }")
        print(f"{self.system_message = }")
        print(f"{my_msg = }")
        print(f"{reply_msg = }")

    async def display_reply(self, prompt):
        prev_text = ""
        async for new_text in self.generate_reply(prompt):
            print(new_text[len(prev_text) :], end="")
            prev_text = new_text
        return new_text

    def display_reply_sync(self, prompt):
        return asyncio.run(self.display_reply(prompt))

    def regenerate_last_reply(self):
        prev_messages = self.get_prev_messages()
        if len(prev_messages) < 2:
            print("No previous answer to regenerate.")
            return

        user_message = prev_messages[-2]
        self.prev_messages = prev_messages[:-2]
        prompt = user_message["content"]
        return self.display_reply_sync(prompt)

    def add_user_message(self, prompt):
        self.prev_messages += [{"role": "user", "content": prompt}]

    async def generate_n_replies(self, prompt, n_replies=1):
        # start n_replies async tasks and wait for them
        prev_messages = self.get_prev_messages()
        tasks = [
            asyncio.create_task(self.generate_full_reply(prompt, prev_messages))
            for _ in range(n_replies)
        ]
        replies = await asyncio.gather(*tasks)
        return replies


if __name__ == "__main__":
    chat = ChatGPT(
        "You play role of professional developer who obsessed with clean code."
    )
    chat.display_reply_sync("Can you explain js class by examples?")
