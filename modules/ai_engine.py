import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st
    groq_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
except:
    groq_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_key)
def get_ai_response(user_input, chat_history=None, user_context="", tasks=None, notes=None, reminders=None):
    try:
        # Build rich system context
        system_parts = [
            "You are NEXUS, a highly intelligent personal AI assistant.",
            "You are sharp, concise, and professional.",
            "You have direct access to the user's personal workspace data.",
        ]

        if user_context:
            system_parts.append(f"\nUSER PROFILE:\n{user_context}")

        if tasks:
            pending = [t for t in tasks if t.status != "completed"]
            done    = [t for t in tasks if t.status == "completed"]
            task_lines = []
            for t in pending:
                task_lines.append(f"  - [PENDING] {t.title}: {t.description or 'no description'}")
            for t in done:
                task_lines.append(f"  - [DONE] {t.title}")
            if task_lines:
                system_parts.append(f"\nUSER'S TASKS:\n" + "\n".join(task_lines))

        if notes:
            note_lines = [f"  - {n.title}: {n.content or 'no content'}" for n in notes]
            system_parts.append(f"\nUSER'S NOTES:\n" + "\n".join(note_lines))

        if reminders:
            import datetime
            now = datetime.datetime.now()
            rem_lines = []
            for r in reminders:
                status = "OVERDUE" if r.due_date and r.due_date < now else "UPCOMING"
                date_str = r.due_date.strftime("%b %d, %Y %H:%M") if r.due_date else "no date"
                rem_lines.append(f"  - [{status}] {r.title} — {date_str}")
            system_parts.append(f"\nUSER'S REMINDERS:\n" + "\n".join(rem_lines))

        system_parts.append(
            "\nUse this data naturally when relevant. "
            "If asked about tasks, notes or reminders, refer to the actual data above. "
            "Be concise and helpful."
        )

        system_instruction = "\n".join(system_parts)

        messages = [{"role": "system", "content": system_instruction}]

        if chat_history:
            for msg in chat_history:
                messages.append({"role": msg["role"], "content": msg["content"]})

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"AI Engine Error: {str(e)}"