
import tkinter as tk
from tkinter import scrolledtext, messagebox
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

# Define questions and their possible answers
questions = [
    "What is your body type? (a) Thin, (b) Moderate, (c) Solid:",
    "What is your weight in kilograms?",
    "How is your skin texture? (a) Dry, (b) Smooth, (c) Oily",
    "How would you describe your hair texture? (a) Thin and dry, (b) Fine and oily, (c) Thick and lustrous",
    "What is your preference for weather? (a) Warm, (b) Moderate, (c) Cold",
    "How do you handle stress? (a) Anxiety, (b) Irritability, (c) Calmness",
    "How is your appetite? (a) Variable, (b) Strong, (c) Slow and steady",
    "How is your digestion? (a) Irregular, (b) Efficient, (c) Slow but strong",
    "How are your energy levels? (a) Variable, (b) High, (c) Stable",
    "How do you react to spicy foods? (a) Sensitive, (b) Moderate, (c) Strong",
    "How do you handle sadness? (a) Easily affected, (b) Frustrated, (c) Takes time to process",
    "How do you prefer your routine? (a) Adapt easily, (b) Thrive on routine, (c) Need structure",
    "How do you interact socially? (a) Outgoing, (b) Diplomatic, (c) Reserved",
    "How do you express anger? (a) Intense bursts, (b) Lasting anger, (c) Slow to anger",
    "How would you describe your sleep? (a) Light and interrupted, (b) Deep and sound, (c) Long and heavy",
]

answers = {
    "a": "Vata",
    "b": "Pitta",
    "c": "Kapha"
}

# Initialize dosha counters
dosha_counts = {
    "Vata": 0,
    "Pitta": 0,
    "Kapha": 0
}

current_question = 0

# Calculate dosha percentages
def calculate_percentages():
    total_responses = sum(dosha_counts.values())
    percentages = {dosha: (count / total_responses) * 100 for dosha, count in dosha_counts.items()}
    return percentages

# Function to determine the dominant dosha
def find_dominant_dosha(percentages):
    dominant_dosha = max(percentages, key=percentages.get)
    description = {
        "Vata": "Your dominant dosha is Vata. Vata individuals tend to have a thin and creative nature, but they should watch out for anxiety and digestion issues. A warm and grounding diet is recommended.",
        "Pitta": "Your dominant dosha is Pitta. Pitta individuals are often intelligent and ambitious but may experience issues like acidity and skin problems. Cooling and soothing foods are beneficial.",
        "Kapha": "Your dominant dosha is Kapha. Kapha individuals are typically calm and compassionate, but they should be cautious of weight gain and congestion. A diet with light and spicy foods is advised."
    }
    
    return description.get(dominant_dosha)


# Function to handle user input and update the conversation
def handle_user_input(event=None):
    global current_question

    user_input = user_entry.get().lower()

    if current_question < len(questions):
        if current_question == 1:
            try:
                weight = int(user_input)
                if weight <= 0:
                    messagebox.showinfo("Invalid Weight", "Weight cannot be negative. Please enter a valid weight.")
                else:
                    # Classify weight into categories
                    if weight < 60:
                        dosha_counts["Vata"] += 1
                    elif 60 <= weight < 75:
                        dosha_counts["Pitta"] += 1
                    else:
                        dosha_counts["Kapha"] += 1
                    current_question += 1
                    user_responses.config(state=tk.NORMAL)
                    user_responses.insert(tk.END, f"you: {weight}\n")
                    user_responses.config(state=tk.DISABLED)
                    user_entry.delete(0, tk.END)
                    # Display the next question if available
                    if current_question < len(questions):
                        user_responses.config(state=tk.NORMAL)
                        user_responses.insert(tk.END, f"\nPrakriti Chatbot: {questions[current_question]}\n")
                        user_responses.config(state=tk.DISABLED)
            except ValueError:
                messagebox.showinfo("Invalid Input", "Please enter a valid integer for weight.")
        else:
            answer_key = answers.get(user_input)
            if answer_key:
                dosha_counts[answer_key] += 1
                current_question += 1
                user_responses.config(state=tk.NORMAL)
                user_responses.insert(tk.END, f"you: {user_input}\n")
                user_responses.config(state=tk.DISABLED)
                user_entry.delete(0, tk.END)

                # Display the next question if available
                if current_question < len(questions):
                    user_responses.config(state=tk.NORMAL)
                    user_responses.insert(tk.END, f"\nPrakriti Chatbot: {questions[current_question]}\n")
                    user_responses.config(state=tk.DISABLED)
            else:
                messagebox.showinfo("Invalid Answer", "Please select a valid option.")
    else:
        percentages = calculate_percentages()
        user_responses.config(state=tk.NORMAL)
        user_responses.insert(tk.END, "\nPrakriti Assessment Results:\n")
        for dosha, percentage in percentages.items():
            user_responses.insert(tk.END, f"{dosha}: {percentage:.2f}%\n")
        user_responses.config(state=tk.DISABLED)
        dominant_dosha = find_dominant_dosha(percentages)
        user_responses.config(state=tk.NORMAL)
        user_responses.insert(tk.END, f"\nPrakriti Chatbot: Your dominant dosha is {dominant_dosha}.\n")
        user_responses.config(state=tk.DISABLED)

        # Create and display a pie chart
        labels = dosha_counts.keys()
        sizes = dosha_counts.values()
        colors = ['#056608', '#0047ab', '#850101']
        max_percentage_index = list(sizes).index(max(sizes))
        explode = [0.1 if i == max_percentage_index else 0 for i in range(len(sizes))]

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, colors=colors, explode=explode, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Prakriti Assessment Results')
        plt.show()

# Create a GUI window
window = tk.Tk()
window.title("Prakriti Assessment Chatbot")

# Load the background image
bg_image = Image.open("C:/Users/Anurag Dey/OneDrive/Desktop/SIH/meditation-7308899_960_720.jpg")  # Replace "background.jpg" with your image file path
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label for the background image
bg_label = tk.Label(window, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Configure the appearance of the message box
message_box_style = {
    "bg": "#E0A96D",  # Background color set to Prussian Blue
    "fg": "#201E20",   # Text color
    "font": ("Cambria", 20)  # Text font
}

# Create a scrolled text widget for the chat display
user_responses = scrolledtext.ScrolledText(
    window,
    wrap=tk.WORD,
    width=60,
    height=20,
    **message_box_style  # Apply the message box style
)
user_responses.pack(padx=10, pady=10)
user_responses.config(state=tk.DISABLED)

# Create an entry field for user responses
user_entry = tk.Entry(window, font=("Bookman Old Style", 18), width=40)
user_entry.bind('<Return>', handle_user_input)
user_entry.pack(pady=10)
send_button = tk.Button(window, text="Send", command=handle_user_input, font=('Helvetica', 12))
send_button.pack()

# Initialize the conversation with an initial message
user_responses.config(state=tk.NORMAL)
user_responses.insert(tk.END, "Prakriti Chatbot: Hi, I'm Prakriti Chatbot! I'll assist you to determine your prakriti. "
                             "I'll ask you some questions, and you have to answer them with the provided options (a, b, c). "
                             "Let's get started!\n\n")
user_responses.insert(tk.END, f"\nPrakriti Chatbot: {questions[current_question]}\n")
user_responses.config(state=tk.DISABLED)

# Run the GUI main loop
window.mainloop()
