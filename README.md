# Sri Lankan NIC Validator - DFA Implementation

Hey! This is my Automata Theory assignment where I built a **DFA** (Deterministic Finite Automaton) to validate Sri Lankan NIC numbers. Basically took what we learned in class about finite automata and applied it to something actually useful.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Automata Theory Background](#automata-theory-background)
- [NIC Format Specification](#nic-format-specification)
- [DFA Specification](#dfa-specification)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Testing](#testing)
- [Educational Value](#educational-value)
- [Limitations](#limitations)
- [Sample Inputs & Outputs](#sample-inputs--outputs)
- [Technologies Used](#technologies-used)

---

## Project Overview

So here's what I built - a DFA that checks if Sri Lankan NIC numbers are valid. The project has three main parts:

1. **Python Backend**: Where the actual DFA lives, plus a Flask API to use it
2. **React Frontend**: A simple web interface to test it out
3. **Test Suite**: 50+ test cases to make sure everything works

### About Sri Lankan NICs

There are two formats:
- **Old format** (before 2016): 9 digits then V or X (like `981234567V`)
- **New format** (from 2016): Just 12 digits (like `199812345678`)

My DFA only checks if the format is correct - not if the NIC is real or if the numbers make sense. That's perfect for a DFA since we don't need anything fancy like memory or complex logic.

---

## Automata Theory Background

### Quick Recap - What's a Finite Automaton?

From our lectures, a finite automaton has:
- Some states to move between
- An alphabet (the characters it can read)
- Transition rules (how to move from state to state)
- A starting point
- Some accepting states (the "good" endings)

### Why DFA and not NFA?

I used a **DFA** (Deterministic) instead of NFA because:
- Each state has exactly one place to go for each character
- No confusion about which path to take
- Same input = same result every time
- Easier to code honestly

### Why DFA Works for This

NIC validation is actually perfect for a DFA:
1. The input length is fixed (10 or 12 characters)
2. We just read it left to right, one character at a time
3. Either it's valid or it's not - no gray area
4. We don't need to remember anything except what state we're in
5. Super fast - just O(n)

---

## NIC Format Specification

### Old NIC Format (Pre-2016)

**Pattern**: 9 digits + V or X

Like: `981234567V` or `801234567X`

Total = 10 characters

### New NIC Format (2016 Onwards)

**Pattern**: Just 12 digits

Like: `199812345678`

### What I'm NOT Checking

This DFA ONLY checks the pattern. It doesn't check:
- If the year makes sense
- If the day of year is valid (001-366)
- Gender stuff
- If the NIC actually exists in some database
- Any checksum digits

**Why?** Because checking all that would need way more than a DFA. This is just pattern matching - which is exactly what DFAs are good at!

---

## DFA Specification

### Formal Definition (for the assignment)

**M = (Q, Σ, δ, q₀, F)**

- **Q** (States): {q0, q1, q2, ..., q13, q_reject} - that's 15 states total
- **Σ** (Alphabet): {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, V, X} - digits and the two suffixes
- **δ** (Transition function): see the table below
- **q₀** (Start state): q0
- **F** (Accept states): {q10, q13} - two ways to accept

### What Each State Does

| State | What's happening |
|-------|------------------|
| `q0` | Starting point |
| `q1` - `q9` | Reading the first 9 digits |
| `q10` | Accept! (got 9 digits + V/X) |
| `q11` | Reading the 10th digit |
| `q12` | Reading the 11th digit |
| `q13` | Accept! (got all 12 digits) |
| `q_reject` | Something went wrong, reject it |

### State Transition Diagram

```
        digit        digit        digit              digit
q0 ──────────> q1 ──────────> q2 ─────> ... ─────> q9
                                                     │
                                                     ├──V/X──> q10 (ACCEPT: Old NIC)
                                                     │
                                                     └─digit─> q11 ──digit──> q12 ──digit──> q13 (ACCEPT: New NIC)

Any invalid transition → q_reject
```

### How the Transitions Work

**Main idea**:

- Keep reading digits: q0 → q1 → q2 → ... → q9
- After 9 digits (at q9), two options:
  - See V or X? → Go to q10 and ACCEPT (old NIC)
  - See another digit? → Keep going to q11 → q12 → q13 and ACCEPT (new NIC)
- Anything else? → Straight to q_reject

Basically, after reading 9 digits, we check what comes next to figure out which format it is.

---


## Installation & Setup

### What You Need

- Python 3.8+
- Node.js 14+
- npm

### Backend Setup

Open a terminal:

```bash
cd backend

# Make a virtual environment (keeps things clean)
python -m venv venv

# Activate it
venv\Scripts\activate    # Windows
source venv/bin/activate  # Mac/Linux

# Install stuff
pip install -r requirements.txt

# Run the server
python app.py
```

Backend will be at `http://localhost:5000`

### Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm start
```

Browser should open automatically to `http://localhost:3000`

---

## Usage

### Testing from Terminal

You can run the DFA directly:

```bash
cd backend
python dfa.py
```

It'll show you step-by-step what the DFA is doing - pretty cool to see it in action!

### Using the Web Interface

This is the easier way:

1. Make sure both backend and frontend are running
2. Go to `http://localhost:3000`
3. Type in a NIC number
4. Hit "Validate NIC"
5. See if it accepts or rejects

There's also a checkbox to show the state transitions if you want to see the DFA working.

### API Endpoints (if you're curious)

The Flask backend has 4 endpoints:

- `POST /validate-nic` - validates a NIC
- `POST /validate-nic-trace` - same but shows all the state transitions
- `GET /dfa-info` - returns the DFA specification
- `GET /health` - just checks if the server is running

**Request**:
```json
{
  "nic": "981234567V"
}
```

**Response**:
```json
{
  "result": "ACCEPT",
  "final_state": "q10",
  "input": "981234567V",
  "format": "Old NIC (9 digits + V/X)"
}
```

#### 2. Validate with Trace

**Endpoint**: `POST /validate-nic-trace`

**Request**:
```json
{
  "nic": "199812345678"
}
```

**Response**:
```json
{
  "result": "ACCEPT",
  "final_state": "q13",
  "input": "199812345678",
  "trace": [
    {"step": 0, "input": "", "state": "q0"},
    {"step": 1, "input": "1", "state": "q1"},
    {"step": 2, "input": "9", "state": "q2"},
    ...
    {"step": 12, "input": "8", "state": "q13"}
  ]
}
```

#### 3. DFA Information

**Endpoint**: `GET /dfa-info`

---

## Testing

### Running the Tests

```bash
cd backend
python test_cases.py
```

### What's Tested

I wrote 50+ test cases covering:

1. Valid old NICs (with V)
2. Valid old NICs (with X)
3. Valid new NICs (12 digits)
4. Wrong length
5. Invalid characters
6. V/X in wrong positions
7. Edge cases (empty string, spaces, etc.)

All tests pass! Got 100% success rate.

---

## What I Learned

Building this project helped me understand:

**Automata Theory Stuff:**
- How to design a DFA from scratch
- State transitions and how they work in practice
- When to accept vs reject
- How DFAs recognize patterns

**Programming Stuff:**
- Building a REST API with Flask
- Making a React frontend
- Writing good tests
- Connecting backend and frontend

**Problem Solving:**
- Breaking a real problem into states
- Thinking about what a DFA can and can't do
- Validation logic

---

## Limitations

### What This Doesn't Do

My DFA only checks the pattern. It doesn't check:
- If the birth year makes sense
- If the day of year is valid (001-366)
- Gender stuff encoded in the digits
- If the NIC exists in any database
- Checksum validation

### Why Not?

Because DFAs can't do:
- Math operations (like calculating age)
- Comparisons with external data (like current year)
- Remember more than just the current state
- Understand what the numbers mean

Those need more powerful models like pushdown automata or actual programming logic. DFAs are just for pattern matching!

---

## Examples

### These Should Work (ACCEPT)

| Input | Type |
|-------|------|
| `981234567V` | Old NIC |
| `801234567X` | Old NIC |
| `199812345678` | New NIC |
| `200012345678` | New NIC |

### These Should Fail (REJECT)

| Input | Why it fails |
|-------|-------------|
| `12345678` | Too short |
| `12345678A` | A is not valid (only V or X) |
| `123456789v` | lowercase v |
| `1234567890` | 10 digits but no V/X |
| `12345678901` | 11 digits (wrong length) |
| `1234567890123` | 13 digits (too long) |
| `123 456 789V` | Has spaces |
| `` | Empty |

---

## Tech Stack

**Backend:**
- Python 3.8+
- Flask (for the API)
- Flask-CORS (so frontend can talk to backend)

**Frontend:**
- React 18
- Just vanilla CSS

**Tools:**
- npm for frontend packages
- pip for Python packages

---

## References

I used these while building this:

- Our Automata Theory textbook (Hopcroft & Ullman)
- Sipser's "Theory of Computation"
- Flask docs
- React docs
- Info about Sri Lankan NIC system from government sites

---

## Quick Start

If you just want to run it quickly:

```bash
# Terminal 1 - Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py

# Terminal 2 - Frontend  
cd frontend
npm install
npm start
```

Then go to `http://localhost:3000` in your browser.

---

That's it! This was my Automata Theory assignment. Hope it helps if you're working on something similar.
