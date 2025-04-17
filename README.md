```markdown
# AI-genda: Smart Todoist Scheduler with ChatGPT

## Requirements

- Python 3.7+
- Todoist account
- OpenAI account
- `.env` file

## Setup

### 1. Create Todoist Project

- Name: `Test`

### 2. Get Todoist API Token

- https://todoist.com/prefs/integrations

### 3. Get OpenAI API Key

- https://platform.openai.com/api-keys

### 4. Create `.env` file

```
TODOIST_API_TOKEN=your_todoist_token_here
OPENAI_API_KEY=your_openai_key_here
PROJECT_NAME=Test
```

### 5. Install Dependencies

```
pip install openai requests python-dotenv
```

## Usage

### Run the scheduler

```
python main.py
```

### (Optional) Clear and reset tasks

```
python clear.py
```

## Default Scheduling Rules

- Work: 09:00–11:00
- Chores: Before 09:00
- Fitness: 17:00
- Reading: 16:00
```
