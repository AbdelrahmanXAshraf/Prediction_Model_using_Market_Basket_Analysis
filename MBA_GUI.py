"""Created By: Abdelrahman Ashraf 152761"""
import MBA_Main
import os
from tkinter import messagebox as mb
from tkinter import filedialog
from tkinter import *
from datetime import datetime
import matplotlib.pyplot as plt

now = datetime.now()


def button_plot_callback():
    support_threshold = float(entry_support.get())
    confidence_threshold = float(entry_confidence.get())
    input_file = entry_filename.get()
    if os.path.splitext(input_file)[1] == ".csv":
        text.delete(1.0, END)
        data = MBA_Main.read_data(input_file)
        rules = ['{} => {}'.format(item_set, item)
                 for item_set, item in MBA_Main.apriori(data[1:], support_threshold, confidence_threshold)]

        lift = ['lift = {:.2f}'.format(MBA_Main.lift(data[1:], item_set, {item}))
                for item_set, item in MBA_Main.apriori(data[1:], support_threshold, confidence_threshold)]
        # for i in range(0,len(lift)):
        #     lift[int(i)] = int(lift[i])

        y_positions = range(len(rules))

        # Creating our bar plot
        plt.bar(y_positions, lift)
        plt.xticks(y_positions, rules)
        plt.ylabel("Lift")
        plt.title("Lift of each rule")
        plt.show()
    else:
        mb.showerror("File Error", "Sorry,You need to enter a .csv file")


def button_go_callback():
    try:
        support_threshold = float(entry_support.get())
        confidence_threshold = float(entry_confidence.get())
        input_file = entry_filename.get()
        if os.path.splitext(input_file)[1] == ".csv":
            text.delete(1.0, END)
            data = MBA_Main.read_data(input_file)
            final_results = ['{} => {}  \t|\t Support = {:.2f}, Confidence = {:.2f}, Lift = {:2f}'.
                                 format(item_set, item, MBA_Main.support_frequency(data[1:],item_set.union({item})),
                                 MBA_Main.confidence(data[1:], item_set, {item}), MBA_Main.lift(data[1:], item_set, {item}))
                                 for item_set, item in MBA_Main.apriori(data[1:], support_threshold, confidence_threshold)]

            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            text.insert(INSERT, "Current Date & Time: ", [0], date_time)
            text.insert(INSERT, "\n\n")

            for result in final_results:
                text.insert(INSERT, str(result)[3:-2])
                text.insert(INSERT, "\n\n")

            statusText.set("Rules Generated Successfully")
        else:
            mb.showerror("File Error", "Sorry,You need to enter a .csv file")
    except:
        mb.showerror("Input Error", "Sorry, No file have been added!")


def button_browse_callback():
    filename = filedialog.askopenfilename()
    entry_filename.delete(0, END)
    entry_filename.insert(0, filename)


def button_viewinput_callback():
    input_file = entry_filename.get()
    text.delete(1.0, END)
    with open(input_file, 'r') as file_reader:
        for line in file_reader:
            text.insert(INSERT, line)
            text.insert(INSERT, "\n")
    statusText.set(str(os.path.splitext(input_file)) + " Displayed Successfully" )


"""
 ******** Program GUI ******** 
"""

root = Tk()
root.title('Prediction Model using MBA')
frame = Frame(root)
frame.pack()

statusText = StringVar(root)
statusText.set(
    "Click Browse and select file, then select Confidence and Support Thresholds, " "\nClick on View Input to view Input Transactions or Click on Go")

top_frame = Frame(frame)

label = Label(top_frame, text="CSV file: ", padx=5, pady=2)
label.pack(side=LEFT)
entry_filename = Entry(top_frame, bd=5, width=100)
entry_filename.pack(side=LEFT)
La = Label(top_frame, padx=3, pady=5, text=" ")
La.pack(side=LEFT)
button_browse = Button(top_frame, text="Browse", command=button_browse_callback)
button_browse.pack(side=RIGHT)

top_frame.pack()
separator = Frame(frame, height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=5)
"""  ###############################################   """

mid_frame = Frame(frame)

Confidence_label = Label(mid_frame, padx=5, pady=5, text="Confidence Threshold :")
entry_confidence = Spinbox(mid_frame, width=5, from_=0.1, to=1, format="%.2f", increment=0.05, bd=5)
Confidence_label.pack(side=LEFT)
entry_confidence.pack(side=LEFT)

Support_label = Label(mid_frame, padx=5, pady=5, text="Support Threshold :")
entry_support = Spinbox(mid_frame, width=5, from_=0.1, to=1, format="%.2f", increment=0.05, bd=5)
Support_label.pack(side=LEFT)
entry_support.pack(side=LEFT)

VI_label = Label(mid_frame, padx=10, pady=10, text=" ")
VI_label.pack(side=LEFT)

button_viewinput = Button(mid_frame, text="View Input", command=button_viewinput_callback)
button_viewinput.pack(side=LEFT)

Go_label = Label(mid_frame, padx=5, pady=5, text=" ")
Go_label.pack(side=LEFT)

button_go = Button(mid_frame, text="Go", command=button_go_callback)
button_go.pack(side=RIGHT)

plot_label = Label(mid_frame, padx=5, pady=5)
plot_label.pack(side=LEFT)

button_plot = Button(mid_frame, text="Plot Results", command=button_plot_callback)
button_plot.pack(side=LEFT)

mid_frame.pack()
separator = Frame(mid_frame, height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=5)

separator = Frame(frame, height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=5)

# Creating a Frame
txt_frm = Frame(frame, width=1080, height=920)
txt_frm.pack(fill="both", expand=True)
txt_frm.grid_propagate(False)
txt_frm.grid_rowconfigure(0, weight=1)
txt_frm.grid_columnconfigure(0, weight=1)
text = Text(txt_frm, borderwidth=3)
text.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

# Scroll bars
scrollbary = Scrollbar(txt_frm, command=text.yview)
scrollbary.grid(row=0, column=1, sticky='w')
text['yscrollcommand'] = scrollbary.set
scrollbary.pack(side=RIGHT, fill=Y)
text.pack()

separator = Frame(frame, height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=5)

message = Label(frame, textvariable=statusText)
message.pack()



