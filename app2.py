import openai
import gradio as gr
import requests
from bs4 import BeautifulSoup

# Set up OpenAI API key
openai.api_key = "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"

scraped_data = None  # Placeholder for scraped data
conversation = []

# Scraping function using BeautifulSoup
def scrape_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        # Extract text content from HTML using Beautiful Soup
        extracted_text = " ".join([p.get_text() for p in soup.find_all("p")])
        return extracted_text
    return None
    
# Process scraped data and create prompt
def prepare_prompt(data):
    return f"User: Extracted from URL: {data}\nAI:"

# AI interaction function
def ai_chat(conversation):
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    ai_response = chat.choices[0].message.content
    return ai_response

def chatbot(input_text):
    global scraped_data
    global conversation

    if scraped_data is None:
        scraped_data = scrape_url(input_text)
        conversation.append({"role": "user", "content": scraped_data})
        return "URL scraped successfully. Please input your question."

    else:
        user_question = input_text
        prompt = prepare_prompt(scraped_data)
        conversation.append({"role": "user", "content": user_question})
        ai_response = ai_chat(conversation)
        conversation[-1]["content"] = user_question  # Update last user input
        conversation.append({"role": "assistant", "content": ai_response})
        return ai_response

iface = gr.Interface(
    fn=chatbot,
    inputs=gr.inputs.Textbox(label="Enter URL to scrape or ask a question"),
    outputs=gr.outputs.Textbox(label="AI Response")
)

if __name__ == "__main__":
    iface.launch()