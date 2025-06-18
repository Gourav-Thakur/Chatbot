from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# # Setup Gemini API
# # genai.configure(api_key="YOUR_GEMINI_API_KEY")

# # model = genai.GenerativeModel("gemini-pro")
# # chat = model.start_chat()

# # Store in-memory conversation


import google.generativeai as genai


# 🧾 Step 3: What the bot must collect
required_info = {
    "name": None,
    "product": None,
    "batch_number": None,
    "issue_type": None,
    "photo": None  # assume text for now
}

# 💬 Step 4: Initial instruction prompt
initial_prompt = """
You are a paint complaint assistant. Your job is to collect these from the user:
- Name
- Product name
- Batch number
- Type of problem (peeling, smell, bubbling, discoloration, etc.)
- Optional: a photo (describe if possible)

Start by greeting them. If any field is missing, politely ask for it.
When all info is collected, reply: "✅ Complaint registered successfully!"
"""

# chat_history = []

# print("PaintBot 🤖: Hello! I’m here to register your paint complaint. How can I help you today?")

# 🔄 Step 5: Chat loop
# while True:
#     user_input = input("You: ")

#     if user_input.lower() in ["exit", "quit"]:
#         print("PaintBot 🤖: Thank you for contacting JSW. Goodbye!")
#         break

genai.configure(api_key="AIzaSyCVUBomH-ejVfatDhbKzbdUTdOrKTSCM4k")  # Replace with your Gemini API key

# 🧠 Step 2: Load model and initialize chat
model = genai.GenerativeModel("gemini-1.5-flash-latest")
#     # Send user message to Gemini
#     response = chat.send_message(user_input)
@csrf_exempt
def chatbot_view(request):
    # Use session to store chat history per user
    if 'chat_history' not in request.session:
        request.session['chat_history'] = [
            {'sender': 'bot', 'text': "Hello! I’m here to register your paint complaint. How can I help you today?"}
        ]
    chat_history = request.session['chat_history']

    # Build Gemini history from chat_history
    gemini_history = []
    for msg in chat_history:
        if msg['sender'] == 'user':
            gemini_history.append({"role": "user", "parts": [msg['text']]})
        elif msg['sender'] == 'bot':
            gemini_history.append({"role": "model", "parts": [msg['text']]})
    # Always start with the initial prompt
    if not any(h['role'] == 'user' and h['parts'][0] == initial_prompt for h in gemini_history):
        gemini_history.insert(0, {"role": "user", "parts": [initial_prompt]})

    chat = model.start_chat(history=gemini_history)

    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        if user_input:
            chat_history.append({'sender': 'user', 'text': user_input})
            response = chat.send_message(user_input)
            chat_history.append({'sender': 'bot', 'text': response.text})
            request.session['chat_history'] = chat_history  # Save back to session

    return render(request, 'chat.html', {'messages': chat_history})