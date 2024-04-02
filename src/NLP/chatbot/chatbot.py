import numpy as np
import torch
import torch.nn as nn
from NLP.features_extractor.bag_of_words import BagOfWords
from NLP.modeling.neural_net import NeuralNet
import json

from NLP.preprocessing.text_preprocessor import TextPreprocessor
from utilities.file_searcher import PathFinder


class ChatBot:
    def __init__(self, model_file):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model, self.bag_of_words, self.all_words, self.tags = self.load_model(model_file)
        self.model.eval()
        filename = PathFinder().get_complet_path('ressources/intents/intents.json')
        # Load intents data from JSON file
        with open(filename, 'r', encoding='utf-8') as file:
            self.intents_data = json.load(file)

    def load_model(self, model_file):
        data = torch.load(model_file, map_location=self.device)
        input_size = data["input_size"]
        hidden_size = data["hidden_size"]
        output_size = data["output_size"]
        all_words = data["all_words"]
        tags = data["tags"]

        model = NeuralNet(input_size, hidden_size, output_size).to(self.device)
        model.load_state_dict(data["model_state"])

        bag_of_words = BagOfWords(prepocessor=TextPreprocessor())  # Make sure this matches your actual implementation

        return model, bag_of_words, all_words, tags

    def get_response(self, sentence) -> str:
        X = self.bag_of_words.extract_features(sentence)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(dtype=torch.float).to(self.device)

        output = self.model(X)
        _, predicted = torch.max(output, dim=1)

        tag = self.tags[predicted.item()]

        probabilities = torch.softmax(output, dim=1)
        prob = probabilities[0][predicted.item()]
        
        if prob.item() > 0.75:
            for intent in self.intents_data['intents']:
                if tag == intent["tag"]:
                    return np.random.choice(intent['responses'])
        return "I do not understand..."
