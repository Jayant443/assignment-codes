import re
import random
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
BOT_NAME = "Robi"
CREATOR = "an SE assignment"
STOPWORDS = {"a", "an", "the", "is", "are", "was", "were", "be", "been", "being", "am", "do", "does", "did", "i",
             "me", "my", "mine", "you", "your", "yours", "we", "our", "us", "about", "of", "to", "and", "or", "in",
             "on", "at", "for", "it", "this", "that", "what", "who", "whom", "whose", "when", "where", "why", "how",
             "which", "can", "could", "would", "should", "will", "shall", "say", "said", "tell", "told", "know",
             "knew", "remember", "recall", "search", "find", "again", "mention", "mentioned", "chat", "conversation",
             "talk", "talked", "anything", "something", "please"}
RECALL_HINT = r"\b(remember|recall|our (?:chat|conversation)|we (?:talked|discussed)|i (?:said|told|mentioned)|did i (?:say|tell|mention)|what did i|what have i|do i (?:say|tell|mention))\b"
QUESTION_START = r"^\s*(what|who|whom|whose|when|where|why|how|which|do|did|does|have|has|had|can|could|would|should|is|are|was|were|tell|remind|recall|search|show|list|any)\b"
CLAUSE_SPLIT = re.compile(r"\s*(?:[,;.!?]|\band\b|\bbut\b|\bbecause\b|\bso\b)\s*")
PRONOUNS = [(r"\bi'm\b", "you're"), (r"\bi am\b", "you are"), (r"\bi've\b", "you've"), (r"\bi'll\b", "you'll"),
            (r"\bmy\b", "your"), (r"\bmine\b", "yours"), (r"\bme\b", "you"), (r"\bi\b", "you")]
VALUE_TRIGGERS = r"(?:is|are|was|were|am|be|named|called|in|at|on|from|as|like|likes|love|loves|learning|studying|using|knows|works|works? as)"
RULES = [(r"\b(hi|hello|hey|hola|namaste)\b", [
        "Hello! I'm {bot}. How can I help you today?", "Hey there! {bot} at your service.", "Hi! What would you like to talk about?",
    ]), (r"\bhow are you\b|\bhow's it going\b|\bwhats up\b|\bwhat's up\b", [
        "I'm just a bunch of rules, but I'm running great! How about you?", "All logic and no feelings, and that suits me fine. You?",
    ]), (r"\byour name\b|\bwho are you\b|\bwhat are you\b", [
        "I'm {bot}, a rule-based chatbot built with if-then logic.", "The name's {bot}. I match your words to rules and reply.",
    ]), (r"\bwho (made|created|built) you\b", [ "I was built for {creator} using Python and tkinter.",]), 
    (r"\b(what )?can you do\b|\bhelp\b|\byour features\b", [
        "I can chat, tell the time and date, answer simple questions, and respond to keywords. ", 
        "I also remember our whole chat - ask me 'what did I tell you about ...' and I'll search it.", "Try: hello, time, date, joke, bye.",
    ]), (r"\btime\b|\bclock\b", [lambda: f"The time is {datetime.now().strftime('%H:%M:%S')}."]),
    (r"\bdate\b|\btoday\b|\bday is it\b", [lambda: f"Today is {datetime.now().strftime('%A, %d %B %Y')}."]),
    (r"\bjoke\b|\bfunny\b", [
        "Why did the programmer quit his job? Because he didn't get arrays.", "Why do Java developers wear glasses? Because they don't C#.",
        "There are 10 kinds of people: those who understand binary and those who don't.",
    ]),
    (r"\b(thanks|thank you|thx)\b", ["You're welcome!", "Anytime! That's what rules are for."]),
    (r"\b(bye|goodbye|see you|exit)\b", ["Goodbye! Type 'bye' again or close the window.", "See you later!"]),
    (r"\byour (creator|author)\b", ["I was created for {creator}."]),
    (r"\b(love|like) you\b", ["Aww, that's a nice string of characters. I'm flattered."]),
    (r"\bweather\b", ["I don't have a weather feed, but I hope it's nice outside!"]),
    (r"^\s*(-?\d+)\s*([\+\-\*/])\s*(-?\d+)\s*$", ["__MATH__"]),
    (r"\bcalculate\b|\bmath\b|\d+\s*[\+\-\*/]\s*\d+", ["I only do simple math rules. Ask me simple arithmetic like '2 + 3'."])]
