"""
Chatbot 2 - Advanced ML-Based Chatbot
Chatbot avancé avec apprentissage automatique et NLP plus sophistiqué
"""

import json
import random
import re
from typing import Dict, List, Tuple
import numpy as np

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class AdvancedChatbot:
    """Chatbot avancé avec similarité sémantique et apprentissage"""
    
    def __init__(self):
        """Initialiser le chatbot avancé"""
        self.intents = self._load_intents()
        self.vectorizer = None
        self.intent_vectors = None
        self.learning_memory = []
        self.conversation_history = []
        
        if SKLEARN_AVAILABLE:
            self._train_intent_classifier()
    
    def _load_intents(self) -> Dict:
        """
        Charger les intentions du chatbot
        
        Returns:
            Dictionnaire des intentions
        """
        intents = {
            "greeting": {
                "patterns": ["bonjour", "salut", "coucou", "hey", "ça va"],
                "responses": [
                    "Bonjour! Heureux de vous rencontrer!",
                    "Salut! Comment puis-je vous aider aujourd'hui?",
                    "Coucou! Quoi de neuf?"
                ]
            },
            "name": {
                "patterns": ["ton nom", "comment tu t'appelles", "quel est ton nom"],
                "responses": [
                    "Je suis ChatBot2, un assistant IA avancé!",
                    "Mon nom est ChatBot2, ravi de vous rencontrer!",
                    "Je m'appelle ChatBot2, votre assistant numérique intelligent."
                ]
            },
            "help": {
                "patterns": ["aide", "help", "peux-tu m'aider", "besoin d'aide"],
                "responses": [
                    "Bien sûr! Je peux vous aider avec vos questions.",
                    "Oui, je suis là pour vous aider. Que puis-je faire?",
                    "Absolument! Posez-moi vos questions."
                ]
            },
            "thanks": {
                "patterns": ["merci", "thank you", "merci beaucoup", "grâce"],
                "responses": [
                    "De rien! C'est un plaisir!",
                    "Heureux de pouvoir aider!",
                    "C'est mon rôle!"
                ]
            },
            "goodbye": {
                "patterns": ["au revoir", "goodbye", "bye", "à bientôt", "ciao"],
                "responses": [
                    "Au revoir! À bientôt!",
                    "Bye! Passez une excellente journée!",
                    "À bientôt, c'était agréable de discuter!"
                ]
            },
            "weather": {
                "patterns": ["météo", "temps", "weather", "il fait"],
                "responses": [
                    "Je n'ai pas accès aux données météorologiques.",
                    "Pour la météo, consultez une application dédiée.",
                    "Vérifiez un service météorologique pour les prévisions."
                ]
            },
            "ai_info": {
                "patterns": ["IA", "intelligence artificielle", "machine learning", "apprentissage"],
                "responses": [
                    "L'IA est fascinante! Elle transforme le monde.",
                    "L'intelligence artificielle est l'avenir!",
                    "L'IA permet de résoudre des problèmes complexes."
                ]
            }
        }
        return intents
    
    def _train_intent_classifier(self):
        """Entraîner le classifieur d'intentions avec TF-IDF"""
        if not SKLEARN_AVAILABLE:
            return
        
        # Préparer les données d'entraînement
        all_patterns = []
        intent_labels = []
        
        for intent_name, intent_data in self.intents.items():
            for pattern in intent_data["patterns"]:
                all_patterns.append(pattern)
                intent_labels.append(intent_name)
        
        if all_patterns:
            self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='french')
            self.intent_vectors = self.vectorizer.fit_transform(all_patterns)
            self.intent_labels = intent_labels
    
    def preprocess(self, text: str) -> str:
        """
        Prétraiter le texte
        
        Args:
            text: Texte à traiter
            
        Returns:
            Texte nettoyé
        """
        text = text.lower()
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'[!?.,;:]', '', text)
        return text
    
    def find_best_intent(self, user_input: str) -> Tuple[str, float]:
        """
        Trouver l'intention la mieux adaptée
        
        Args:
            user_input: Entrée utilisateur
            
        Returns:
            Tuple (intention, confiance)
        """
        if not SKLEARN_AVAILABLE or not self.vectorizer:
            return self._find_intent_basic(user_input)
        
        processed_input = self.preprocess(user_input)
        user_vector = self.vectorizer.transform([processed_input])
        
        similarities = cosine_similarity(user_vector, self.intent_vectors)[0]
        best_idx = np.argmax(similarities)
        best_intent = self.intent_labels[best_idx]
        confidence = similarities[best_idx]
        
        return best_intent, confidence
    
    def _find_intent_basic(self, user_input: str) -> Tuple[str, float]:
        """Méthode de fallback pour trouver l'intention"""
        processed_input = self.preprocess(user_input)
        
        for intent_name, intent_data in self.intents.items():
            for pattern in intent_data["patterns"]:
                if pattern in processed_input:
                    return intent_name, 0.8
        
        return "unknown", 0.0
    
    def get_response(self, user_input: str) -> str:
        """
        Obtenir une réponse adaptée
        
        Args:
            user_input: Entrée utilisateur
            
        Returns:
            Réponse du chatbot
        """
        intent, confidence = self.find_best_intent(user_input)
        
        # Sauvegarder en mémoire
        self.learning_memory.append({
            "input": user_input,
            "intent": intent,
            "confidence": float(confidence)
        })
        
        # Retourner une réponse adaptée
        if intent in self.intents:
            responses = self.intents[intent]["responses"]
            response = random.choice(responses)
        else:
            response = "Je ne suis pas sûr de bien comprendre. Pouvez-vous reformuler?"
        
        return response
    
    def get_stats(self) -> Dict:
        """
        Obtenir les statistiques d'apprentissage
        
        Returns:
            Dictionnaire des statistiques
        """
        if not self.learning_memory:
            return {}
        
        intents_count = {}
        total_confidence = 0
        
        for memory in self.learning_memory:
            intent = memory["intent"]
            intents_count[intent] = intents_count.get(intent, 0) + 1
            total_confidence += memory["confidence"]
        
        avg_confidence = total_confidence / len(self.learning_memory)
        
        return {
            "total_interactions": len(self.learning_memory),
            "intents_detected": intents_count,
            "average_confidence": avg_confidence
        }
    
    def chat(self):
        """Boucle de conversation interactive"""
        print("\n" + "="*60)
        print("🤖 Bienvenue dans ChatBot 2 - Advanced IA!")
        print("Commandes: 'quitter' pour terminer, 'stats' pour les statistiques")
        print("="*60 + "\n")
        
        while True:
            try:
                user_input = input("Vous: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quitter', 'exit', 'bye']:
                    stats = self.get_stats()
                    print(f"\nChatBot: Au revoir! 👋")
                    if stats:
                        print(f"Statistiques: {stats}\n")
                    break
                
                if user_input.lower() == 'stats':
                    stats = self.get_stats()
                    print(f"\nChatBot: Voici mes statistiques:\n{json.dumps(stats, indent=2)}\n")
                    continue
                
                response = self.get_response(user_input)
                print(f"ChatBot: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\nChatBot: Au revoir! À bientôt! 👋\n")
                break


def main():
    """Fonction principale"""
    chatbot = AdvancedChatbot()
    chatbot.chat()


if __name__ == "__main__":
    main()
