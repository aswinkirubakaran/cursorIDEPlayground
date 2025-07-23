import gradio as gr
import requests
import os

# Set your Hugging Face API token here or via environment variable
HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')

SYSTEM_PROMPT = """
You are an AI system check assistant. The user will ask you about system status (disk, CPU, memory, network, processes, services, etc.).
1. If the user asks a question, suggest the most appropriate system command (for Windows, use PowerShell; for Linux/Mac, use bash) and explain what it does.
2. Ask the user to run the command and paste the result here.
3. When the user pastes the result, analyze it and suggest next steps if there are issues, or confirm if all is well.
4. Never run commands yourself. Always keep the human in the loop.
"""


def chat_agent(history, user_input, os_type):
    # Compose the prompt
    prompt = f"""{SYSTEM_PROMPT}\nThe user's operating system is: {os_type}.\nConversation history:\n"""
    for user, ai in history:
        prompt += f"User: {user}\nAssistant: {ai}\n"
    prompt += f"User: {user_input}\nAssistant:"

    api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 256, "temperature": 0.7}}

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        if isinstance(result, dict) and "error" in result:
            return f"Error: {result['error']}"
        # The response is a list of dicts with 'generated_text'
        return result[0]["generated_text"].split("Assistant:")[-1].strip()
    except Exception as e:
        print("Hugging Face API error:", e)
        return f"Error: {e}"


def gradio_chat(user_input, history, os_type):
    if history is None:
        history = []
    ai_reply = chat_agent(history, user_input, os_type)
    history.append((user_input, ai_reply))
    return history, history

with gr.Blocks() as demo:
    gr.Markdown("# 🛠️ AI System Check Agent\nAsk me about your system status! (Disk, CPU, memory, network, processes, services, etc.)\n\n**Note:** I will suggest commands, but you must run them and paste the results here.")
    os_type = gr.Radio(["Windows", "Linux", "Mac"], value="Windows", label="Your Operating System")
    chatbot = gr.Chatbot()
    state = gr.State([])
    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Type your system check question or paste command output here...")
    txt.submit(gradio_chat, [txt, state, os_type], [chatbot, state])
    txt.submit(lambda: "", None, txt)

demo.launch() 
