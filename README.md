# Creating GenAI Marketing Benchmarks (Beta)

## Introduction

Generative AI (GenAI) has the potential to transform the marketing industry, yet there is currently no comprehensive way to assess the marketing capabilities of GenAI models. This project aims to fill that gap by creating a benchmark that evaluates GenAI models' knowledge, understanding, and ability to perform marketing tasks.

## The Challenge

The marketing industry lacks standardized benchmarks to evaluate GenAI models specifically for marketing capabilities. While there are existing benchmarks for general AI capabilities, these do not adequately cover the breadth and depth required for marketing.

### Key Issues:
- Existing benchmarks primarily test general knowledge, not marketing-specific knowledge, understanding or reasoning.
- Limited number of marketing-related questions in current benchmarks (e.g., the [MMMU Benchmark](https://mmmu-benchmark.github.io) has only **216** marketing questions and **12** advertising images).
- Clients, platforms, and agencies need reliable benchmarks to select, develop, and fine-tune GenAI tools.

## Project Objective

To create a comprehensive bank of questions, tests, and tasks that can be used to benchmark GenAI models knowledge, understanding and capabilities across all aspects of marketing.

### Benefits:
- Provides a valuable resource for the marketing industry.
- Offers an objective way to test GenAI's marketing knowledge and capabilities.
- Enables comparison between different GenAI models.
- Assesses new GenAI models and features as they are released.
- Monitors improvements in GenAI capabilities over time.

##  PHASE ONE - Knowledge Questions
![GenAI Marketing Benchmark Questions](https://github.com/seanbetts/genai-marketing-benchmarks/blob/main/Images/Questions%20_June_2024.png)

### IN PROGRESS
Collect and create a bank of multiple-choice questions across the breadth and depth of marketing that can be used to test the marketing **knowledge** of LLMs. The LLMs' responses to these multiple-choice questions will be scored on whether they get the right answer or not.

The database of marketing questions currently contains **1,600+** multiple-choice questions to test the marketing knowledge of generative AI models. The questions are currently focused around Comms Planning, Marketing Effectiveness and Media. The question bank needs broadening out to include all marketing disciplines.

### Missing Quesitons
The project is currently missing multiple-choice quesitons from the following marketing discilpines:
- Content Marketing
- Influencer Marketing
- Brand Management
- Customer Relationship Management (CRM)
- Market Research and Insights
- Public Relations (PR)
- Email Marketing
- Mobile Marketing
- Customer Experience (CX)
- Data-Driven Marketing

If there are other marketing disciplines that you think should be represented in the GenAI Marketing Benchmark database please raise an [issue](https://github.com/seanbetts/genai-marketing-benchmarks/issues) to let me know.

### Preliminary Results
These results are from an initial test run of the benchmarks performed on **8th June 2024**:<br>

| Model           | TOTAL↓ | AV     | Ad Ops | Affiliates | Audio | Cinema | Comms Planning | Marketing Effectiveness | Outdoor | Paid Search | Paid Social | Privacy & Ethics | Programmatic | Publishing | SEO   | Web Analytics | eCommerce |
|-----------------|-------|--------|--------|------------|-------|--------|----------------|-------------------------|---------|-------------|-------------|------------------|--------------|------------|-------|---------------|-----------|
| Claude-3 Opus   | **83.0%**  | 73.3%  | 90.0%  | 93.1%      | **60.0%** | 68.4%  | **85.6%**          | **85.9%**                   | 70.0%   | **85.6%**       | **74.2%**       | 86.0%            | **77.0%**        | 60.0%      | 86.0% | 78.3%         | 97.0%     |
| GPT-4o          | 81.9%  | 63.3%  | 88.0%  | **96.6%**     | 45.0% | **73.7%**  | 84.1%          | 83.8%                   | **75.0%**   | 82.4%       | 72.5%       | **92.0%**            | 73.5%        | **64.0%**      | 86.0% | **83.3%**        | **100.0%**    |
| GPT-4 Turbo     | 81.0%  | 70.0%  | **94.0%**  | 93.1%      | 40.0% | 68.4%  | 81.3%          | 75.8%                   | 65.0%   | 82.2%       | 72.0%       | 86.0%            | 71.7%        | 60.0%      | **88.3%** | 75.0%         | 98.5%     |
| Claude-3 Sonnet | 76.4%  | 66.7%  | 76.0%  | 75.9%      | 45.0% | 42.1%  | 80.4%          | 74.8%                   | 65.0%   | 77.1%       | 73.6%       | 84.0%            | 68.1%        | 48.0%      | 81.0% | 75.0%         | 98.5%     |
| Claude-3 Haiku  | 76.3%  | **76.7%**  | 78.0%  | 86.2%      | 40.0% | 57.9%  | 81.3%          | 81.8%                   | 70.0%   | 72.8%       | 73.1%       | 80.0%            | 68.1%        | 56.0%      | 81.0% | 68.3%         | 98.5%     |
| GPT-3.5 Turbo   | 74.2%  | 56.7%  | 84.0%  | 89.7%      | 40.0% | 52.6%  | 78.5%          | 68.7%                   | 50.0%   | 73.1%       | 68.1%       | 80.0%            | 63.7%        | 60.0%      | 81.2% | 70.0%         | 95.5%     |
| Gemini-1.5 Flash | 73.5% | 66.7% | 70.0% | 82.8% | 35.0% | 42.1% | 75.7% | 73.7% | 50.0% | 73.4% | 66.5% | 82.0% | 62.8% | 56.0% | 80.5% | 71.7% | 98.5% |

## PHASE TWO - Understanding Questions

### NOT STARTED
Collect and create a bank of open-ended questions across the breadth and depth of marketing that can be used to test the **understanding** LLMs have of important marketing concepts. The LLMs' responses to these open-ended questions will be graded by another LLM, with access to acredited source material that can be used as reference, on the marketing concepts tested in each open-ended question.

## PHASE THREE - Capabilities Questions

### NOT STARTED
Collect and create a bank of discipline specific tasks across the breadth and depth of marketing that can be used to test the **capabilities** of LLMs to complete these tasks. The LLMs' will need to be able to complete these tasks to a pre-defined standard (TBC) to be scored as capable of completing the task.

## Models
The code currently allows the testing of the following GenAI models:
- Anthropic (Claude-3 Haiku, Claude-3 Sonnet, Claude-3 Opus)
- OpenAI (GPT-3.5 Turbo, GPT-4, GPT-4 Turbo, GPT-4o)
- Google (Gemini-1.0 Pro, Gemini-1.5 Flash, Gemini-1.5 Pro)
- Meta (Llama-2-7B, Llama-2-13B, Llama-2-70B, Llama-3-8B, Llama-3-70B)
- Mistral (Mistral-7B, Mixtral-8x7B, Mixtral-8x22B)

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