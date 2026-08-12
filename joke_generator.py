"""
Joke Generator - Fetch random jokes from external API
Générateur de blagues aléatoires utilisant une API externe
"""

import requests
import json
from typing import Dict, Optional, List


class JokeGenerator:
    """Générateur de blagues utilisant des APIs externes"""
    
    def __init__(self):
        """Initialiser le générateur de blagues"""
        # APIs disponibles pour les blagues
        self.apis = {
            "official_joke_api": "https://official-joke-api.appspot.com/jokes/random",
            "joke_api": "https://v2.jokeapi.dev/joke/Any?format=json",
            "dad_jokes": "https://icanhazdadjoke.com/?format=json"
        }
        self.last_jokes = []
    
    def fetch_from_official_joke_api(self) -> Optional[Dict]:
        """
        Récupérer une blague depuis Official Joke API
        
        Returns:
            Dictionnaire contenant la blague ou None
        """
        try:
            response = requests.get(self.apis["official_joke_api"], timeout=5)
            response.raise_for_status()
            
            data = response.json()
            joke = {
                "setup": data.get("setup", ""),
                "punchline": data.get("punchline", ""),
                "type": data.get("type", "general"),
                "source": "Official Joke API"
            }
            return joke
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur Official Joke API: {e}")
            return None
    
    def fetch_from_joke_api(self) -> Optional[Dict]:
        """
        Récupérer une blague depuis JokeAPI
        
        Returns:
            Dictionnaire contenant la blague ou None
        """
        try:
            response = requests.get(self.apis["joke_api"], timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("error"):
                return None
            
            if data.get("type") == "twopart":
                joke = {
                    "setup": data.get("setup", ""),
                    "delivery": data.get("delivery", ""),
                    "category": data.get("category", ""),
                    "source": "JokeAPI"
                }
            else:
                joke = {
                    "joke": data.get("joke", ""),
                    "category": data.get("category", ""),
                    "source": "JokeAPI"
                }
            return joke
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur JokeAPI: {e}")
            return None
    
    def fetch_from_dad_jokes(self) -> Optional[Dict]:
        """
        Récupérer une blague Dad depuis icanhazdadjoke.com
        
        Returns:
            Dictionnaire contenant la blague ou None
        """
        try:
            response = requests.get(self.apis["dad_jokes"], timeout=5)
            response.raise_for_status()
            
            data = response.json()
            joke = {
                "joke": data.get("joke", ""),
                "type": "dad_joke",
                "source": "icanhazdadjoke.com"
            }
            return joke
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur Dad Jokes API: {e}")
            return None
    
    def get_random_joke(self, api_choice: str = "random") -> Optional[Dict]:
        """
        Récupérer une blague aléatoire
        
        Args:
            api_choice: Choix de l'API ('random', 'official', 'joke', 'dad')
            
        Returns:
            Dictionnaire contenant la blague ou None
        """
        if api_choice == "random":
            apis_list = list(self.apis.keys())
            api_choice = apis_list[0]  # Utiliser Official Joke API par défaut
        
        joke = None
        
        if api_choice == "official" or api_choice == "official_joke_api":
            joke = self.fetch_from_official_joke_api()
        elif api_choice == "joke" or api_choice == "joke_api":
            joke = self.fetch_from_joke_api()
        elif api_choice == "dad" or api_choice == "dad_jokes":
            joke = self.fetch_from_dad_jokes()
        
        if joke:
            self.last_jokes.append(joke)
        
        return joke
    
    def format_joke(self, joke: Dict) -> str:
        """
        Formater la blague pour l'affichage
        
        Args:
            joke: Dictionnaire contenant la blague
            
        Returns:
            Chaîne formatée de la blague
        """
        if not joke:
            return "❌ Impossible de récupérer une blague."
        
        source = joke.get("source", "Unknown")
        formatted = f"\n📝 Blague ({source}):\n"
        formatted += "-" * 50 + "\n"
        
        # Format avec setup et punchline
        if "setup" in joke and "punchline" in joke:
            formatted += f"❓ {joke['setup']}\n"
            formatted += f"😂 {joke['punchline']}\n"
        # Format avec setup et delivery
        elif "setup" in joke and "delivery" in joke:
            formatted += f"❓ {joke['setup']}\n"
            formatted += f"😂 {joke['delivery']}\n"
        # Format simple
        elif "joke" in joke:
            formatted += f"😂 {joke['joke']}\n"
        
        # Ajouter des métadonnées si disponibles
        if "category" in joke:
            formatted += f"🏷️  Catégorie: {joke['category']}\n"
        if "type" in joke and joke["type"] != "general":
            formatted += f"📌 Type: {joke['type']}\n"
        
        formatted += "-" * 50 + "\n"
        return formatted
    
    def display_joke(self, api_choice: str = "random"):
        """
        Afficher une blague formatée
        
        Args:
            api_choice: Choix de l'API
        """
        print("\n⏳ Récupération d'une blague...")
        joke = self.get_random_joke(api_choice)
        print(self.format_joke(joke))
    
    def get_multiple_jokes(self, count: int = 3, api_choice: str = "random") -> List[Dict]:
        """
        Récupérer plusieurs blagues
        
        Args:
            count: Nombre de blagues à récupérer
            api_choice: Choix de l'API
            
        Returns:
            Liste de blagues
        """
        jokes = []
        for i in range(count):
            joke = self.get_random_joke(api_choice)
            if joke:
                jokes.append(joke)
        return jokes
    
    def display_multiple_jokes(self, count: int = 3, api_choice: str = "random"):
        """
        Afficher plusieurs blagues
        
        Args:
            count: Nombre de blagues à afficher
            api_choice: Choix de l'API
        """
        print(f"\n⏳ Récupération de {count} blagues...")
        jokes = self.get_multiple_jokes(count, api_choice)
        
        for i, joke in enumerate(jokes, 1):
            print(f"\n🎯 Blague {i}/{count}")
            print(self.format_joke(joke))
    
    def interactive_menu(self):
        """Menu interactif pour le générateur de blagues"""
        print("\n" + "="*60)
        print("😂 Générateur de Blagues Aléatoires")
        print("="*60)
        
        while True:
            print("\n📋 Menu:")
            print("1. Obtenir une blague (Official Joke API)")
            print("2. Obtenir une blague (JokeAPI)")
            print("3. Obtenir une blague (Dad Jokes)")
            print("4. Obtenir 3 blagues aléatoires")
            print("5. Afficher l'historique des blagues")
            print("6. Quitter")
            
            choice = input("\n➡️  Votre choix (1-6): ").strip()
            
            if choice == "1":
                self.display_joke("official")
            elif choice == "2":
                self.display_joke("joke")
            elif choice == "3":
                self.display_joke("dad")
            elif choice == "4":
                self.display_multiple_jokes(3)
            elif choice == "5":
                self._display_history()
            elif choice == "6":
                print("\n👋 Au revoir! Merci d'avoir utilisé le générateur de blagues!\n")
                break
            else:
                print("❌ Choix invalide. Veuillez réessayer.")
    
    def _display_history(self):
        """Afficher l'historique des blagues"""
        if not self.last_jokes:
            print("\n📭 Aucune blague dans l'historique.")
            return
        
        print(f"\n📚 Historique ({len(self.last_jokes)} blagues):")
        print("-" * 60)
        for i, joke in enumerate(self.last_jokes[-5:], 1):
            print(f"{i}. {self.format_joke(joke)}")


def main():
    """Fonction principale"""
    generator = JokeGenerator()
    generator.interactive_menu()


if __name__ == "__main__":
    main()
