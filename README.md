# AI-Driven Assessment Platform for Embedded/Automotive Engineers

This project is an automated, AI-driven assessment platform designed to evaluate the skills of junior embedded and automotive engineers. It combines adaptive coding challenges, static and dynamic code analysis, and conversational AI to provide a comprehensive evaluation of a candidate's abilities.

## Core Components

- **Assessment Orchestrator**: A backend service that manages the candidate workflow, selects tasks, and stores results.
- **Question & Task Engine**: A system for generating parameterized tasks, including firmware snippets, failing tests, and log analysis exercises.
- **Execution Sandbox**: A containerized environment for running code with cross-compilers, simulators, and unit-testing harnesses.
- **AI Evaluation Module**: An LLM-based module for grading reasoning, checking explanations, and detecting plagiarism.
- **Static Analysis & Safety Checks**: A component for running MISRA, CERT C, and other static analysis tools.
- **Conversational Interviewer**: An LLM-based interviewer that asks follow-up questions and assesses communication skills.
- **Human Review Dashboard**: A web interface for human reviewers to validate AI decisions and view evidence.
- **Reporting & Learning Plan Generator**: A tool for creating candidate reports and personalized learning plans.

## Getting Started

### Prerequisites

- Python 3.9+
- Docker

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Set up the backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Run the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Tech Stack

- **Backend**: FastAPI
- **LLM**: GPT-4 (or similar)
- **Code Execution**: Docker, QEMU
- **Static Analysis**: clang-tidy, Cppcheck
- **Unit Testing**: Unity, CppUTest
- **Frontend**: React, Tailwind CSS (to be developed)
- **Database**: PostgreSQL