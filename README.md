# YouTube AI Tutor (FYP)

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![AI/RAG](https://img.shields.io/badge/AI-Retrieval_Augmented_Generation-005571?style=flat)

An interactive, AI-driven educational platform that transforms standard YouTube content into a personalized tutoring experience. Developed as a Final Year Project, this application uses a Retrieval-Augmented Generation (RAG) architecture built entirely on **Streamlit** to process videos, extract knowledge, and provide an interactive Q&A interface.

## System Architecture

This project utilizes a unified Python stack, leveraging Streamlit for both the frontend interface and backend logic:

* **Framework:** Streamlit for a highly interactive, responsive, and data-centric user interface.
* **Intelligence Layer:** AI agents tasked with transcription, summarization, and generating pedagogical responses.
* **Data Retrieval:** A RAG pipeline that grounds the AI's responses strictly in the context of the processed YouTube video, minimizing hallucinations.
* **Language:** Pure Python, ensuring seamless integration between the UI, data processing, and machine learning models.

## Key Features

* **Interactive Chat Interface:** Ask specific questions about any processed YouTube video using Streamlit's native chat elements.
* **Context-Aware Learning:** The RAG pipeline ensures that the AI tutor's answers are accurate and directly tied to the video's transcript and metadata.
* **Rapid Processing:** Quickly ingest YouTube URLs, extract transcripts, and build searchable knowledge bases on the fly.
* **Visual Summaries:** Clean, scannable summaries and breakdowns of complex topics directly within the app.

## Prerequisites

Ensure you have the following installed before running the project:
* Python 3.10+
* Git

## Local Development Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/mubashiriftkhar/FYP-YouTube-Tutor.git](https://github.com/mubashiriftkhar/FYP-YouTube-Tutor.git)
cd FYP-YouTube-Tutor
