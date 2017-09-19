# Import the modules
import sys
import random


# takes in integer i and returns binary representation, if n length, for the integer.
def intToBinary(i,n):
    l = [0] * n # creates a list of zeros of n length
    if i == 0: return l #If n = 0 then we just output the zero list
    index = 0
    # For each iteration we check if the integer is even or odd.
    #   if the integer is even then the program adds 1 to the list l
    #   if the integer is odd then the program adds 0 to the list l
    while i:
        # if modulus of 2 returns 1 then the number is odd
        if i % 2 == 1:
            l[index] = 1
        else:
            l[index] = 0
        i /= 2
        index += 1
    # Then reverse the list before returning
    return l[::-1]

# Creates all combination of list of n size that only contains 0 or 1 (binary list)
def createLists(n):
    for i in range (2**n):
        print intToBinary(i,n)

# Check if string is integer
def representsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

ans = True

while ans:
    question = raw_input("Please enter a integer: (press enter to quit) ")
    
    if(question == ""):
        break

    if representsInt(question):
        createLists(int(question))
    else:
        print "\nThis is not an integer \n"

