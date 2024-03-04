import glob
import yaml
import chardet
from loguru import logger

from . import utils
from .chatgpt import ChatGPT
from .config import CodeImproverConfig, ProjectConfig


class CodeImprover:
    def __init__(self, yaml_path):
        logger.info(f"Initializing CodeImprover for {yaml_path}")
        self.texts = {}
        self.config = None
        self.replaces = {}
        #
        self.load_config(yaml_path)
        self.load_texts()

        conf = self.config
        self.gpt = ChatGPT(
            role=conf["role"],
            model_name=conf["model"],
            max_context_tokens=conf["max_context_tokens"],
            max_output_tokens=conf["max_output_tokens"],
        )
        self.full_text = self.get_full_text()
        #
        self.gpt.add_user_message(self.full_text)
        self.log_initial_context()

    def load_config(self, yaml_path):
        with open(yaml_path) as config_file:
            self.config = yaml.safe_load(config_file)
        prompts = self.config["prompts"]
        self.replaces = {f".{name}": prompt for name, prompt in prompts.items()}

    def _load_one_text(self, full_path):
        with open(full_path, "rb") as fp:
            result = chardet.detect(fp.read())
            encoding = result["encoding"]

        with open(full_path, "r", encoding=encoding) as fp:
            try:
                return fp.read()
            except UnicodeDecodeError:
                return open(full_path, "r").read()

    def load_texts(self):
        directory = self.config["directory"]
        masks = self.config["files"]
        self.texts = {}
        for mask in masks:
            for path in glob.glob(f"{directory}/{mask}"):
                self.texts[path] = self._load_one_text(path)

    def get_full_text(self, files=None):
        files = list(files or self.texts.keys())
        texts = [f"Project contains following files: {files}"]
        texts += [
            f"### Content of '{path}' file:\n\n{text}"
            for path, text in self.texts.items()
            if path in files
        ]
        full_text = "\n".join(texts)
        return full_text

    def log_initial_context(self):
        file_names = list(self.texts.keys())
        num_tokens = self.gpt.get_num_tokens_for_text(self.full_text)
        text_info = f"\nPrefix: {self.full_text[:500]}\n...\n"
        text_info += f"Files: {file_names}\n"
        text_info += f"Number of tokens = {num_tokens}\n"
        logger.info(text_info)

    def generate_reply(self, prompt):
        return self.gpt.display_reply_sync(prompt)

    def update_file(self, path, new_content, mode="w"):
        with open(path, mode=mode) as fp:
            fp.write(new_content)
        print(f"File '{path}' has been updated.")

    def fix_prompt(self, prompt):
        for cmd, text in self.replaces.items():
            if cmd in prompt:
                prompt = prompt.replace(cmd, text)

        logger.info(f"\nPrompt: {prompt}")
        return prompt

    def start_interactive_dialog(self):
        logger.info("Starting interactive dialog. Type 'exit' to end the conversation.")
        last_output = ""
        cmds = [".exit", ".regenerate", ".update", ".append"]
        cmds += list(self.replaces.keys())
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
    if not CodeImproverConfig.try_load_openai_key():
        return

    path = ProjectConfig.get_config_path("code_improver.yaml")
    if not path:
        return

    code_improver = CodeImprover(path)
    code_improver.start_interactive_dialog()


if __name__ == "__main__":
    main()
