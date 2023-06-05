import yaml
from loguru import logger

from . import utils
from .chatgpt import ChatGPT


class CodeImprover:
    def __init__(self, yaml_path):
        logger.info(f"Initializing CodeImprover for {yaml_path}")
        self.texts = {}
        self.files = []
        self.config = None
        self.steps_prompt = None
        self.critic_prompt = None
        self.resolver_prompt = None
        #
        self.load_config(yaml_path)
        self.load_texts()

        self.gpt = ChatGPT(role=self.config["role"], model_name=self.config["model"])
        self.full_text = self.get_full_text()
        #
        self.gpt.add_user_message(self.full_text)
        logger.info(f"Prefix: {self.full_text[:500]}\n...")
        logger.info(f"Files added to context: {self.files}")
        #

    def load_config(self, yaml_path):
        with open(yaml_path) as config_file:
            self.config = yaml.safe_load(config_file)
        self.steps_prompt = self.config["step_by_step_prompt"]
        self.critic_prompt = self.config["critic_prompt"]
        self.resolver_prompt = self.config["resolver_prompt"]

    def load_texts(self):
        directory = self.config["directory"]
        self.files = self.config["files"]
        self.texts = {}
        for path in self.files:
            with open(f"{directory}/{path}") as fp:
                self.texts[path] = fp.read()

    def get_full_text(self, files=None):
        files = list(files or self.texts.keys())
        texts = [f"Project contains following files: {files}"]
        texts += [
            f"### Content of '{path}' file:\n\n{text}"
            for path, text in self.texts.items()
            if path in files
        ]
        full_text = "\n".join(texts)
        num_tokens = self.gpt.get_num_tokens_for_text(full_text)
        print(f"Number of tokens in {files} = {num_tokens}")
        return full_text

    def generate_reply(self, prompt):
        return self.gpt.display_reply_sync(prompt)

    def update_file(self, path, new_content, mode="w"):
        with open(path, mode=mode) as fp:
            fp.write(new_content)
        print(f"File '{path}' has been updated.")

    def fix_prompt(self, prompt):
        # Shortcut for "Let's think step-by-step"
        steps_shortcut = ".sbs"
        if steps_shortcut in prompt:
            prompt = prompt.replace(steps_shortcut, self.steps_prompt)
        logger.info(f"Prompt: {prompt}")
        return prompt

    def start_interactive_dialog(self):
        logger.info("Starting interactive dialog. Type 'exit' to end the conversation.")
        last_output = ""
        cmds = [".exit", ".regenerate", ".critic", ".resolver"]
        cmds += [".update", ".append", ".sbs"]
        cmd_input = utils.get_prompt_session(cmds=cmds)
        while True:
            try:
                prompt = cmd_input.prompt().strip()
            except KeyboardInterrupt:
                break

            if prompt == "":
                continue

            prompt = self.fix_prompt(prompt)

            if prompt == ".exit":
                break
            elif prompt == ".regenerate":
                last_output = self.gpt.regenerate_last_reply()
            elif prompt == ".critic":
                last_output = self.generate_reply(self.critic_prompt)
            elif prompt == ".resolver":
                last_output = self.generate_reply(self.resolver_prompt)
            elif prompt.startswith(".update "):
                file_path = prompt.split(" ")[-1]
                self.update_file(file_path, last_output)
            elif prompt.startswith(".append "):
                file_path = prompt.split(" ")[-1]
                self.update_file(file_path, last_output, mode="a+")
            else:
                # User input
                last_output = self.generate_reply(prompt)


def main():
    logger.info("Starting CodeImprover")
    code_improver = CodeImprover("config.yaml")
    code_improver.start_interactive_dialog()


if __name__ == "__main__":
    main()
