from setuptools import setup, find_packages

setup(
    name="tinycodeimprover",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai",
        "platformdirs",
        "tiktoken",
        "prompt_toolkit",
        "loguru",
        "PyYAML",
        "litellm",
    ],
    entry_points={
        "console_scripts": [
            "improve_code = tinycodeimprover.code_improver:main",
        ],
    },
    author="@mrvlasyuk",
    description="A tiny project to help developers work with code using GPT-4",
    url="https://github.com/mrvlasyuk/tiny_code_improver",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    package_data={
        "tinycodeimprover": ["config_template.yaml"],
    },
)
