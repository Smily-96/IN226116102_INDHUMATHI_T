# Prompt Engineering using LangChain Prompt Templates

## 📌 Internship Task
This project is part of the **Data Science Internship – February 2026**.

## 🎯 Objective
To build a mini prompt engine using LangChain by replacing hardcoded prompts with reusable prompt templates.

---

## 🚀 Features Implemented

### ✅ Task 1: Replace Hardcoded Prompt
Converted static prompt into reusable `PromptTemplate`.

### ✅ Task 2: Multi-Input Prompt System
Handled multiple inputs:
- topic
- audience
- tone

### ✅ Task 3: Prompt Variations Engine
Created multiple prompt styles:
- Teaching
- Interview
- Storytelling

### ✅ Task 4: ChatPromptTemplate System
Built role-based prompts:
- Teacher
- Interviewer
- Motivator

### ✅ Task 5: Input Validation Layer
Validated:
- audience (beginner, intermediate, expert)
- tone (formal, casual, fun)

### ✅ Task 6: Prompt Generator App
Created dynamic function:
```python
generate_prompt(topic, audience, tone, style)