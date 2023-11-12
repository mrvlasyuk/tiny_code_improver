import os
import glob
import yaml
import shutil

import openai
import platformdirs


class CodeImproverConfig:
    @staticmethod
    def _get_config_path():
        config_dir = platformdirs.user_config_dir("tinycodeimprover")
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, "tiny_config.yaml")

    @staticmethod
    def _create_empty_config(yaml_path):
        with open(yaml_path, "w") as f:
            yaml.dump({"OPENAI_KEY": ""}, f)

    @staticmethod
    def try_load_openai_key():
        yaml_path = CodeImproverConfig._get_config_path()
        if not os.path.exists(yaml_path):
            print(f"Please add OpenAI API key to {yaml_path}")
            CodeImproverConfig._create_empty_config(yaml_path)
            return False

        with open(yaml_path) as f:
            config = yaml.safe_load(f)

        key = config.get("OPENAI_KEY")
        if not key:
            print(f"Please add OpenAI API key to {yaml_path}")
            return False

        openai.api_key = key
        return True


class ProjectConfig:
    @staticmethod
    def _copy_template(yaml_path):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(current_dir, "config_template.yaml")
        shutil.copy(template_path, yaml_path)

    @staticmethod
    def _get_path_from_parent_dir(filename):
        # recursively check parent directories
        current_dir = os.path.abspath(os.getcwd())
        while True:
            yaml_path = os.path.join(current_dir, filename)
            if os.path.exists(yaml_path):
                return yaml_path
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:
                break
            current_dir = parent_dir
        return None

    @staticmethod
    def get_config_path(yaml_path):
        found_path = ProjectConfig._get_path_from_parent_dir(yaml_path)
        if not found_path:
            ProjectConfig._copy_template(yaml_path)
            print(
                f"Config file {yaml_path} has been created in the current directory. Add your files and run `improve_code` again."
            )
            return None

        with open(found_path) as f:
            config = yaml.safe_load(f)

        os.chdir(os.path.dirname(found_path))
        dir_name = config.get("directory", ".")
        masks = config.get("files", [])
        if not masks:
            print(f"{found_path}: No files specified.")
            return None

        for mask in masks:
            files = glob.glob(f"{dir_name}/{mask}")
            if not files:
                print(f"{found_path}: No files found for mask '{mask}'")
                return None
        return found_path
