
import requests

# Ollama API settings
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:0.5b"

# Step 1: FAQ Knowledge Base
faq = {
    "pricing": "Our basic plan starts at $10/month with premium options.",
    "refund": "Refunds are available within 30 days of purchase. Please share your order ID.",
    "support": "You can reach support at support@example.com, 24/7."
}

# Conversation memory
history = []


# Step 2: Check FAQ
def check_faq(email_text):
    for keyword, answer in faq.items():
        if keyword in email_text.lower():
            return answer
    return None


# Step 3: Generate AI Response with Ollama API
def ollama_response(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=300
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()

    except requests.exceptions.ConnectionError:
        return "Error: Ollama is not running. Please start Ollama."

    except requests.exceptions.Timeout:
        return "Error: Request timed out. Please try again."

    except requests.exceptions.RequestException as error:
        return f"Error: {error}"


# Step 4: Email Assistant Logic
def email_assistant(email_text):

    if not email_text.strip():
        return "Please enter an email message."

    faq_answer = check_faq(email_text)

    if faq_answer:
        reply = "FAQ Reply: " + faq_answer

    else:
        context = "\n".join(history[-6:])

        prompt = (
            "You are a professional email assistant. "
            "Draft a polite and professional reply.\n\n"
            f"Previous conversation:\n{context}\n\n"
            f"Incoming email:\n{email_text}\n\n"
            "Suggested reply:"
        )

        reply = "AI Reply: " + ollama_response(prompt)

    # Store conversation history
    history.append(f"Email: {email_text}")
    history.append(reply)

    return reply


# Step 5: Test with sample emails
if __name__ == "__main__":

    emails = [
        "Tell me about pricing",
        "How to get refund?",
        "Need support help",
        "Delay in my order"
    ]

    for mail in emails:
        print("\nEmail:", mail)
        print(email_assistant(mail))

    # Interactive mode
    print("\n--- Intelligent Email Assistant ---")
    print("Type 'exit' to stop.\n")

    while True:
        email = input("Incoming email: ")

        if email.lower() == "exit":
            print("Assistant closed.")
            break

        print(email_assistant(email))
