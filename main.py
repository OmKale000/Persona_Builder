import os
import praw
from dotenv import load_dotenv
from together import Together

# Load API keys from .env file
load_dotenv()

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Initialize Together API
client = Together(api_key=TOGETHER_API_KEY)

def fetch_reddit_data(username, limit=50):
    try:
        user = reddit.redditor(username)
        posts, comments = [], []

        for post in user.submissions.new(limit=limit):
            posts.append({
                'title': post.title,
                'selftext': post.selftext,
                'permalink': f"https://reddit.com{post.permalink}"
            })

        for comment in user.comments.new(limit=limit):
            comments.append({
                'body': comment.body,
                'permalink': f"https://reddit.com{comment.permalink}"
            })

        return posts, comments

    except Exception as err:
        print(f"[!] Error fetching data for u/{username}: {err}")
        return [], []

def build_prompt(posts, comments, username):
    intro = (
        f"Create a detailed, structured persona for Reddit user '{username}', formatted exactly like this example:\n\n"
        "Name: [Name]\n"
        "Age: [Age]\n"
        "Occupation: [Occupation]\n"
        "Status: [Relationship Status]\n"
        "Location: [City, Country]\n"
        "Tier: [User Tier]\n"
        "Archetype: [Archetype]\n\n"
        "Personality:\n"
        "Trait1 – Trait2\n"
        "Trait3 – Trait4\n"
        "Introvert <--------|--------> Extrovert\n"
        "Intuition <----|----------> Sensing\n"
        "Feeling <------|---------> Thinking\n"
        "Perceiving <----------|--> Judging\n\n"
        "Motivations:\n"
        "Convenience: ████████\n"
        "Wellness: ████████\n"
        "Speed: ███████\n"
        "Preferences: ██████\n"
        "Comfort: █████\n"
        "Dietary Needs: ███████\n\n"
        "Behaviour & Habits:\n"
        "[Brief paragraphs describing behavior]\n\n"
        "Frustrations:\n"
        "[List main frustrations]\n\n"
        "Goals & Needs:\n"
        "[List main goals and needs]\n\n"
        "Quote:\n"
        "[A memorable quote from the user]\n\n"
        "Use the Reddit posts and comments below as the data source to fill this template.\n\n"
    )

    post_block = "Posts:\n"
    for idx, post in enumerate(posts, 1):
        snippet = post['selftext'].strip().replace('\n', ' ')[:200] if post['selftext'] else ""
        post_block += f"{idx}. {post['title']} — {snippet}...\n   Link: {post['permalink']}\n"

    comment_block = "\nComments:\n"
    for idx, comment in enumerate(comments, 1):
        body = comment['body'].strip().replace('\n', ' ')[:200]
        comment_block += f"{idx}. {body}...\n   Link: {comment['permalink']}\n"

    closing = "\nGenerate the persona in the above structured format."

    return intro + post_block + comment_block + closing


def generate_persona(prompt_text):
    try:
        response = client.chat.completions.create(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=[
                {
                    "role": "system",
                    "content": "You analyze Reddit users and generate sharp, detailed personas based on their posts and comments."
                },
                {
                    "role": "user",
                    "content": prompt_text
                }
            ],
            max_tokens=1200,
            temperature=0.65
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Together API error: {e}")
        return None

def save_persona(username, persona):
    filename = f"{username}_persona.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(persona)
    print(f" Persona saved to {filename}")


def main():
    print(" Reddit Persona Generator")
    print("-" * 30)

    uname = input("Enter Reddit username: ").strip()
    print(f" Fetching data for u/{uname}...\n")

    posts, comments = fetch_reddit_data(uname)

    if not posts and not comments:
        print(" No data found. Try a different username.")
        return

    prompt = build_prompt(posts, comments, uname)
    print(" Generating persona from Together.ai...\n")

    result = generate_persona(prompt)

    if result:
        save_persona(uname, result)
    else:
        print(" Could not generate persona. Please try again later.")

if __name__ == "__main__":
    main()
