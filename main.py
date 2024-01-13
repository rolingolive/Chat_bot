import json
from difflib import get_close_matches
import tkinter as tk
from tkinter import scrolledtext

# Import knowledge base data
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

# Function that is going to save the data so that it can be used next time
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Will find the best match from the dictionary
# Will take user question, go into the knowledge base, and find the best response, if no responses match it will return None
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_questions(questions: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == questions:
            return q["answer"]

def chat_bot():
    knowledge_base: dict = load_knowledge_base('Knowledge_base.json')

    window = tk.Tk()
    window.title("Chatbot")

    # Create a scrolled text widget to display the conversation
    conversation_display = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=15)
    conversation_display.grid(row=0, column=0, columnspan=2)

    # Entry widget for user input
    user_input_entry = tk.Entry(window, width=30)
    user_input_entry.grid(row=1, column=0)

    def process_user_input():
        user_input = user_input_entry.get()
        conversation_display.insert(tk.END, f"You: {user_input}\n")

        if user_input.lower() == 'quit':
            window.destroy()
            return

        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer = get_answer_for_questions(best_match, knowledge_base)
            conversation_display.insert(tk.END, f"Bot: {answer}\n")
        else:
            conversation_display.insert(tk.END, "Bot: I don't know the answer. Can you teach me? 😊\n")
            conversation_display.insert(tk.END, "Bot: Type the answer or skip to skip\n")

            # Entry widget for user to type the answer
            new_answer_entry = tk.Entry(window, width=30)
            new_answer_entry.grid(row=2, column=0)

            # Button to submit the new answer
            submit_new_answer_button = tk.Button(window, text="Teach Botchan!", command=lambda: submit_new_answer(new_answer_entry))
            submit_new_answer_button.grid(row=2, column=1)

    def submit_new_answer(entry_widget):
        new_answer = entry_widget.get()
        conversation_display.insert(tk.END, f"Bot: Thank you! Bot learned something new: {new_answer} 😊!\n")
        knowledge_base["questions"].append({"question": user_input_entry.get(), "answer": new_answer})
        save_knowledge_base('Knowledge_base.json', knowledge_base)
        entry_widget.delete(0, tk.END)  # Clear the entry

    # Button to submit user input
    submit_button = tk.Button(window, text="Submit", command=process_user_input)
    submit_button.grid(row=1, column=1)

    window.mainloop()

if __name__ == '__main__':
    chat_bot()
