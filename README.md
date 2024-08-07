# Creating GenAI Marketing Benchmarks (v0.2.0 Beta)

## Introduction

Generative AI (GenAI) has the potential to transform the marketing industry, yet there is currently no comprehensive way to assess the marketing capabilities of Large Language Models (LLMs) and other GenAI technologies. This project aims to fill that gap by creating benchmark tests that evaluate GenAI technnology's knowledge, understanding, and ability to perform marketing tasks.

## Contents
- [The Challenge](#the-challenge)
- [Project Objective](#project-objective)
- [Contributors](#contributors)
- [Phase One - Testing Marketing Knowledge](#phase-one---testing-marketing-knowledge)
    - [Preliminary Results](#preliminary-results)
- [Phase Two - Testing Markeitng Understanding](#phase-two---testing-marketing-understanding)
- [Phase Three - Testing Marketing Capabilities](#phase-three---testing-marketing-capabilities)
- [Ideas For Future Development](#ideas-for-future-development)
- [Supported Large Language Models](#supported-large-language-models)
- [Installing The GenAI Marketing Benchmarks](#installing-the-genai-marketing-benchmarks)
- [Running The GenAI Marketing Benchmarks](#running-the-genai-marketing-benchmarks)
- [Testing Methodology](#testing-methodology)

## The Challenge

The marketing industry lacks standardized benchmarks to evaluate GenAI models specifically for marketing knowledge, understanding, and capabilities. While there are existing benchmarks for general GenAI capabilities, these do not adequately cover the breadth and depth required for marketing.

### Key Issues:
- Existing GenAI benchmarks primarily test general knowledge, not marketing-specific knowledge, understanding or capabilities.
- There are a limited number of marketing-related questions in current GenAI benchmark tests (e.g., the [MMMU Benchmark](https://mmmu-benchmark.github.io) has only **216** marketing questions and **12** advertising images).
- Clients, platforms, and agencies need reliable benchmarks to select, develop, and fine-tune GenAI tools.

## Project Objective

To create a comprehensive bank of questions, tests, and tasks that can be used to benchmark GenAI technnology's knowledge, understanding and capabilities across all aspects of marketing.

### Benefits:
- Provides a valuable resource for the marketing industry.
- Offers an objective way to test GenAI technology's marketing knowledge and capabilities.
- Enables comparison between different GenAI technologies.
- Assesses new GenAI technologies and features as they are released.
- Monitors improvements in GenAI knowledge and capabilities over time.

## Contributors

I'd like to thank the following organisations for supporting the project by providng training content, testing questions, and advice:
![Contributors](https://github.com/seanbetts/genai-marketing-benchmarks/blob/main/Images/Contributors.png)


##  PHASE ONE - Testing Marketing Knowledge
![GenAI Marketing Benchmark Questions](https://github.com/seanbetts/genai-marketing-benchmarks/blob/main/Images/Questions_23_June_2024.png)

Some of these questions are UK-centric and have a bias towards the UK marketing industry. Many of the questions are globally applicable though.

### Status: MINIMAL VIABLE PRODUCT
I have collected and created a bank of multiple-choice questions across the breadth and depth of marketing that can be used to test the marketing **knowledge** of LLMs. The LLMs responses to these multiple-choice questions are scored on whether they pick right answer or not.

The database of marketing knowledge questions currently contains **2,800+** multiple-choice questions. The question bank needs broadening out further to include all marketing categories and ensure a high enough volume of questions for each category to make the benchmarks robust.

### More Questions Required
As of **23rd June 2024**, the project has a low number of questions for the following marketing discilpines and requires more adding to make the benchmark scores more robust:
- Publishing
- Outdoor
- eCommerce
- Content Marketing
- Web Analytics
- Ad Ops
- Privacy & Ethics
- Affiliates
- Market Research & Insights
- Influencer Marketing

### Missing Quesitons
As of **23rd June 2024**, the project is missing multiple-choice questions from the following marketing discilpines:
- Brand Management
- Customer Relationship Management (CRM)
- Email Marketing
- Mobile Marketing
- Customer Experience (CX)
- Data-Driven Marketing

If there are other marketing disciplines that you think should be represented in the GenAI Marketing Benchmark database please raise an [issue](https://github.com/seanbetts/genai-marketing-benchmarks/issues) to let me know.

### Preliminary Results
These results are from a test run of the benchmarks performed on **24th July 2024**:<br>

| Provider | Model | TOTAL↓ | AV | Ad Ops | Affiliates | Audio | Cinema | Comms Planning | Marketing Effectiveness | Outdoor | Paid Search | Paid Social | Privacy & Ethics | Programmatic | Publishing | SEO | Web Analytics | eCommerce | Content Marketing | Influencer Marketing | Market Research & Insights |
| -------- | ----- | ------ | -- | ------ | ---------- | ----- | ------ | -------------- | ----------------------- | ------- | ----------- | ----------- | ---------------- | ------------ | ---------- | --- | ------------- | --------- | ----------------- | -------------------- | -------------------------- |
| Anthropic | Claude-3.5 Sonnet | **80.1%** | 72.8% | 88.0% | 93.1% | 72.3% | **65.8%** | 89.0% | **87.2%** | 59.0% | **85.3%** | **79.6%** | 87.8% | 74.8% | 43.6% | 86.6% | **81.7%** | 87.1% | 98.3% | 90.0% | 90.0% |
| Meta | Llama-3.1 405B | 79.8% | **74.1%** | **96.0%** | 93.1% | 69.1% | 61.4% | **89.8%** | 84.0% | **67.0%** | 83.5% | 75.7% | 89.8% | **76.2%** | 42.2% | 86.8% | 75.0% | 87.8% | 98.3% | 85.0% | **95.0%** |
| Meta | Llama-3.1 70B | 79.3% | 73.9% | 88.0% | **96.6%** | 72.3% | 64.8% | 89.0% | 82.3% | 60.0% | 82.1% | 74.6% | 91.8% | 72.1% | 48.5% | **87.9%** | 76.7% | 84.7% | 95.0% | 90.0% | **95.0%** |
| OpenAI | GPT-4o | 78.1% | 70.8% | 92.0% | 93.1% | **73.5%** | 50.0% | 89.0% | 81.7% | 55.8% | 82.7% | 76.2% | **93.9%** | 73.9% | 50.5% | 86.4% | **81.7%** | 83.5% | 98.3% | **100.0%** | 90.0% |
| Mistral | Mistral Large 2 | 78.0% | 70.5% | 84.0% | 89.7% | 71.7% | 58.4% | 86.6% | 84.8% | 62.1% | 81.8% | 77.9% | 89.8% | 75.7% | 44.6% | 85.9% | 78.3% | 83.5% | 98.3% | 90.0% | 90.0% |
| OpenAI | GPT-4 Turbo | 77.3% | 73.3% | 86.0% | 89.7% | 71.7% | 52.0% | 83.5% | 77.4% | 62.1% | 80.4% | 77.4% | 87.8% | 70.3% | **57.4%** | 87.2% | 70.0% | 80.0% | 98.3% | 90.0% | **95.0%** |
| Anthropic | Claude-3 Opus | 77.1% | 70.8% | 84.0% | 86.2% | 65.7% | 52.5% | 89.0% | 83.5% | 59.0% | 83.6% | 75.7% | 89.8% | 73.0% | 47.5% | 85.4% | 76.7% | 82.4% | **100.0%** | 85.0% | **95.0%** |
| OpenAI | GPT-4o Mini | 77.0% | 66.6% | 94.0% | **96.6%** | 65.7% | 59.9% | 85.8% | 79.3% | 54.7% | 82.7% | 77.9% | 87.8% | 72.1% | 44.6% | 86.6% | 73.3% | **89.4%** | 98.3% | 85.0% | 90.0% |
| Google | Gemini-1.5 Pro | 76.4% | 69.9% | 86.0% | 93.1% | 68.1% | 53.0% | 81.9% | 81.1% | 59.0% | 80.9% | 74.0% | 87.8% | 74.8% | 44.6% | 84.8% | 76.7% | 84.7% | 98.3% | 90.0% | 90.0% |
| Anthropic | Claude-3 Sonnet | 74.0% | 67.4% | 74.0% | 79.3% | 63.9% | 47.0% | 85.8% | 77.4% | 56.8% | 79.5% | 76.2% | 81.6% | 70.3% | 44.6% | 81.2% | 76.7% | 84.7% | **100.0%** | 95.0% | 90.0% |
| Anthropic | Claude-3 Haiku | 73.9% | 66.6% | 86.0% | 89.7% | 63.9% | 56.4% | 81.9% | 76.2% | 55.8% | 76.8% | 71.8% | 77.6% | 71.2% | 48.5% | 82.3% | 70.0% | 81.2% | 98.3% | 85.0% | **95.0%** |
| Mistral | Mixtral-8x22B | 71.6% | 66.6% | 90.0% | 93.1% | 63.2% | 32.7% | 81.1% | 72.6% | 56.8% | 72.7% | 70.2% | 85.7% | 72.1% | 38.6% | 83.0% | 80.0% | 78.8% | 96.7% | 90.0% | 90.0% |
| Google | Gemini-1.5 Flash | 70.2% | 64.9% | 84.0% | 93.1% | 57.8% | 41.1% | 78.0% | 72.0% | 53.7% | 76.0% | 64.1% | 83.7% | 68.5% | 38.6% | 79.2% | 66.7% | 82.4% | 93.3% | 90.0% | **95.0%** |
| Mistral | Mixtral-8x7B | 70.2% | 65.7% | 56.0% | 65.5% | 62.0% | 43.1% | 80.3% | 73.2% | 51.6% | 74.5% | 66.8% | 83.7% | 67.6% | 31.7% | 79.4% | 78.3% | 81.2% | 96.7% | 95.0% | 85.0% |
| Meta | Llama-3.1 8B | 69.4% | 62.6% | 90.0% | 93.1% | 60.8% | 45.5% | 76.4% | 75.6% | 53.7% | 69.2% | 66.8% | 89.8% | 63.1% | 44.6% | 77.9% | 58.3% | 80.0% | 93.3% | 90.0% | 90.0% |

*These marketing categories have less than 100 multiple-choice questions in the benchmarking test, so don't provide as robust an evaluation as I would like. The scores in these categories should not be taken as definitive.

## PHASE TWO - Testing Marketing Understanding

### Status: NOT STARTED

#### Aim of Phase Two
To collect and create a bank of open-ended questions across the breadth and depth of marketing that can be used to test the **understanding** LLMs have of important marketing concepts. The LLMs' responses to these open-ended questions will be graded by another LLM, with access to acredited source material that can be used as reference, on the marketing concepts tested in each open-ended question.

## PHASE THREE - Testing Marketing Capabilities

### Status: NOT STARTED

#### Aim of Phase Three
To collect and create a bank of discipline specific tasks across the breadth and depth of marketing that can be used to test the **capabilities** of LLMs to complete these tasks. The LLMs' will need to be able to complete these tasks to a pre-defined standard (TBC) to be scored as capable of completing the task.

## Ideas for Future Development
Below is a list of areas for future development:
- Categorise questions into gobal/regional/local suitability to determine how well suited the GenAI Marketing Benchmarks are outside of the UK. I suspect 90% of questions are already globally suitable.
- Get support/endorsment from marketing bodies outside of the UK (such as the [World Federation of Advertisers (WFA)](https://wfanet.org)) to expand the GenAI Marketing Benchmarks to other regions and markets.
- Build a GUI for the GenAI Marketing Benchmarks so they are more broadly accessible.
- Build a standard set of reporting dashboards to enable more accessible analysis of benchmark results.

## Supported Large Language Models
The code currently allows the user to test the following LLMs:
- Anthropic (Claude-3 Haiku, Claude-3 Sonnet, Claude-3 Opus)
- OpenAI (GPT-3.5 Turbo, GPT-4, GPT-4 Turbo, GPT-4o)
- Google (Gemini-1.0 Pro, Gemini-1.5 Flash, Gemini-1.5 Pro)
- Meta (Llama-2 7B, Llama-2 13B, Llama-2 70B, Llama-3 8B, Llama-3 70B)
- Mistral (Mistral-7B, Mixtral-8x7B, Mixtral-8x22B)

More open-source models can be easily added to the code if supported by [Together AI](https://www.together.ai) which the project uses for inference for open-source models. A list of supported open-source models is available [here](https://docs.together.ai/docs/chat-models).

## Installing the GenAI Marketing Benchmarks
Before running the GenAI Marketing Benchmarks, you need to set up the project on your local machine. Follow these steps to install and configure the project:

1. **Clone the repository**
   ```bash
   git clone https://github.com/seanbetts/genai-marketing-benchmarks.git
   cd genai-marketing-benchmarks
   ```

2. **Set up a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory of the project and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   CLAUDE_API_KEY=your_claude_api_key
   TOGETHER_API_KEY=your_together_api_key
   ```

   Replace `your_openai_api_key`, `your_claude_api_key`, and `your_together_api_key` with your actual API keys.

5. **Set up the database**
   
   The project uses SQLite for storing the questions and results. 
   
   To ensure the integrity of the GenAI Marketing Benchmarks, I am not making the database of multiple-choice questions publicly available. This will prevent these questions and answers from being included in future LLM training datasets, which could compromise the validity of the GenAI Marketing Benchmarks.

   If you would like to run your own tests please open an [issue](https://github.com/seanbetts/genai-marketing-benchmarks/issues) in the GitHub repository to request the multiple-choice questions database. The database file will need to be saved in a `Database` folder in the project root.

6. **Verify installation**
   
   Run the following command to verify that everything is set up correctly:
   ```bash
   python main.py --help
   ```

   This should display the help message for the CLI, indicating that the installation was successful.

### Troubleshooting
- If you encounter any issues with package dependencies, try updating pip and setuptools:
  ```bash
  pip install --upgrade pip setuptools
  ```
  Then, run the installation command again.
- Ensure that your Python version is 3.7 or higher. You can check your Python version with:
  ```bash
  python --version
  ```
- If you're having trouble with API keys, make sure they are correctly set in your `.env` file and that the file is in the root directory of the project.

For any other issues, open an [issue](https://github.com/seanbetts/genai-marketing-benchmarks/issues) in the GitHub repository.

## Running the GenAI Marketing Benchmarks
The GenAI Marketing Benchmarks can be run in two modes: interactive and non-interactive. Both modes are accessible through the command-line interface (CLI).

### Prerequisites
Before running the benchmarks, ensure you have:

1. Installed all required dependencies (see [Installation section](#installation) section).
2. Set up your `.env` file with the necessary API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   CLAUDE_API_KEY=your_claude_api_key
   TOGETHER_API_KEY=your_together_api_key
   ```

### Interactive Mode
To run the benchmarks in interactive mode, simply execute:
```bash
python main.py
```

This will guide you through a series of prompts to:
- Select the models to test
- Choose the categories of questions
- Specify the number of questions and rounds
- Confirm the estimated cost before running

### Non-Interactive Mode
For automated or scripted runs, use the non-interactive mode with command-line arguments:
```bash
python main.py --non-interactive [OPTIONS]
```

Available options:
- `--num-questions`: Number of questions to test (use 'all' for all available questions)
- `--num-rounds`: Number of rounds to run
- `--models` or `-m`: Models to use for testing (can be specified multiple times)
- `--categories` or `-c`: Categories to test (can be specified multiple times)

Example:
```bash
python main.py --non-interactive --num-questions 100 --num-rounds 2 --models "GPT-4" "Claude-3 Opus" --categories "SEO" "PPC"
```

This command will:
- Run in non-interactive mode
- Test 100 questions
- Perform 2 rounds of testing
- Use the GPT-4 and Claude-3 Opus models
- Test questions from the SEO and PPC categories

### Viewing Results
After running the benchmarks, results will be saved in the SQLite database. You can analyze these results using SQL queries or export them for further analysis.

## Testing Methodology

### Marketing Knowledge
The benchmarking methodology uses the [AI Harness](https://github.com/EleutherAI/lm-evaluation-harness/tree/e47e01beea79cfe87421e2dac49e64d499c240b4) prompt implementation. Below is an example of the prompt used to ask the multiple choice questions:

*Choose the correct answer for the following marketing multiple-choice question. ANSWER ONLY with a SINGLE letter of the correct choice.<br><br>
Question: Which channel is considered most effective for long-term brand building?<br><br>
Choices:<br>
A. Radio<br>
B. TV<br>
C. Online ads<br>
D. Print<br><br>
Answer:*

### Marketing Understanding
TBC

### Marketing Capabilities
TBC