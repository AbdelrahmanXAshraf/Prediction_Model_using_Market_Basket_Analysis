import MBA_GUI
from tabulate import tabulate
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib
# plt.style.use('ggplot')
from matplotlib.pyplot import figure


"""
# matplotlib inline
matplotlib.rcParams['figure.figsize'] = (12,8)

pd.options.mode.chained_assignment = None


# read the data
df = pd.read_csv('./Datasets/sample_input.csv')

# shape and data types of the data
# print(df)
# print(df.dtypes)

# if it's a larger dataset and the visualization takes too long can do this.
# % of missing.
for col in df.columns:
    pct_missing = np.mean(df[col].isnull())
    print('{} - {}%'.format(col, round(pct_missing*100)))
"""

# This Method reads the data set File
def read_data(file_name):
    result = list()
    with open(file_name, 'r') as file_reader:
        for line in file_reader:
            order_set = set(line.strip().split(','))
            result.append(order_set)
    return result


# This method counts how many time does an element appears the orders list
def support_count(orders, item_set):  # 2 parameters (orders, item_set == each element per order)
    count = 0
    for order in orders:  # looping over orders
        if item_set.issubset(order):  # issubset checks whether at least on element of item_set in the orders set
            count += 1  # as long as the element exist it will increment the counter var by 1
        else:
            pass  # else statement will do nothing
    return count


# This method calculates the actual support for a certain item set (A.K.A. basket)
def support_frequency(orders, item_set):
    N = len(orders)  # assigning the length of the orders to N
    return support_count(orders, item_set) / float(N)  # Support =  item_set1 + item_set2 / total(N)


def confidence(orders, left, right):
    left_count = support_count(orders, left)
    right = right.union(left)
    right_count = support_count(orders, right)
    result = right_count / left_count
    return result


# This Method contains the Main Algorithm (Apriori)
def apriori(orders, support_threshold, confidence_threshold):
    """ Accepts a list of item sets (i.e. orders) and returns a list of
        association rules matching support and confidence thresholds. """
    candidate_items = set()   # creating a set() that holds the candidate items

    for items in orders:  # Looping over items in the orders files
        candidate_items = candidate_items.union(items)  # Merging the items in the orders file with empty "Candidate set"

    def apriori_next(item_set=set()):  # this function takes an empty set as a parameter
        """ Accepts a single item set and returns list of all association rules
            containing item_set that match support and confidence thresholds."""
        result = []  # Initializing an empty list called "result"

        # Recursion base case.
        # a condition to check whether the length of set of the item_set == len of the candidate_items set
        if len(item_set) == len(candidate_items):
            return result  # if true it will return the result List

        elif not item_set:
            for item in candidate_items:
                item_set = {item}
                if support_frequency(orders, item_set) >= support_threshold:
                    result.extend(apriori_next(item_set))
                else:
                    pass
        # Else statement if neither of the above statements are satisfied
        # Given that an item set where all candidate items meeting threshold
        else:
            # looping over items in the set of the (candidate_items - item_set)
            for item in candidate_items.difference(item_set):
                if support_frequency(orders, item_set.union({item})) >= support_threshold:
                    if confidence(orders, item_set, {item}) >= confidence_threshold:
                        result.append((item_set, item))
                        result.extend(apriori_next(item_set.union({item})))
                    else:
                        pass
                else:
                    pass

        return [rule for rule in result if rule]

    return apriori_next()


"""
def item_freq_graph():
    bar_width = 0.20
    # support_threshold = float(entry_support.get())
    input_file = entry_filename.get()
    text.delete(1.0, END)
    data = read_data(input_file)
    plt.bar(len(support_frequency(data[1:])) - bar_width / 2, support_frequency(data[1:]), bar_width)
    plt.show()
"""

"""
def button_go_callback():
    support_threshold = float(entry_support.get())
    confidence_threshold = float(entry_confidence.get())
    input_file = entry_filename.get()
    text.delete(1.0, END)
    statusText.set("Rules Generated Successfully")
    data = read_data(input_file)
    final_results = ["{} => {}  \t|\t Support = {:0.2f}, Confidence = {:0.2f}".format(item_set, item,
                     support_frequency(data[1:], item_set.union({item})), confidence(data[1:], item_set, {item}))
                     for item_set, item in apriori(data[1:], support_threshold, confidence_threshold)]

    date_time = now.strftime("%d/%m/%Y %H:%M:%S")
    text.insert(INSERT, "Current Date & Time: ", [0], date_time)
    text.insert(INSERT, "\n\n")
    for result in final_results:
        text.insert(INSERT, str(result)[3:-2])
        text.insert(INSERT, "\n\n")
       # plt.scatter(support_frequency(data[1:], item_set.union({item})), confidence(data[1:], item_set, {item})), alpha=0.5, marker="*")



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
    statusText.set(" Transactions Displayed Successfully")

"""


if __name__ == '__main__':
    MBA_GUI.mainloop()

