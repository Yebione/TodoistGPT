import requests
import openai
import datetime
import json
from dotenv import load_dotenv
import os

load_dotenv()

TODOIST_API_TOKEN = os.getenv("TODOIST_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

PROJECT_NAME="Test" #You can change this to your actual inbox. Please refer to todoist API documetation. 

# Set your OpenAI API key
openai.api_key = OPENAI_API_KEY
# ==== HEADERS ====
todoist_headers = {
    "Authorization": f"Bearer {TODOIST_API_TOKEN}"
}

openai.api_key = OPENAI_API_KEY

# ==== STEP 1: Get Project ID ====
def get_project_id(project_name):
    response = requests.get("https://api.todoist.com/rest/v2/projects", headers=todoist_headers)
    response.raise_for_status()
    projects = response.json()
    for project in projects:
        if project["name"].lower() == project_name.lower():
            return project["id"]
    return None

# ==== STEP 2: Fetch Tasks in Project ====
def get_tasks_from_project(project_id):
    response = requests.get("https://api.todoist.com/rest/v2/tasks", headers=todoist_headers)
    response.raise_for_status()
    all_tasks = response.json()
    return [task for task in all_tasks if task["project_id"] == project_id]

# ==== STEP 3: Format Tasks for OpenAI ====
def format_tasks_for_prompt(tasks):
    lines = []
    for task in tasks:
        line = f"- {task['content']}"
        if "due" in task and task["due"] and task["due"].get("datetime"):
            line += f" (Due: {task['due']['datetime']})"
        lines.append(line)
    return "\n".join(lines)

# ==== STEP 4: Ask OpenAI to Schedule in JSON ====
def ask_openai_to_schedule_json(formatted_task_list):
    prompt = f"""
You are my personal secretary. Your job is to look into my Todoist to-do list and assign start times based on the following rules:

[‼️input your schedule context here (ex. "I work at 9am to 5pm so that is my work hours, put work related tasks in that time")]

You MUST reply with **raw JSON only**. Do NOT wrap the response in code blocks or markdown. Just a plain JSON array. Example:

[
  {{
    "task_content": "Fix the fence",
    "start_time": "07:30",
    "estimated_duration_minutes": 45
  }},
  ...
]

Here is the to-do list:
{formatted_task_list}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18", #You can also use other models
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']


# ==== STEP 5: Update Task in Todoist ====
def update_task_due_time(task_id, start_time_iso):
    response = requests.post(
        f"https://api.todoist.com/rest/v2/tasks/{task_id}",
        headers={
            **todoist_headers,
            "Content-Type": "application/json"
        },
        json={
            "due_datetime": start_time_iso
        }
    )
    response.raise_for_status()
    print(f"✅ Updated task ID {task_id} to start at {start_time_iso}")

# ==== STEP 6: Main Flow ====
def main():
    # Get project ID
    project_id = get_project_id(PROJECT_NAME)
    if not project_id:
        print(f"Project '{PROJECT_NAME}' not found.")
        return

    # Fetch tasks
    tasks = get_tasks_from_project(project_id)
    if not tasks:
        print("No tasks found in project.")
        return

    # Format for prompt and send to OpenAI
    formatted = format_tasks_for_prompt(tasks)
    chatgpt_response = ask_openai_to_schedule_json(formatted)

    try:
        scheduled_tasks = json.loads(chatgpt_response)
    except json.JSONDecodeError as e:
        print("❌ Failed to decode JSON from OpenAI:", e)
        print(chatgpt_response)
        return

    # Update tasks in Todoist
    now = datetime.datetime.now()
    for scheduled in scheduled_tasks:
        content = scheduled["task_content"]
        time_str = scheduled["start_time"]
        iso_time = f"{now.date()}T{time_str}:00"

        matched = False
        for task in tasks:
            if task["content"].strip().lower() == content.strip().lower():
                update_task_due_time(task["id"], iso_time)
                matched = True
                break

        if not matched:
            print(f"⚠️ Could not find match for task: {content}")

if __name__ == "__main__":
    main()