
# LLM Evaluation with LangSmith

## Overview

This project provides a structured and automated pipeline for evaluating Large Language Model (LLM) responses using [LangSmith](https://smith.langchain.com). It enables comparison of model outputs against reference answers to assess **accuracy**, **correctness**, and overall performance.

---

## Features

* **Custom LLM Evaluation**: Evaluate model responses using tailored evaluators (e.g., accuracy, correctness).
* **Data Ingestion**: Easily load datasets into LangSmith for batch evaluation.
* **LLM Caching**: Improve performance through in-memory caching of repeated evaluations.

---

## Folder Structure

```
langchain_sdk/
├── evaluator.py         # Main evaluation script for LLM responses
├── ingest_data.py       # Script to ingest datasets into LangSmith
├── readme.md            # Project documentation
├── llm/
    ├── __init__.py
    └── gemini.py        # Configuration for the Gemini LLM (API key, model settings)
├── prompt/
    ├── __init__.py
    └── prompt.py        # Shared prompts and instructions
├── schema/
    ├── __init__.py
    └── models.py        # Data models for structured input/output
```

---

## How to Run
First, navigate to the `langchain_sdk` directory:
```bash
cd langchain_sdk
```

### 1. Ingest Data

```bash
uv run ingest_data.py
```

### 2. Run Evaluation

```bash
uv run evaluator.py
```

---

## Key Components

### 1. Evaluators

* **Accuracy**: Checks conceptual similarity between the LLM output and reference answers.
* **Correctness**: Grades answers based on defined criteria or expected structure.

### 2. LLM Configuration

Located in `llm/gemini.py`, this file handles:

* API key management
* Model selection and configuration

### 3. Prompts

All reusable prompts and LLM instructions are defined in `prompt/prompt.py`.

---

## References

* [Hands-on Guide to LLM Caching with LangChain](https://adasci.org/hands-on-guide-to-llm-caching-with-langchain-to-boost-llm-responses/)
* [LangSmith Evaluation Tutorials](https://docs.smith.langchain.com/evaluation/tutorials/evaluation)

