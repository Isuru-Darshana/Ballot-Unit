from tkinter import *
from tkinter import messagebox, font
import cups

votes = {1: 0, 2: 0, 3: 0, 4: 0, 'None': 0}
sequence_number = 65610  # Starting sequence number

def get_candidate_file_path(candidate_number):
    
    file_name = {
        1: 'A',
        2: 'B',
        3: 'C',
        4: 'D',
        'None': 'X'
    }.get(candidate_number, 'X')  
    return f'{file_name}_{sequence_number}.pdf'

def on_vote(candidate_number):
    global sequence_number
    candidate_label = 'Candidate ' + str(candidate_number) if candidate_number != 'None' else 'None of the above'
    response = messagebox.askyesno("Confirm Vote", f"Are you sure you want to vote for {candidate_label}?")
    if response:
        votes[candidate_number] += 1
        sequence_number += 1  # Increment sequence number after each vote
        messagebox.showinfo("Vote Recorded", f"Your vote for {candidate_label} has been recorded.")
        vote_amount()
        print_vote(candidate_number)
#Results on the Backend
def vote_amount():
    total_votes = sum(votes.values())
    print(f"Total Votes: {total_votes}")
    for candidate, vote_count in votes.items():
        candidate_name = f"Candidate {candidate}" if candidate != 'None' else 'None of the above'
        percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
        print(f"{candidate_name}: {vote_count} votes, {percentage:.2f}% of total")

#Print the Ballot
def print_vote(candidate_number):
    conn = cups.Connection()
    printers = conn.getPrinters()
    default_printer = list(printers.keys())[0]
    print_file_path = get_candidate_file_path(candidate_number)
    if print_file_path:
        conn.printFile(default_printer, print_file_path, f"Vote for {candidate_number}", {})
    else:
        messagebox.showerror("Print Error", "No file associated with this candidate.")

#GUI Interface
root = Tk()
root.title("CAST YOUR VOTE")
root.geometry("1024x600")
root.configure(bg='black')

title_font = font.Font(family="Arial", size=50, weight="bold")
title_label = Label(root, text="CAST YOUR VOTE", font=title_font, fg="white", bg='black')
title_label.pack(pady=50)

button_font = ("Helvetica", 20)
for i in range(1, 5):
    button = Button(root, text=f"Vote for Candidate {i}", bg="Blue", fg="White", font=button_font, command=lambda i=i: on_vote(i))
    button.pack(fill='x', padx=50, pady=10)

none_button = Button(root, text="None of the above", bg="Blue", fg="White", font=button_font, command=lambda: on_vote('None'))
none_button.pack(fill='x', padx=50, pady=10)

root.mainloop()
