# TinyCodeImprover

![TinyCodeImprover demo](https://s11.gifyu.com/images/Suc53.gif)

TinyCodeImprover is a tiny project designed to help developers work with code in the context of an entire project using GPT-4. It simplifies the process of getting help from GPT-4 by allowing you to easily add files from your project to the prompt context. With TinyCodeImprover, you can ask questions about your code, request it to fix issues, find bugs, or even write new features!

## Table of Contents

- [Installation](#installation)
- [Usage and Examples](#usage-and-examples)
- [Features and Functionality](#features-and-functionality)
- [Code Structure and Organization](#code-structure-and-organization)
- [License](#license)
- [Success Stories and Use Cases](#success-stories-and-use-cases)

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/mrvlasyuk/code_improver_gpt.git
cd code_improver_gpt
```
Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project directory and add your OpenAI API key:

```
OPENAI_KEY=your_api_key_here
```

## Usage and Examples

To start using TinyCodeImprover, run the `code_improver.py` script:

```bash
python code_improver.py
```

This will start an interactive dialog with GPT-4. You can ask questions about your code, request GPT-4 to fix issues, find bugs, or even write new features. For example:

```
User: How can I improve the error handling in utils.py?
```

You can also use special commands like `.critic` to ask GPT-4 to critique its own answer, or `.resolver` to improve the initial answer by fixing any errors found by the critic.

## Features and Functionality

- **Interactive dialog**: TinyCodeImprover allows you to start an interactive dialog with GPT-4, making it easy to ask questions about your code, request GPT-4 to fix issues, find bugs, etc.
- **Critic feature**: After asking GPT-4 to fix or recommend something, you can use the `.critic` command to ask it to critique its own answer. This helps in identifying errors in its own logic. In my experience he found bugs in his own code in ~30% of cases.
- **Customizable prompts**: You can easily customize prompts in TinyCodeImprover, which helps in getting more accurate and relevant responses from GPT-4.

## Code Structure and Organization

TinyCodeImprover consists of several Python files:

- `utils.py`: Contains utility functions and classes for working with GPT-4 and handling user input.
- `chatgpt.py`: Implements the main ChatGPT class, which handles communication with GPT-4 and manages the conversation context.
- `code_improver.py`: The main script that starts the interactive dialog and processes user commands.

## Success Stories and Use Cases

- **Improving itself**: TinyCodeImprover was used to improve its own code. It added a nice input library () for a better user experience.
- **Fastest README ever**: GPT-4 wrote a README for this project in just 1 minute using TinyCodeImprover. [see gif above]
- **HTML & CSS guru**: TinyCodeImprover has helped me to fix HTML & CSS issues in my projects. I've learned many tricks from it.


## License

TinyCodeImprover is released under the [MIT License](LICENSE). Please provide proper attribution to the original author if you use this project in your work.
