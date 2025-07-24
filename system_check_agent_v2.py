 # This code uses the OpenAI Python SDK to call Groq's API endpoint and the Gemma model.
import gradio as gr
import os
import shutil
import psutil
import socket
from openai import OpenAI

# Set your Groq API key and model here or via environment variable
GROQ_API_KEY = 'GROQ_API_*****'
GROQ_MODEL = 'gemma2-9b-it'  # Default to Gemma-7B-IT

def get_disk_usage(os_type):
    if os_type == "Windows":
        drive = os.getenv('SystemDrive', 'C:') + "\\"
    else:
        drive = "/"
    total, used, free = shutil.disk_usage(drive)
    gb = lambda x: round(x / (1024 ** 3), 2)
    percent_used = round(used / total * 100, 2)
    return f"Disk usage for {drive}:\nTotal: {gb(total)} GB\nUsed: {gb(used)} GB ({percent_used}%)\nFree: {gb(free)} GB"

def get_memory_usage():
    mem = psutil.virtual_memory()
    gb = lambda x: round(x / (1024 ** 3), 2)
    return f"Memory usage:\nTotal: {gb(mem.total)} GB\nUsed: {gb(mem.used)} GB ({mem.percent}%)\nFree: {gb(mem.available)} GB"

def get_network_status():
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    lines = []
    for iface, addr_list in addrs.items():
        if iface in stats and stats[iface].isup:
            ip = next((a.address for a in addr_list if a.family == socket.AF_INET), None)
            lines.append(f"{iface}: UP, IP: {ip if ip else 'N/A'}")
    if not lines:
        return "No active network interfaces found."
    return "Network status:\n" + "\n".join(lines)

def get_system_status():
    return f"System status summary:\n{get_disk_usage(os_type='Windows' if os.name == 'nt' else 'Linux')}\n{get_memory_usage()}\n{get_network_status()}"

def is_disk_usage_question(user_input):
    keywords = ["disk usage", "disk space", "free space", "storage left", "how much space", "used space", "available space"]
    return any(k in user_input.lower() for k in keywords)

def is_memory_usage_question(user_input):
    keywords = ["memory usage", "ram usage", "free memory", "used memory", "available memory", "system memory"]
    return any(k in user_input.lower() for k in keywords)

def is_network_status_question(user_input):
    keywords = ["network status", "network connection", "internet status", "ip address", "network interface", "is network up", "is internet up"]
    return any(k in user_input.lower() for k in keywords)

def is_system_status_question(user_input):
    keywords = ["system status", "system summary", "overall status", "system health", "system info", "system information"]
    return any(k in user_input.lower() for k in keywords)

SYSTEM_PROMPT = (
    "You are a system check assistant. The user will ask you about system status (disk, CPU, memory, network, processes, services, etc.). "
    "If the user asks a question, suggest the most appropriate system command (for Windows, use PowerShell; for Linux/Mac, use bash) and explain what it does. "
    "Ask the user to run the command and paste the result here. "
    "When the user pastes the result, analyze it and suggest next steps if there are issues, or confirm if all is well. "
    "Never run commands yourself. Always keep the human in the loop."
)

def groq_agent(history, user_input, os_type):
    prompt = f"{SYSTEM_PROMPT}\nThe user's operating system is: {os_type}.\nConversation history:\n"
    for user, ai in history:
        prompt += f"User: {user}\nAssistant: {ai}\n"
    prompt += f"User: {user_input}\nAssistant:"
    try:
        client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
            max_tokens=256,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def gradio_chat(user_input, history, os_type):
    if history is None:
        history = []
    if is_disk_usage_question(user_input):
        ai_reply = get_disk_usage(os_type)
    elif is_memory_usage_question(user_input):
        ai_reply = get_memory_usage()
    elif is_network_status_question(user_input):
        ai_reply = get_network_status()
    elif is_system_status_question(user_input):
        ai_reply = get_system_status()
    else:
        ai_reply = groq_agent(history, user_input, os_type)
    history.append((user_input, ai_reply))
    return history, history

with gr.Blocks() as demo:
    gr.Markdown("# 🛠️ System Check Agent\nAsk me about your system status! (Disk, CPU, memory, network, processes, services, etc.)\n\n**Note:** I will suggest commands, but you must run them and paste the results here. Powered by Groq and Gemma.")
    os_type = gr.Radio(["Windows", "Linux", "Mac"], value="Windows", label="Your Operating System")
    chatbot = gr.Chatbot()
    state = gr.State([])
    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Type your system check question or paste command output here...")
    txt.submit(gradio_chat, [txt, state, os_type], [chatbot, state])
    txt.submit(lambda: "", None, txt)

demo.launch() 
