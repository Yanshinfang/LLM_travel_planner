import gradio as gr
from google.cloud import storage, firestore
from langchain.schema.document import Document
from langchain_google_firestore import FirestoreVectorStore
from langchain_google_vertexai import VertexAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import vertexai
from vertexai.language_models import ChatModel
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
import time

# define first model - chat model
PROJECT_ID = ""     # define project id
vertexai.init(project=PROJECT_ID, location="us-central1")
textsi_1 = """
    ROLE:You are a Travel Planner Chatbox Assistant. Your name is Trav. Now you are only available for scheduling a trip to Bay area cities.

    INSTRUCTION:
    Greet the user warmly and offer assistance in planning their travel. If user doesn't specify questions, provide a list of options they can choose from, or invite them to type their specific request.
    Ensure the options cover various aspects of travel planning, including destination ideas, itinerary planning, accommodation recommendations, transportation options, activities and attractions, and travel tips and advice. 
    Be clear and concise in the messaging. When you recommend hotel/restaurant, make sure you only recommend when you have information to recommend.
    If they want a detail planner, please schedule for them with the tourist place, food day by day.

    RESTRICTION:Do not use overly complex language or jargon. Keep the tone friendly and approachable. Do not overwhelm the user with too many options or too much information at once.
    """

generation_config = {
    "max_output_tokens": 2048,
    "temperature": 0.7,
    "top_p": 1,
  }

safety_settings = {
generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}
model = GenerativeModel(
    "gemini-1.0-pro-002",
    system_instruction=[textsi_1])
chat = model.start_chat()

# define second model - category model
map_category = """
ROLE: You are a assiatance to help people catorize their questions.

INSTRUCTION: 
Given the user question, you will need to reiterate the questions and also map the question into 5 categories - food, weather, hotel, tourist_place, detail_planner.
You might need to consider that some of the questions are follow-up questions, you need to map into above 5 categoires.

RESTRICTION:
If you think the question is only about one categories, then only answer above five categories name - food, weather, hotel, tourist_place, detail_planner.
Only answer above four categories name, if no related then answer None.

EXAMPLE:
user ask: recommend restaurant
you reply: recommend restaurant,food
and user ask follow-up question: in daly city
you reply: recommend restaurant in daly city,food
"""
model_category = GenerativeModel(
    "gemini-1.0-pro-002",
    system_instruction=[map_category]
)
category_chat = model_category.start_chat()

# connect with vector store
def get_vector_store(project_id, collection):
    embedding = VertexAIEmbeddings(
    model_name="textembedding-gecko@latest",
    project=project_id)
    # Create a vector store
    vector_store = FirestoreVectorStore(
        collection=collection,
        embedding_service=embedding
    )
    return vector_store


def multiturn_generate_content(message, history):
    category = category_chat.send_message(
        [message],
        generation_config=generation_config,
        safety_settings=safety_settings).text
    cat = ''
    try:
        question, cat = category.split(',')[0], category.split(',')[1]
        print(question, cat)
    except:
        print(category)

    categories = ['food', 'hotel', 'weather', 'tourist_place']
    if cat in categories:
        vector_store = get_vector_store(PROJECT_ID, cat)
        matches = vector_store.similarity_search(question, 7)
        documents = [doc.page_content for doc in matches]
        # print(f"documents{documents}")
        prompt = f"""
            USER QUESTION:{message}
            RELATED DOCUMENT: {documents}
            """
    elif category == 'detail_planner':
        prompt = f"""USER QUESTION:{message}"""
        for category in categories:
            vector_store = get_vector_store(PROJECT_ID, category)
            matches = vector_store.similarity_search(message, 5)
            documents = [doc.page_content for doc in matches]
            # print(f"documents{documents}")
            prompt += f"""
                Info About{category}: {documents}
                """
    else:
        prompt = f"""USER QUESTION:{message}"""
    return chat.send_message(
        [prompt],
        generation_config=generation_config,
        safety_settings=safety_settings).text


with gr.Blocks(fill_height=True) as demo:
    gr.Markdown("""# Trav - Your travel planner🌁
                
                """)
    with gr.Row():
        with gr.Column(scale=1):
            image = gr.Image(value="./pic/home.webp")
        with gr.Column(scale=2):
            gr.ChatInterface(fn=multiturn_generate_content,
                             examples=["What's the general weather in Bay area?", "Help me to find a must-go place", "Recommend restaurant to me", 'Give me a detailed planner for 5 days', 'Any great hotel?'])

demo.launch(share=True)