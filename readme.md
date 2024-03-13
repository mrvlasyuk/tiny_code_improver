# TinyCodeImprover

TinyCodeImprover is a tiny project designed to help developers work with code in the context of an entire project using GPT-4, Claude, and Gemini models. It simplifies the process of getting help from AI by allowing you to easily add files from your project to the prompt context. With TinyCodeImprover, you can ask questions about your code, request it to fix issues, find bugs, or even write new features!

## Demo

![demo](https://github.com/mrvlasyuk/mrvlasyuk.github.io/raw/main/assets/code_gif.gif)

## Table of Contents

- [Installation](#installation)
- [Usage and Examples](#usage-and-examples)
- [Features and Functionality](#features-and-functionality)
- [Success Stories and Use Cases](#success-stories-and-use-cases)
- [Code Structure and Organization](#code-structure-and-organization)
- [License](#license)

## Installation

Install TinyCodeImprover using pip:

```bash
pip3 install -U git+https://github.com/mrvlasyuk/tiny_code_improver
```

## Usage and Examples

To start using TinyCodeImprover with GPT-4, Claude, or Gemini models, run the `improve_code` command. It will guide you on where to put your OpenAI API key or the API keys for other services if you're using Claude or Gemini.

```bash
improve_code
```

This will create a `code_improver.yaml` file in your current directory. Edit this file to add the files you want to provide to the context:

```yaml
project_name: YourProjectName
directory: "."
files:
  - file1.py
  - file2.py
  - file3.py
```

Now, run the `improve_code` again to start an interactive dialog with GPT-4. You can ask questions about your code, request it to fix issues, find bugs, or even write new features. For example:

```
User: How can I improve the error handling in utils.py?
```

You can also use special commands like `.critic` to ask the model to critique its own answer, or `.resolver` to improve the initial answer by fixing any errors found by the critic.

## Features and Functionality

- **Interactive dialog**: TinyCodeImprover allows you to start an interactive dialog with GPT-4, making it easy to ask questions about your code, request it to fix issues, find bugs, etc.
- **Critic feature**: After asking the model to fix or recommend something, you can use the `.critic` command to ask it to critique its own answer. This helps in identifying errors in its own logic. In my experience, it found bugs in its own code in ~30% of cases.
- **Customizable prompts**: You can easily customize prompts in TinyCodeImprover, which helps in getting more accurate and relevant responses from GPT-4.

## Success Stories and Use Cases

- **Improving itself**: TinyCodeImprover was used extensively to improve its own code. For example, it added a nice input library `prompt_toolkit` for a better user experience.
- **My fastest README ever**: GPT-4 wrote a README for this project in just a minute using TinyCodeImprover. [see gif above]
- **HTML & CSS guru**: TinyCodeImprover has helped me fix numerous HTML & CSS issues in several projects. I've learned a few CSS tricks from it.

## Code Structure and Organization

TinyCodeImprover consists of several Python files:

- `utils.py`: Contains utility functions and classes for working with OpenAI API and handling user input.
- `chatgpt.py`: Implements the main ChatGPT class, which handles communication with GPT-4 and manages the conversation context.
- `config.py`: Handles the configuration of the project, including loading the `code_improver.yaml` file and managing the OpenAI API key.
- `code_improver.py`: The main script that starts the interactive dialog and processes user commands.

## License

TinyCodeImprover is released under the [MIT License](LICENSE). Please provide proper attribution to the original author if you use this project in your work.
