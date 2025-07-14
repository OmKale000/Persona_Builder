# Reddit Persona Generator

This Python script creates a detailed persona for any Reddit user by analyzing their recent posts and comments. It uses the Reddit API to fetch user content and Together.ai to generate a structured user profile.

---

## Features

- Fetches recent posts and comments from Reddit users  
- Generates a clear, bold, and structured user persona  
- Saves the persona in a text file named `<username>_persona.txt`

---

## Prerequisites

Make sure you have Python 3.8+ installed. You’ll also need API credentials for Reddit and Together.ai.

---

## Setup Instructions

First, create a virtual environment to keep dependencies organized:

```bash
python -m venv venv
```
---
Activate the environment:

On Windows:
```
bash
venv\Scripts\activate
```
On macOS/Linux:
```
source venv/bin/activate
```
---
Then, install the required Python packages:
```
pip install praw together python-dotenv
```
## Configure API Keys
---
Create a .env file in the project folder with your API credentials, like this:
```
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=your_user_agent_string
TOGETHER_API_KEY=your_together_api_key
```
Replace the placeholders with your actual keys.

## How to Run
---
Run the script with:
```
bash
python main.py
```
When prompted, enter the Reddit username you want to analyze.

## Example
---
Here’s what running the script might look like:
```
Enter Reddit username: spez
Fetching data for u/spez...
Generating persona from Together.ai...

Persona saved to spez_persona.txt
```
You’ll find the persona saved in a file named spez_persona.txt.

## Troubleshooting
---
If data fetching fails, double-check your Reddit API keys in .env.

If persona generation fails, check your Together.ai API key and quota.

Make sure your internet connection is active.

## Author & Contact :
---
Om Kale

Email: ok176471@gmail.com

LinkedIn: linkedin.com/in/om-kale-1663a0276

GitHub: github.com/OmKale

