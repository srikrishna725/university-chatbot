from collections import Counter
import json
import spacy
import random
from user_functions import preprocess, compare_overlap, pos_tag, extract_nouns

# load spacy model
word2vec = spacy.load("en_core_web_md")

# load intents
with open("intents.json") as file:
    data = json.load(file)

intents = data["intents"]

exit_commands = (
    "quit", "goodbye", "exit", "bye", "bye bye", "see you",
    "see you later", "catch you later", "talk to you later",
    "i have to go", "gotta go", "i'm leaving", "im leaving",
    "thanks bye", "bye for now", "take care", "end chat",
    "stop", "close", "no thanks", "nothing", "that's all", "thats all"
)


class ChatBot:
  
  # make_exit
  def make_exit(self, user_message):
    user_message = user_message.lower().strip()
    
    if user_message in exit_commands:
        print("Ok, Good Bye!")
        return True
    
    return False
  
  # chat
  def chat(self):
    user_message = input("Hello! I'm your university assistant. Ask me anything about the college.")
    while not self.make_exit(user_message):
      user_message = self.respond(user_message)
  
  
  # find_intent_match 
  def find_intent_match(self, user_message):
    bow_user = Counter(preprocess(user_message))
    doc_user = word2vec(user_message)

    best_intent = None
    max_score = 0

    for intent in intents:
        for pattern in intent["patterns"]:
            # BoW score
            bow_pattern = Counter(preprocess(pattern))
            bow_score = compare_overlap(bow_pattern, bow_user)

            # Word2Vec similarity
            doc_pattern = word2vec(pattern)
            similarity = doc_user.similarity(doc_pattern)

            # Combine both
            score = bow_score + similarity

            if score > max_score:
                max_score = score
                best_intent = intent
    if max_score < 0.5:
       return None
    return best_intent

  
  # find_entities (same logic)
  def find_entities(self, user_message):
    doc = word2vec(user_message)

    # Step 1: Try Named Entity Recognition (NER)
    entities = [ent.text for ent in doc.ents]

    if entities:
        return entities[0]

    # Step 2: Fallback to noun extraction (your old logic)
    tagged_user_message = pos_tag(preprocess(user_message))
    nouns = extract_nouns(tagged_user_message)

    if nouns:
        return nouns[0]

    return ""

  
  # respond
  def respond(self, user_message):
    intent = self.find_intent_match(user_message)
    
    if intent is None:
      print("I'm not sure I understood that. Could you please rephrase your question?")
      return input("Do you have any other questions about the college? ")
    
    
    best_response = random.choice(intent["responses"])
    print(best_response)
    
    return input("Do you have any other questions about the college? ")
  

# run chatbot
chatbot = ChatBot()
chatbot.chat()