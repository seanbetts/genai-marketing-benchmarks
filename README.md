# Creating GenAI Marketing Benchmarks (Beta)

## Introduction

Generative AI (GenAI) has the potential to transform the marketing industry, yet there is currently no comprehensive way to assess the marketing capabilities of Large Language Models (LLMs) and other GenAI technologies. This project aims to fill that gap by creating benchmark tests that evaluate GenAI technnology's knowledge, understanding, and ability to perform marketing tasks.

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
- Influecer Marketing

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
These results are from a test run of the benchmarks performed on **23rd June 2024**:<br>

| Provider | Model | TOTAL↓ | AV | Ad Ops* | Affiliates* | Audio | Cinema | Comms Planning | Marketing Effectiveness | Outdoor* | Paid Search | Paid Social | Privacy & Ethics* | Programmatic | Publishing* | SEO | Web Analytics* | eCommerce* | Content Marketing* | Influencer Marketing* | Market Research & Insights* |
| -------- | ----- | ------ | -- | ------ | ---------- | ----- | ------ | -------------- | ----------------------- | ------- | ----------- | ----------- | ---------------- | ------------ | ---------- | --- | ------------- | --------- | ----------------- | -------------------- | -------------------------- |
| Anthropic | Claude-3.5 Sonnet | **80.1%** | 72.8% | 88.0% | 93.1% | 72.3% | **65.8%** | **89.0%** | **87.2%** | 59.0% | **85.3%** | **79.6%** | 87.8% | **74.8%** | 43.6% | 86.6% | **81.7%** | **87.1%** | 98.3% | 90.0% | 90.0% |
| OpenAI | GPT-4o | 78.1% | 70.8% | 92.0% | 93.1% | **73.5%** | 50.0% | **89.0%** | 81.7% | 55.8% | 82.7% | 76.2% | **93.9%** | 73.9% | 50.5% | 86.4% | **81.7%** | 83.5% | 98.3% | **100.0%** | 90.0% |
| OpenAI | GPT-4 Turbo | 77.3% | **73.3%** | 86.0% | 89.7% | 71.7% | 52.0% | 83.5% | 77.4% | **62.1%** | 80.4% | 77.4% | 87.8% | 70.3% | **57.4%** | **87.2%** | 70.0% | 80.0% | 98.3% | 90.0% | **95.0%** |
| Anthropic | Claude-3 Opus | 77.1% | 70.8% | 84.0% | 86.2% | 65.7% | 52.5% | **89.0%** | 83.5% | 59.0% | 83.6% | 75.7% | 89.8% | 73.0% | 47.5% | 85.4% | 76.7% | 82.4% | **100.0%** | 85.0% | **95.0%** |
| Meta | Llama-3 70B | 77.0% | 71.4% | **96.0%** | **96.6%** | 70.5% | 56.9% | 85.0% | 78.7% | 60.0% | 80.6% | 72.9% | 89.8% | 69.4% | 47.5% | 85.1% | 76.7% | 82.4% | 93.3% | 85.0% | **95.0%** |
| Google | Gemini-1.5 Pro | 76.4% | 69.9% | 86.0% | 93.1% | 68.1% | 53.0% | 81.9% | 81.1% | 59.0% | 80.9% | 74.0% | 87.8% | **74.8%** | 44.6% | 84.8% | 76.7% | 84.7% | 98.3% | 90.0% | 90.0% |
| Anthropic | Claude-3 Sonnet | 74.0% | 67.4% | 74.0% | 79.3% | 63.9% | 47.0% | 85.8% | 77.4% | 56.8% | 79.5% | 76.2% | 81.6% | 70.3% | 44.6% | 81.2% | 76.7% | 84.7% | **100.0%** | 95.0% | 90.0% |
| Anthropic | Claude-3 Haiku | 73.9% | 66.6% | 86.0% | 89.7% | 63.9% | 56.4% | 81.9% | 76.2% | 55.8% | 76.8% | 71.8% | 77.6% | 71.2% | 48.5% | 82.3% | 70.0% | 81.2% | 98.3% | 85.0% | **95.0%** |
| Mistral | Mixtral-8x22B | 71.6% | 66.6% | 90.0% | 93.1% | 63.2% | 32.7% | 81.1% | 72.6% | 56.8% | 72.7% | 70.2% | 85.7% | 72.1% | 38.6% | 83.0% | 80.0% | 78.8% | 96.7% | 90.0% | 90.0% |
| Google | Gemini-1.5 Flash | 70.2% | 64.9% | 84.0% | 93.1% | 57.8% | 41.1% | 78.0% | 72.0% | 53.7% | 76.0% | 64.1% | 83.7% | 68.5% | 38.6% | 79.2% | 66.7% | 82.4% | 93.3% | 90.0% | **95.0%** |
| Mistral | Mixtral-8x7B | 70.2% | 65.7% | 56.0% | 65.5% | 62.0% | 43.1% | 80.3% | 73.2% | 51.6% | 74.5% | 66.8% | 83.7% | 67.6% | 31.7% | 79.4% | 78.3% | 81.2% | 96.7% | 95.0% | 85.0% |
| Meta | Llama-3 8B | 69.3% | 61.2% | 72.0% | 93.1% | 57.2% | 45.5% | 74.8% | 72.0% | 57.9% | 73.9% | 68.5% | 83.7% | 66.7% | 37.6% | 77.4% | 66.7% | 81.2% | 91.7% | 90.0% | 90.0% |

