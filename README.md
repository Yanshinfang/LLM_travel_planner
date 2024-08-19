# Trav - AI Travel Assistant

Welcome to **Trav**, your personal AI travel assistant designed to help you customize your travel plans in the Bay Area. Whether you're looking for hotel recommendations, restaurant suggestions, or detailed travel itineraries, Trav has you covered.

## Features

- **Personalized Recommendations**: Get tailored recommendations for hotels, restaurants, and attractions based on your preferences.
- **Weather Insights**: Receive up-to-date weather information to help plan your activities.
- **Custom Travel Itineraries**: Trav can create a detailed, multi-day travel plan by combining information from various categories.

## How Trav Works

1. **Data Collection**: 
   - We gathered data from multiple sources using Selenium to scrape websites.
   - TripAdvisor and Google APIs were used to collect information such as location descriptions, latitude and longitude, reviews, and ratings.

2. **Model Exploration**:
   - We explored different approaches, including using GPT-4 with a Pinecone database and LLama 2 with Chroma and Pinecone vector databases.
   - Due to storage limitations in the free versions, we opted to use Gemini with Firebase Vector for our application, leveraging Google Cloud credits.

3. **Application Workflow**:
   - Our vector database is prepared by loading data from Google Cloud Storage, performing chunking and embedding, and storing it in the vector database.
   - When a user asks a question, we perform a similarity search in the vector database to retrieve relevant information.
   - We then combine the system instructions, relevant documents, and the user's question to generate a precise and useful response.

## Testing and Optimization

- **Temperature**: We tested different temperature settings and settled on 0.7 to ensure creativity in travel planning.
- **Chunk Size**: A chunk size of 1000 tokens was found to be optimal, providing comprehensive information.
- **Similarity Search**: We tested retrieving between 3 to 9 relevant documents and found that 5 documents worked best for detailed itineraries, while 7 documents were ideal for specific queries.

## Demo

Check out our [demo video](https://drive.google.com/file/d/1frLEfvm0iGhfzl5pEJ8-BdzZEwm_lVVM/view?usp=sharing) to see Trav in action!

- Trav can respond to general queries and will ask clarifying questions to better understand your needs.
- It can provide tailored restaurant recommendations based on previous interactions.
- Trav can also plan a detailed 5-day trip by combining information on restaurants, tourist spots, and hotel locations.

## Installation

To run Trav locally:

1. Clone this repository:
   \```bash
   git clone https://github.com/yourusername/trav.git
   \```
2. Install the required dependencies:
   \```bash
   pip install -r requirements.txt
   \```
3. Set up your API keys for TripAdvisor, Google, and Firebase in the `.env` file.

4. Run the application:
   \```bash
   python app_v1.py
   \```
