import streamlit as st
import json
import nltk

nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.metrics import jaccard_distance

user_history = {}
with open("questionaire1.json", "r") as file:
    questionaire1 = json.load(file).get("questionaire1", [])

def preprocess_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    return tokens

def jaccard_similarity(sentence1, sentence2):
    tokens1 = set(preprocess_text(sentence1))
    tokens2 = set(preprocess_text(sentence2))
    jaccard = 1 - jaccard_distance(tokens1, tokens2)
    return jaccard

def login():
    username = st.text_input("Entrez votre nom d'utilisateur : ")
    st.write(f"Bienvenue, {username} ! Vous êtes connecté.")
    return username

def obtenir_reponse(question, username):
    if username in user_history:
        for previous_question, previous_answer in user_history[username].items():
            similarity = jaccard_similarity(question, previous_question)
            if similarity > 0.7:
                return f"Vous avez déjà posé une question similaire. Voici la réponse précédente : {previous_answer}"

    for example in questionaire1:
        similarity = jaccard_similarity(question, example["question"])
        if similarity > 0.7:
            user_history.setdefault(username, {})[question] = example["answer"]
            return f"Voici des informations sur le secourisme : {example['answer']}"

    return "Je ne suis pas sûr de comprendre. Pouvez-vous reformuler votre question ?"

# Set page configuration
st.set_page_config(
    page_title="Professional Chatbot",
    page_icon=":robot_face:",
    layout="wide",
)

def chatbot():
    st.title("Pediatriebot - Ask Me Anything about pediatrics!")
    st.write("Welcome to the professional chatbot. Feel free to ask questions or seek assistance.")

    username = login()

    # User input
    question_utilisateur = st.text_input(f"{username} asks:", key="user_input")

    # Send button
    if st.button("Send", key="send_button"):
        if "bye" in question_utilisateur.lower() or "au revoir" in question_utilisateur.lower():
            st.success("Chatbot: Goodbye!")
        else:
            # Get chatbot response
            response = obtenir_reponse(question_utilisateur, username)
            st.write(f"{username} asks: {question_utilisateur}")
            st.write("Chatbot:", response)

if __name__ == "__main__":
    chatbot()