FALLBACKS = ["I'm rule-based, so I only know certain things. Type 'help'.",
    "I don't have a rule for that yet. Try 'help' to see what I know.", "Hmm, that didn't match any rule. Could you rephrase?",]
class Memory:
    def __init__(self): self.history = []
    def remember(self, sender, text): self.history.append({"sender": sender, "text": text, "time": datetime.now()})
    def keywords(self, message): return [w for w in re.findall(r"[a-z0-9']+", message.lower()) if len(w) > 1 and w not in STOPWORDS]
    def search(self, message, limit=5):
        keys = self.keywords(message)
        if not keys: return []
        scored = []
        for i, entry in enumerate(self.history):
            low = entry["text"].lower()
            score = sum(1 for k in keys if re.search(rf"\b{re.escape(k)}\b", low))
            if score: scored.append((score, i, entry))
        scored.sort(key=lambda t: (-t[0], -t[1]))
        hits, seen = [], set()
        for _, _, entry in scored:
            key = (entry["sender"], entry["text"].lower())
            if key in seen: continue
            seen.add(key)
            hits.append(entry)
            if len(hits) >= limit: break
        return hits
def is_question(text):
    low = text.strip().lower()
    return low.endswith("?") or bool(re.search(QUESTION_START, low))
class Memory:
    def __init__(self): self.history = []
    def remember(self, sender, text): self.history.append({"sender": sender, "text": text, "time": datetime.now()})
    def keywords(self, message): return [w for w in re.findall(r"[a-z0-9']+", message.lower()) if len(w) > 1 and w not in STOPWORDS]
    def _score(self, keys, text):
        low = text.lower()
        return sum(1 for k in keys if re.search(rf"\b{re.escape(k)}", low))
    def _best_entry(self, keys):
        found = [(self._score(keys, e["text"]), e["sender"] == "You", i, e) for i, e in enumerate(self.history) if not is_question(e["text"])]
        found.sort(key=lambda t: (-t[0], not t[1], -t[2]))
        return found[0][3] if found and found[0][0] > 0 else None
    def _best_clause(self, keys, sentence, question):
        clauses = [c.strip() for c in CLAUSE_SPLIT.split(sentence) if c.strip()]
        if re.search(r"\bwhere\b", question.lower()):
            located = [c for c in clauses if re.search(r"\b(in|at|near|on|from|to)\b", c.lower())]
            if located: clauses = located
        scored = sorted(((self._score(keys, c), i, c) for i, c in enumerate(clauses)), key=lambda t: (-t[0], -t[1]))
        return scored[0][2]
    def answer(self, question):
        keys = self.keywords(question)
        if not keys: return None
        entry = self._best_entry(keys)
        if not entry: return None
        clause = self._best_clause(keys, entry["text"], question)
        if len(clause.split()) < 3: clause = entry["text"]
        if entry["sender"] == "You":
            for pattern, replacement in PRONOUNS: clause = re.sub(pattern, replacement, clause, flags=re.I)
        return prettify(clause)
def prettify(text):
    t = text.strip().strip("?.,! ")
    if not t: return t
    t = t[0].upper() + t[1:]
    t = re.sub(rf"\b{VALUE_TRIGGERS}\s+([a-z][\w'-]*)$", lambda m: f"{m.group(0)[:m.group(0).rfind(' ')]} {m.group(1).capitalize()}", t)
    return t + "."
