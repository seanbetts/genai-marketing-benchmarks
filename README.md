# Creating GenAI Marketing Benchmarks

## Introduction

Generative AI (GenAI) has the potential to transform the marketing industry, yet there is currently no comprehensive way to assess the marketing capabilities of GenAI models. This project aims to fill that gap by creating a benchmark that evaluates GenAI models' knowledge, understanding, and ability to perform marketing tasks.

## The Challenge

The marketing industry lacks standardized benchmarks to evaluate GenAI models specifically for marketing capabilities. While there are existing benchmarks for general AI capabilities, these do not adequately cover the breadth and depth required for marketing.

### Key Issues:
- Existing benchmarks primarily test general knowledge, not marketing-specific knowledge, understanding or reasoning.
- Limited number of marketing-related questions in current benchmarks (e.g., the [MMMU Benchmark](https://mmmu-benchmark.github.io) has only 216 marketing questions and 12 advertising images).
- Clients, platforms, and agencies need reliable benchmarks to select, develop, and fine-tune GenAI tools.

## Project Objective

To create a comprehensive bank of questions and tests that can be used to benchmark GenAI models knowledge, understanding and ability to complte tasks across various aspects of marketing.

### Benefits:
- Provides a valuable resource for the marketing industry.
- Offers an objective way to test GenAI's marketing knowledge and capabilities.
- Enables comparison between different GenAI models.
- Assesses new GenAI models and features as they are released.
- Monitors improvements in GenAI capabilities over time.

##  GenAI Marketing Benchmark Questions
![GenAI Marketing Benchmark Questions](https://github.com/seanbetts/genai-marketing-benchmarks/blob/main/Images/Questions%20_June_2024.png)

The database of marketing questions currently contains 1,500+ multiple choice questions to test the marketing knowledge of generative AI models. The questions are currently focused around Comms Planning, Marketing Effectiveness and Media. The question bank needs broadening out to include all marketing disciplines.

## Models
The code currently allows the testing of the following GenAI models:
- Anthropic (Claude-3 Haiku 07-03-24, Claude-3 Sonnet 29-02-24, Claude-3 Opus 29-02-24)
- OpenAI (GPT-3.5 Turbo 25-01-24, GPT-4 13-06-24, GPT-4 Turbo 09-04-24, GPT-4o 13-05-24)
- Google (Gemini-1.0 Pro, Gemini-1.5 Flash, Gemini-1.5 Pro)
- Meta (Llama-2-7B, Llama-2-13B, Llama-2-70B, Llama-3-8B, Llama-3-70B)
- Mistral (Mistral-7B, Mixtral-8x7B, Mixtral-8x22B)
- Microsoft (Phi-3 Mini, Phi-3 Small, Phi-3 Medium)
