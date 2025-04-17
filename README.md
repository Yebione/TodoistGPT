# AI-genda: Smart Todoist Scheduler with ChatGPT

## Requirements  
- Python 3.7+  
- Todoist account  
- OpenAI account  
- `.env` file  

## Setup

### 1. Download and Set Up Todoist  
- Go to https://todoist.com or download the app  
- Sign up or log in to your account  
- Create a new project and name it `Test`  

### 2. Get Todoist API Token  
- Go to https://todoist.com/prefs/integrations  
- Scroll to "API token" and copy it  

### 3. Get OpenAI API Key  
- Go to https://platform.openai.com/api-keys  
- Click "Create new secret key" and copy it  

### 4. Create `.env` file in your project directory  
TODOIST_API_TOKEN=your_todoist_token_here  
OPENAI_API_KEY=your_openai_key_here  
PROJECT_NAME=Test  

### 5. Install Dependencies  
pip install openai requests python-dotenv

## Usage

### Run the scheduler  
python main.py
