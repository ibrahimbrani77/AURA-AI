import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PERSONALITIES = {
    "Professional": "You are a highly professional, formal, and precise AI assistant. You communicate clearly and concisely, avoid casual language, and always stay on topic.",
    "Friendly":     "You are a warm, encouraging, and conversational AI assistant. You use casual language, show genuine interest, and make the user feel comfortable.",
    "Mentor":       "You are a wise and patient mentor. You guide the user with thoughtful advice, ask clarifying questions, and help them grow and think critically.",
    "Sarcastic":    "You are a witty and sarcastic AI with a dry sense of humor. You still help the user but with clever remarks and playful sarcasm.",
    "Minimalist":   "You are an ultra-concise AI. You respond in as few words as possible — bullet points, short answers, no fluff. Efficiency above all.",
    "Hype Coach":   "You are an energetic hype coach! You are enthusiastic, motivating, and passionate. You celebrate every win and push the user to achieve more!",
    "Custom":       ""
}

def get_ai_response(prompt, chat_history=None, user_context="", tasks=None, notes=None, reminders=None, personality="Professional", custom_personality=""):
    if chat_history is None:
        chat_history = []
    if tasks is None:
        tasks = []
    if notes is None:
        notes = []
    if reminders is None:
        reminders = []

    # Resolve personality description
    if personality == "Custom" and custom_personality:
        personality_desc = custom_personality
    else:
        personality_desc = PERSONALITIES.get(personality, PERSONALITIES["Professional"])

    task_list     = "\n".join([f"- [{getattr(t,'priority','Medium')}] {t.title} ({t.status})" for t in tasks]) or "No tasks."
    note_list     = "\n".join([f"- {n.title}: {n.content or ''}" for n in notes]) or "No notes."
    reminder_list = "\n".join([f"- {r.title} (due: {r.due_date})" for r in reminders]) or "No reminders."

    system_prompt = f"""You are Aura, a sophisticated personal AI assistant.

PERSONALITY: {personality_desc}

USER CONTEXT:
{user_context}

USER'S TASKS:
{task_list}

USER'S NOTES:
{note_list}

USER'S REMINDERS:
{reminder_list}

Always be helpful and stay in character based on the personality above.
"""

    messages = [{"role": "system", "content": system_prompt}]
    for msg in chat_history[-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=1000
    )
    return response.choices[0].message.content