def get_response(message, memory=None):
    text = message.strip()
    if not text: return "Say something and I'll respond!"
    low = text.lower()
    recall = re.search(RECALL_HINT, low)
    if memory is not None and recall:
        ans = memory.answer(text)
        if ans: return ans
    for pattern, responses in RULES:
        match = re.search(pattern, low)
        if match:
            choice = random.choice(responses)
            if choice == "__MATH__":
                a, op, b = int(match.group(1)), match.group(2), int(match.group(3))
                result = {"+": a + b, "-": a - b, "*": a * b, "/": a / b if b else None}[op]
                if result is None: return "I can't divide by zero, even with rules."
                return f"{a} {op} {b} = {result}"
            if callable(choice): return choice()
            return choice.format(bot=BOT_NAME, creator=CREATOR)
    if memory is not None and (is_question(text) or recall):
        ans = memory.answer(text)
        if ans: return ans
        if recall: return "I don't think we talked about that."
    return random.choice(FALLBACKS)
class ChatApp:
    def __init__(self, root):
        self.root = root
        self.memory = Memory()
        root.title(f"{BOT_NAME} - Rule-Based Chatbot")
        root.geometry("520x600")
        root.configure(bg="#f5f5f7")
        header = tk.Frame(root, bg="#89b4fa", height=56)
        header.pack(fill="x")
        tk.Label(header, text=f"{BOT_NAME}", bg="#89b4fa", fg="#ffffff", font=("Segoe UI", 16, "bold")).pack(side="left", padx=16, pady=10)
        tk.Label(header, text="rule-based chatbot", bg="#89b4fa", fg="#eef3ff", font=("Segoe UI", 10)).pack(side="left")
        self.chat = scrolledtext.ScrolledText(root, wrap="word", bg="#ffffff", fg="#2e2e38", font=("Segoe UI", 11), bd=0, state="disabled", padx=12, pady=8)
        self.chat.pack(fill="both", expand=True, padx=8, pady=(8, 0))
        self.chat.tag_config("bot", foreground="#1e66f5", font=("Segoe UI", 11, "bold"))
        self.chat.tag_config("user", foreground="#40a02b", font=("Segoe UI", 11, "bold"))
        self.chat.tag_config("msg", foreground="#2e2e38")
        bottom = tk.Frame(root, bg="#f5f5f7")
        bottom.pack(fill="x", padx=8, pady=8)
        self.entry = tk.Entry(bottom, bg="#ffffff", fg="#2e2e38", insertbackground="#2e2e38", font=("Segoe UI", 12), bd=0, relief="flat",
                               highlightthickness=1, highlightbackground="#d5d8e0", highlightcolor="#1e66f5")
        self.entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))
        self.entry.bind("<Return>", lambda e: self.send())
        tk.Button(bottom, text="Send", command=self.send, bg="#1e66f5", fg="#ffffff", font=("Segoe UI", 11, "bold"), bd=0, padx=18, pady=6,
                  activebackground="#7287fd", activeforeground="#ffffff").pack(side="right")
        self.welcome()
        self.entry.focus_set()
    def append(self, sender, text):
        self.chat.configure(state="normal")
        self.chat.insert("end", f"{sender}: ", sender.lower())
        self.chat.insert("end", f"{text}\n\n", "msg")
        self.chat.see("end")
        self.chat.configure(state="disabled")
    def welcome(self): self.append(BOT_NAME, f"Hi, I'm {BOT_NAME}! Type 'help' to see what I can do. I also remember our chat.")
    def send(self):
        text = self.entry.get().strip()
        if not text: return
        self.entry.delete(0, "end")
        self.append("You", text)
        self.memory.remember("You", text)
        reply = get_response(text, self.memory)
        self.append(BOT_NAME, reply)
        self.memory.remember(BOT_NAME, reply)
def main():
    root = tk.Tk()
    ChatApp(root)
    root.mainloop()
if __name__ == "__main__":
    main()
