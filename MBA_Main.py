"""Created By: Abdelrahman Ashraf 152761"""
import MBA_GUI
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import association_rules
import pandas as pd


# This Method reads the data set File
def read_data(file_name):
    result = list()
    with open(file_name, 'r') as file_reader:
        for line in file_reader:
            order_set = set(line.strip().split(','))
            result.append(order_set)
    return result


def fp_growth_algorithm():
    TE = TransactionEncoder()
    TE_Array = TE.fit(read_data('groceries.csv')).transform(read_data('groceries.csv'))
    DF = pd.DataFrame(TE_Array, columns=TE.columns_)
    frequent_itemsets_fp = fpgrowth(DF, min_support=0.01, use_colnames=True)
    rules_fp = association_rules(frequent_itemsets_fp, metric="confidence", min_threshold=0.35)
    str_DF = rules_fp.to_string()
    File = open("Result_File.txt", "w")
    File.write(str_DF)
    File.close()


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
    """
    confidence{B->A} = support{A,B} / support{B}
    """
    left_count = support_count(orders, left)
    right = right.union(left)
    right_count = support_count(orders, right)
    result = right_count / left_count
    return result


def lift(orders, left, right):
    """
    Lift: lift{A,B} = lift{B,A} = support{A,B} / (support{A} * support{B})

    * lift = 1 implies no relationship between A and B.
    (ie: A and B occur together only by chance)

    * lift > 1 implies that there is a positive relationship between A and B.
    (ie:  A and B occur together more often than random)

    * lift < 1 implies that there is a negative relationship between A and B.
    (ie:  A and B occur together less often than random)
    """
    left_count = support_count(orders, left)
    right_count = support_count(orders, right)
    right = right.union(left)
    union_count = support_count(orders, right)
    lift_result = union_count / (left_count * right_count)
    return lift_result


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
            # looping over items in the set of the (candidate_items - item_set) -> elements that are in set "candidate_items" but not "item_set"
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


if __name__ == '__main__':
    MBA_GUI.mainloop()


