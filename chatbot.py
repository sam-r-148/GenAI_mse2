#!/usr/bin/env python3
"""
Conversational Bot — Vanilla RNN (NumPy) + NLTK preprocessing.
"""

import json
import os
import pickle
import random
import sys
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder

# Download required resources
for resource in ("punkt", "wordnet"):
    nltk.download(resource, quiet=True)

# ── Configuration ─────────────────────────────────────────────
HIDDEN_SIZE = 64
LEARNING_RATE = 0.005
EPOCHS = 600
CONFIDENCE_THRESHOLD = 0.6   # FIXED
INTENTS_FILE = "intents.json"
MODEL_DIR = "model_artifacts"
# ─────────────────────────────────────────────────────────────

lemmatizer = WordNetLemmatizer()

# ── Preprocessing ─────────────────────────────────────────────

def preprocess(text: str) -> list:
    tokens = nltk.word_tokenize(text.lower())
    return [lemmatizer.lemmatize(tok) for tok in tokens if tok.isalpha()]  # FIXED


def build_vocabulary(intents: dict) -> dict:
    vocab = set()
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            vocab.update(preprocess(pattern))
    return {word: idx for idx, word in enumerate(sorted(vocab))}


def _one_hot(idx: int, size: int) -> np.ndarray:
    vec = np.zeros((size, 1))
    vec[idx] = 1.0   # FIXED
    return vec


def tokens_to_one_hot(tokens: list, vocab: dict) -> list:
    size = len(vocab)
    vectors = [_one_hot(vocab[tok], size) for tok in tokens if tok in vocab]
    return vectors if vectors else [np.zeros((size, 1))]

# ── RNN ──────────────────────────────────────────────────────

class VanillaRNN:
    def __init__(self, input_size, hidden_size, output_size, lr):
        self.lr = lr
        self.hidden_size = hidden_size

        self.Wxh = np.random.randn(hidden_size, input_size) * np.sqrt(2.0 / input_size)
        self.Whh = np.random.randn(hidden_size, hidden_size) * np.sqrt(2.0 / hidden_size)
        self.Why = np.random.randn(output_size, hidden_size) * np.sqrt(2.0 / hidden_size)
        self.bh = np.zeros((hidden_size, 1))
        self.by = np.zeros((output_size, 1))

    def forward(self, inputs):
        h = np.zeros((self.hidden_size, 1))
        self._inputs = inputs
        self._hs = {0: h.copy()}

        for t, x in enumerate(inputs):
            h = np.tanh(self.Wxh @ x + self.Whh @ h + self.bh)
            self._hs[t + 1] = h.copy()

        logits = self.Why @ h + self.by
        probs = _softmax(logits)
        return probs

    def backward(self, probs, target_idx):
        n = len(self._inputs)

        d_logits = probs.copy()
        d_logits[target_idx] -= 1.0

        d_Why = d_logits @ self._hs[n].T
        d_by = d_logits.copy()
        d_Whh = np.zeros_like(self.Whh)
        d_Wxh = np.zeros_like(self.Wxh)
        d_bh = np.zeros_like(self.bh)

        d_h = self.Why.T @ d_logits

        for t in reversed(range(n)):
            dtanh = (1.0 - self._hs[t + 1] ** 2) * d_h   # FIXED
            d_bh += dtanh
            d_Wxh += dtanh @ self._inputs[t].T
            d_Whh += dtanh @ self._hs[t].T
            d_h = self.Whh.T @ dtanh

        for grad in (d_Wxh, d_Whh, d_Why, d_bh, d_by):
            np.clip(grad, -5, 5, out=grad)

        self.Wxh -= self.lr * d_Wxh
        self.Whh -= self.lr * d_Whh
        self.Why -= self.lr * d_Why
        self.bh -= self.lr * d_bh
        self.by -= self.lr * d_by

        return float(-np.log(probs[target_idx, 0] + 1e-8))

    def predict(self, inputs):
        return self.forward(inputs)

    def save(self, path):
        np.savez(
            path,
            Wxh=self.Wxh, Whh=self.Whh, Why=self.Why,
            bh=self.bh, by=self.by,
            meta=np.array([self.hidden_size, self.lr]),
        )

    @classmethod
    def load(cls, path):
        d = np.load(path)
        hs = int(d["meta"][0])
        lr = float(d["meta"][1])
        rnn = cls(d["Wxh"].shape[1], hs, d["Why"].shape[0], lr)
        rnn.Wxh, rnn.Whh, rnn.Why = d["Wxh"], d["Whh"], d["Why"]
        rnn.bh, rnn.by = d["bh"], d["by"]
        return rnn


