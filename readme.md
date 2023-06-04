# TinyCodeImprover

![TinyCodeImprover demo](https://s11.gifyu.com/images/Suc53.gif)

TinyCodeImprover is a tiny project designed to help developers work with code in the context of an entire project using GPT-4. It simplifies the process of getting help from GPT by allowing you to easily add files from your project to the prompt context. With TinyCodeImprover, you can ask questions about your code, request it to fix issues, find bugs, or even write new features!

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage and Examples](#usage-and-examples)
- [Features and Functionality](#features-and-functionality)
- [Success Stories and Use Cases](#success-stories-and-use-cases)
- [Code Structure and Organization](#code-structure-and-organization)
- [License](#license)

## Installation

Clone the repository and navigate to the project directory and install the required packages:

```bash
git clone https://github.com/mrvlasyuk/code_improver_gpt.git
cd code_improver_gpt
pip install -r requirements.txt
```

Create a `.env` file in the project directory and add your OpenAI API key:

```
OPENAI_KEY=your_api_key_here
```

## Configuration

Edit the `config.yaml` file to list the directory and files of your project:

```yaml
project_name: YourProjectName
directory: "path/to/your/project"
files:
  - file1.py
  - file2.py
  - file3.py
```

This will allow TinyCodeImprover to include the specified files in the GPT-4 prompt context.

## Usage and Examples

To start using TinyCodeImprover, run the `code_improver.py` script:

```bash
python code_improver.py
```

This will start an interactive dialog with GPT-4. You can ask questions about your code, request it to fix issues, find bugs, or even write new features. For example:

```
User: How can I improve the error handling in utils.py?
```

You can also use special commands like `.critic` to ask the model to critique its own answer, or `.resolver` to improve the initial answer by fixing any errors found by the critic.

## Features and Functionality

- **Interactive dialog**: TinyCodeImprover allows you to start an interactive dialog with GPT-4, making it easy to ask questions about your code, request it to fix issues, find bugs, etc.
- **Critic feature**: After asking the model to fix or recommend something, you can use the `.critic` command to ask it to critique its own answer. This helps in identifying errors in its own logic. In my experience he found bugs in his own code in ~30% of cases.
- **Customizable prompts**: You can easily customize prompts in TinyCodeImprover, which helps in getting more accurate and relevant responses from GPT-4.

## Success Stories and Use Cases

- **Improving itself**: TinyCodeImprover was used extensively to improve its own code. For example, it added a nice input library `prompt_toolkit` for a better user experience.
- **My fastest README ever**: GPT-4 wrote a README for this project in just a minute using TinyCodeImprover. [see gif above]
- **HTML & CSS guru**: TinyCodeImprover has helped me fix numerous HTML & CSS issues in several projects. I've learned a few CSS tricks from it.

## Code Structure and Organization

TinyCodeImprover consists of several Python files:

- `utils.py`: Contains utility functions and classes for working with OpenAI API and handling user input.
- `chatgpt.py`: Implements the main ChatGPT class, which handles communication with GPT-4 and manages the conversation context.
- `code_improver.py`: The main script that starts the interactive dialog and processes user commands.

## License

TinyCodeImprover is released under the [MIT License](LICENSE). Please provide proper attribution to the original author if you use this project in your work.