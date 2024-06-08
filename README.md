# Creating GenAI Marketing Benchmarks (Beta)

## Introduction

Generative AI (GenAI) has the potential to transform the marketing industry, yet there is currently no comprehensive way to assess the marketing capabilities of GenAI models. This project aims to fill that gap by creating a benchmark that evaluates GenAI models' knowledge, understanding, and ability to perform marketing tasks.

## The Challenge

The marketing industry lacks standardized benchmarks to evaluate GenAI models specifically for marketing capabilities. While there are existing benchmarks for general AI capabilities, these do not adequately cover the breadth and depth required for marketing.

### Key Issues:
- Existing benchmarks primarily test general knowledge, not marketing-specific knowledge, understanding or reasoning.
- Limited number of marketing-related questions in current benchmarks (e.g., the [MMMU Benchmark](https://mmmu-benchmark.github.io) has only 216 marketing questions and 12 advertising images).
- Clients, platforms, and agencies need reliable benchmarks to select, develop, and fine-tune GenAI tools.

## Project Objective

To create a comprehensive bank of questions, tests, and tasks that can be used to benchmark GenAI models knowledge, understanding and capabilities across all aspects of marketing.

### Benefits:
- Provides a valuable resource for the marketing industry.
- Offers an objective way to test GenAI's marketing knowledge and capabilities.
- Enables comparison between different GenAI models.
- Assesses new GenAI models and features as they are released.
- Monitors improvements in GenAI capabilities over time.

##  GenAI Marketing Benchmark - Knowledge Questions
![GenAI Marketing Benchmark Questions](https://github.com/seanbetts/genai-marketing-benchmarks/blob/main/Images/Questions%20_June_2024.png)

**PROJECT PHASE ONE: IN PROGRESS** - collect and create a bank of multiple-choice questions across the breadth and depth of marketing that can be used to test the marketing **knowledge** of LLMs. The LLMs' responses to these multiple-choice questions will be scored on whether they get the right answer or not.

The database of marketing questions currently contains 1,500+ multiple-choice questions to test the marketing knowledge of generative AI models. The questions are currently focused around Comms Planning, Marketing Effectiveness and Media. The question bank needs broadening out to include all marketing disciplines.

## GenAI Marketing Benchmark - Understanding Questions

**PROJECT PHASE TWO: NOT STARTED** - collect and create a bank of open-ended questions across the breadth and depth of marketing that can be used to test the **understanding** LLMs have of important marketing concepts. The LLMs' responses to these open-ended questions will be graded by another LLM, with access to acredited source material that can be used as reference, on the marketing concepts tested in each open-ended question.

## GenAI Marketing Benchmark - Capabilities Questions

**PROJECT PHASE THREE: NOT STARTED** - collect and create a bank of discipline specific tasks across the breadth and depth of marketing that can be used to test the **capabilities** of LLMs to complete these tasks. The LLMs' will need to be able to complete these tasks to a pre-defined standard (TBC) to be scored as capable of completing the task.

## Models
The code currently allows the testing of the following GenAI models:
- Anthropic (Claude-3 Haiku, Claude-3 Sonnet, Claude-3 Opus)
- OpenAI (GPT-3.5 Turbo, GPT-4, GPT-4 Turbo, GPT-4o)
- Google (Gemini-1.0 Pro, Gemini-1.5 Flash, Gemini-1.5 Pro)
- Meta (Llama-2-7B, Llama-2-13B, Llama-2-70B, Llama-3-8B, Llama-3-70B)
- Mistral (Mistral-7B, Mixtral-8x7B, Mixtral-8x22B)
- Microsoft (Phi-3 Mini, Phi-3 Small, Phi-3 Medium)

## Knowledge Testing Methodology
The benchmarking methodology uses the [AI Harness](https://github.com/EleutherAI/lm-evaluation-harness/tree/e47e01beea79cfe87421e2dac49e64d499c240b4) prompt implementation. Below is an example of the prompt used to ask the multiple choice questions:

Choose the correct answer for the following multiple-choice question. ANSWER ONLY with a SINGLE letter of the correct choice.<br><br>
Question: Which channel is considered most effective for long-term brand building?<br><br>
Choices:<br>
A. Radio<br>
B. TV<br>
C. Online ads<br>
D. Print<br><br>
Answer:

## Understanding Testing Methodology

TBC

## Capabilities Testing Methodology

TBC