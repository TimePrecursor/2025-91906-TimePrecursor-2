import random
import math
import numpy


def sqrt1(n, value):
    return value ** (1 / n)

def sqrt_str(powersign, value):
    return f"{powersign}{value}"

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

lvl3_signs = [["add","subtract"],["times","divide"],["sqrt1","power"]]

def ri_args(min, max):
    return random.randint(min,max)

def ri_10():
    return random.randint(0, 10)

def print_question(*args,**kwargs):
    list1 = []

    for i, sign in enumerate(kwargs):
        list1.insert(int(i*2),str(kwargs[sign[0]]))
    for i, val in enumerate(args):
        if val[0] == "sqrt1":
            pass
        list1.insert(i+i,str(f"{val[0]}"))

    print("What is", *list1)


def level_all():
    signs_dict = {}

    def rand_sign():
        index = lvl3_signs[difficulty - 1][ri_args(0, 1)]
        sign2 = str(random.choice(lvl_signs[difficulty][index]))
        sign_val = random.choice(lvl_signs[difficulty][index])
        # if diff == 3:
        #     pass
        return sign2,sign_val

    difficulty = numpy.clip(int(round(float(input("Choose your difficulty: ")))),0,3)
    print(f"Chosen difficulty is {difficulty}\n")


    # Make random questions:
    if difficulty == 3:
        powersign = power1(ri_args(0,3),ri_10())[1]
        sqrt = sqrt_str(powersign=(ri_args(1,3)), value=(ri_args(0,100)))
        sign1 = random.choice([powersign,sqrt])
        # print(sign1, "sign1")


    # input(f"What is {ri_10()} {rand_sign()} {ri_10()}")
    print_question(ri_10(), ri_10(), ri_10(), ri_10(), q=rand_sign(), w=rand_sign(), e=rand_sign())


level_all()