def _softmax(x):
    e_x = np.exp(x - np.max(x))   # FIXED
    return e_x / e_x.sum()

# ── Training ─────────────────────────────────────────────

def prepare_training_data(intents, vocab, encoder):
    data = []
    classes = list(encoder.classes_)
    for intent in intents["intents"]:
        label_idx = classes.index(intent["tag"])
        for pattern in intent["patterns"]:
            tokens = preprocess(pattern)
            vectors = tokens_to_one_hot(tokens, vocab)
            data.append((vectors, label_idx))
    return data


def train_and_save(intents):
    print("Building vocabulary...")
    vocab = build_vocabulary(intents)

    tags = [intent["tag"] for intent in intents["intents"]]
    encoder = LabelEncoder()
    encoder.fit(tags)

    training_data = prepare_training_data(intents, vocab, encoder)

    rnn = VanillaRNN(len(vocab), HIDDEN_SIZE, len(encoder.classes_), LEARNING_RATE)

    for epoch in range(EPOCHS):
        random.shuffle(training_data)
        total_loss = 0

        for vectors, label_idx in training_data:
            probs = rnn.forward(vectors)
            loss = rnn.backward(probs, label_idx)
            total_loss += loss

        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Loss: {total_loss:.4f}")

    os.makedirs(MODEL_DIR, exist_ok=True)
    rnn.save(os.path.join(MODEL_DIR, "rnn_weights.npz"))

    with open(os.path.join(MODEL_DIR, "vocab.pkl"), "wb") as f:
        pickle.dump(vocab, f)

    with open(os.path.join(MODEL_DIR, "encoder.pkl"), "wb") as f:
        pickle.dump(encoder, f)

    return rnn, vocab, encoder


def load_artifacts():
    rnn = VanillaRNN.load(os.path.join(MODEL_DIR, "rnn_weights.npz"))

    with open(os.path.join(MODEL_DIR, "vocab.pkl"), "rb") as f:
        vocab = pickle.load(f)

    with open(os.path.join(MODEL_DIR, "encoder.pkl"), "rb") as f:
        encoder = pickle.load(f)

    return rnn, vocab, encoder


def artifacts_exist():
    return all(
        os.path.exists(os.path.join(MODEL_DIR, f))
        for f in ["rnn_weights.npz", "vocab.pkl", "encoder.pkl"]
    )

# ── Inference ─────────────────────────────────────────────

def predict_intent(text, rnn, vocab, encoder):
    tokens = preprocess(text)
    vectors = tokens_to_one_hot(tokens, vocab)
    probs = rnn.predict(vectors)
    idx = int(np.argmax(probs))
    return encoder.classes_[idx], float(probs[idx])


def get_response(tag, intents):
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])
    return "I don't understand."


def start_chat(intents, rnn, vocab, encoder):
    print("Bot is ready! Type 'quit' to exit.")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit"]:
            break

        tag, confidence = predict_intent(user_input, rnn, vocab, encoder)

        if confidence < CONFIDENCE_THRESHOLD:
            print("Bot: I didn't understand that.")
        else:
            print("Bot:", get_response(tag, intents))


def main():
    if not os.path.exists(INTENTS_FILE):
        print("intents.json not found!")
        return

    with open(INTENTS_FILE) as f:
        intents = json.load(f)

    if not artifacts_exist():
        rnn, vocab, encoder = train_and_save(intents)
    else:
        rnn, vocab, encoder = load_artifacts()

    start_chat(intents, rnn, vocab, encoder)


if __name__ == "__main__":
    main()