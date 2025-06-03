import random
import math
import numpy

difficulty = input("Choose your difficulty: ")
num_float = float(difficulty)  # Convert string to float
num_rounded = round(num_float)  # Round the float number
difficulty = int(num_rounded)    # Convert the rounded number to int

print(f"Chosen difficulty is {difficulty}")


def sqrt1(n, value):
    return value ** (1 / n)

def power1(n,value):
    superscripts = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
        '+': '⁺', '-': '⁻', '=': '⁼', '(': '⁽', ')': '⁾',
        'n': 'ⁿ', 'i': 'ⁱ'
    }
    return [(value ** n),superscripts[str(n)]]

# Name: [function, sign]
lvl_signs = {
    1: {'add': ["+","+"], 'subtract': ["-","-"]},
    2: {'times': ["*", "×"], 'divide': ["/", "÷"]},
    3: {'sqrt1': ["sqrt1","√"], 'power': ["^","power1"]}
    }
lvl_signs2 = ["add","subtract","times","divide","sqrt1","power"]
def getsign(x):
    y = lvl_signs[str(x)]
    print(y)

# getsign(difficulty)
# print(power1(2,10))

def question1(diff):
    questionlist = [
        random.randint(1,10),
        random.choice(lvl_signs[1]["add"]),
        random.randint(1, 10)
    ]
    print(f"What is {questionlist[0]}",questionlist[diff],f"{questionlist[2]}")

question1(difficulty)