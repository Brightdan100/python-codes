#Assignment 1
def internship_date(income, travel_cost, rent, other_expenses):
    numberOfDays = (income - rent - other_expenses) // (travel_cost * 2)
    if numberOfDays < 0:
        return 0
    elif numberOfDays > 30:
        return 30
    else:
        return numberOfDays

#Assignment 2
def calculate_payment(order):
    return order.count("B") * 2.00 + order.count("W") * 2.50 + order.count("S") * 1.50

#Assignment 3
def maximum_by(dataFrame, columnName):
    import pandas as pd
    return dataFrame.loc[dataFrame[columnName].idxmax()]
    import math
    normSum = 0
    for component in vector:
        normSum += pow(component, 2)
    return math.sqrt(normSum)

#Assignment 4
def KL(p, q):
    import math
    if int(sum(p)) != 1:
        p = p / sum(p)
    if int(sum(q)) != 1:
        q = q / sum(q)
    totalSum = 0
    for i in range(len(p)):
        totalSum += p[i] * math.log((p[i]/ float(q[i])), 2)
    return totalSum

#Assignment 5
def diagonals(array):
    differenceArray = [i for i in range(-max(len(array[0]), len(array)), max(len(array[0]), len(array)))]
    diagonalArray = []
    for count in range(2 * max(len(array[0]), len(array))):
        temporaryArray = []
        for i in range(len(array)):
            for j in range(len(array[0])):
                if (i - j) == differenceArray[count]:
                    temporaryArray += [array[i][j]]
        if temporaryArray != []:
            diagonalArray += [temporaryArray]
    return diagonalArray