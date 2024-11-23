import tkinter as tk
from tkinter import messagebox


class Game:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("The Soul's Journey")
        self.window.geometry("800x600")  # Larger window size
        self.acceptance_percentage = 0
        self.step = 0
        self.max_steps = 4  # End the game after 4 responses

        # Load or create small images
        try:
            self.body_image = tk.PhotoImage(file="body.png").subsample(6, 6)  # Smaller image
        except Exception:
            self.body_image = tk.PhotoImage(width=50, height=50)  # Placeholder if missing

        try:
            self.soul_image = tk.PhotoImage(file="soul.png").subsample(6, 6)  # Smaller image
        except Exception:
            self.soul_image = tk.PhotoImage(width=50, height=50)  # Placeholder if missing

        try:
            self.narrator_image = tk.PhotoImage(file="narrator.png").subsample(6, 6)  # Smaller image
        except Exception:
            self.narrator_image = tk.PhotoImage(width=50, height=50)  # Placeholder if missing

        self.conversation = [
            {"text": "Oh, I feel something weird.", "speaker": "Body"},
            {"text": "Oh no, what is happening? Is my soul leaving me?", "speaker": "Body"},
            {"text": "The soul has left the body.", "speaker": "Narrator"},
            {"text": "This world feels so lonely without the body to interact with.", "speaker": "Soul"},
            {"text": "I must return to my body and restore balance.", "speaker": "Soul"},
            {"text": "Why should I let you back after you abandoned me?", "speaker": "Body"},
        ]
        self.responses = [
            [
                {"text": "I am a part of you; without me, you are incomplete.", "effect": 25},
                {"text": "I made a mistake leaving, and I seek to make it right.", "effect": 25},
                {"text": "You are nothing without me.", "effect": -10},
                {"text": "I don’t care about you—I just want my place back.", "effect": -10},
            ],
            [
                {"text": "I understand your pain, but together, we are stronger.", "effect": 25},
                {"text": "Let’s rebuild our connection and thrive again.", "effect": 25},
                {"text": "You’re weak without me; admit it.", "effect": -10},
                {"text": "I don’t need you, but you need me.", "effect": -10},
            ],
            [
                {"text": "I promise to honor our bond and grow together.", "effect": 25},
                {"text": "The body and soul are one; let’s reunite.", "effect": 25},
                {"text": "You’re just a vessel—I am the essence.", "effect": -10},
                {"text": "This separation is your fault for being so fragile.", "effect": -10},
            ],
            [
                {"text": "We can be stronger by forgiving each other.", "effect": 25},
                {"text": "I truly regret leaving, and I need you.", "effect": 25},
                {"text": "You exist because of me; accept this.", "effect": -10},
                {"text": "I will force you to let me back.", "effect": -10},
            ],
        ]

        self.create_ui()

    def create_ui(self):
        # Conversation frame with text and images
        self.conversation_frame = tk.Frame(self.window)
        self.conversation_frame.pack(pady=10)

        self.conversation_canvas = tk.Canvas(self.conversation_frame, width=700, height=350)
        self.conversation_scrollbar = tk.Scrollbar(
            self.conversation_frame, orient="vertical", command=self.conversation_canvas.yview
        )
        self.conversation_scrollable_frame = tk.Frame(self.conversation_canvas)

        self.conversation_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.conversation_canvas.configure(scrollregion=self.conversation_canvas.bbox("all")),
        )
        self.conversation_canvas.create_window((0, 0), window=self.conversation_scrollable_frame, anchor="nw")
        self.conversation_canvas.configure(yscrollcommand=self.conversation_scrollbar.set)

        self.conversation_canvas.pack(side="left", fill="both", expand=True)
        self.conversation_scrollbar.pack(side="right", fill="y")

        # Response buttons
        self.response_frame = tk.Frame(self.window)
        self.response_frame.pack(pady=10)

        # Acceptance percentage label
        self.acceptance_label = tk.Label(self.window, text="Acceptance percentage: 0%")
        self.acceptance_label.pack(pady=5)

        self.display_conversation()

    def display_conversation(self):
        for widget in self.conversation_scrollable_frame.winfo_children():
            widget.destroy()

        for line in self.conversation:
            frame = tk.Frame(self.conversation_scrollable_frame)
            frame.pack(anchor="w", pady=5)

            # Add character image if applicable
            if line["speaker"] == "Body":
                img_label = tk.Label(frame, image=self.body_image)
            elif line["speaker"] == "Soul":
                img_label = tk.Label(frame, image=self.soul_image)
            elif line["speaker"] == "Narrator":
                img_label = tk.Label(frame, image=self.narrator_image)
            else:
                img_label = tk.Label(frame, width=4)  # Placeholder for other speakers

            img_label.pack(side="left", padx=5)

            # Add conversation text
            text_label = tk.Label(frame, text=f"{line['speaker']}: {line['text']}", wraplength=600, anchor="w")
            text_label.pack(side="left", fill="x")

        if self.step < self.max_steps:
            self.display_responses()
        else:
            self.end_game()

    def display_responses(self):
        for widget in self.response_frame.winfo_children():
            widget.destroy()

        for response in self.responses[self.step]:
            button = tk.Button(
                self.response_frame,
                text=response["text"],
                command=lambda response=response: self.choose_response(response),
                wraplength=400,  # Wrap text for long options
                anchor="w",
            )
            button.pack(pady=2, fill=tk.X)

    def choose_response(self, response):
        self.acceptance_percentage += response["effect"]
        self.acceptance_label["text"] = f"Acceptance percentage: {self.acceptance_percentage}%"
        self.conversation.append({"text": response["text"], "speaker": "Soul"})
        self.step += 1
        self.display_conversation()

    def end_game(self):
        for widget in self.response_frame.winfo_children():
            widget.destroy()

        if self.acceptance_percentage >= 100:
            final_message = "The body has fully accepted the soul back. You are reunited in harmony!"
        else:
            final_message = (
                "The body has not fully accepted the soul back. You remain separated."
                "\nTry again to reach 100% acceptance."
            )

        final_label = tk.Label(self.response_frame, text=final_message, wraplength=400)
        final_label.pack(pady=10)

        messagebox.showinfo("Game Over", final_message)

    def play(self):
        self.window.mainloop()


# Start the game
if __name__ == "__main__":
    game = Game()
    game.play()