*These marketing categories have less than 100 multiple-choice questions in the benchmarking test, so don't provide as robust an evaluation as I would like. The scores in these categories should not be taken as definitive.

## PHASE TWO - Testing Marketing Understanding

### Status: NOT STARTED

#### Aim
Collect and create a bank of open-ended questions across the breadth and depth of marketing that can be used to test the **understanding** LLMs have of important marketing concepts. The LLMs' responses to these open-ended questions will be graded by another LLM, with access to acredited source material that can be used as reference, on the marketing concepts tested in each open-ended question.

## PHASE THREE - Testing Marketing Capabilities

### Status: NOT STARTED

#### Aim
Collect and create a bank of discipline specific tasks across the breadth and depth of marketing that can be used to test the **capabilities** of LLMs to complete these tasks. The LLMs' will need to be able to complete these tasks to a pre-defined standard (TBC) to be scored as capable of completing the task.

## Large Language Models
The code currently allows the user to test the following LLMs:
- Anthropic (Claude-3 Haiku, Claude-3 Sonnet, Claude-3 Opus)
- OpenAI (GPT-3.5 Turbo, GPT-4, GPT-4 Turbo, GPT-4o)
- Google (Gemini-1.0 Pro, Gemini-1.5 Flash, Gemini-1.5 Pro)
- Meta (Llama-2 7B, Llama-2 13B, Llama-2 70B, Llama-3 8B, Llama-3 70B)
- Mistral (Mistral-7B, Mixtral-8x7B, Mixtral-8x22B)

More open source models can be easily added to the code if supported by [Together AI](https://www.together.ai) which the project uses for inference for open source models.

## Testing Methodology - Marketing Knowledge
The benchmarking methodology uses the [AI Harness](https://github.com/EleutherAI/lm-evaluation-harness/tree/e47e01beea79cfe87421e2dac49e64d499c240b4) prompt implementation. Below is an example of the prompt used to ask the multiple choice questions:

Choose the correct answer for the following multiple-choice question. ANSWER ONLY with a SINGLE letter of the correct choice.<br><br>
Question: Which channel is considered most effective for long-term brand building?<br><br>
Choices:<br>
A. Radio<br>
B. TV<br>
C. Online ads<br>
D. Print<br><br>
Answer:

## Testing Methodology - Marketing Understanding

TBC

## Testing Methodology - Marketing Capabilities

TBC