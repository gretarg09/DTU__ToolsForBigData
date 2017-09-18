#the given list
names = ['John', 'Tom', 'Snappy', 'John', 'Kitty', 'Jessie','John', 'Kitty', 'Chester', 'John', 'Doe', 'Tom', 'Stefano', 'Jenny', 'Anna', 'charles']

the_dictonary = {} #initilize a dictionary
for name in names:
    # add to, and updated the dictonary
    if name not in the_dictonary:
        the_dictonary[name] = 1 # Add new key to the dictionary
    else:
        the_dictonary[name] += 1  # Update the value for the give key

# Lets also sort the dictonary according to value.
#   Remember that the_dictionary.items() returns a list of (key, value) pairs
# reverse prints the highest number first, 
# the anyomus function selects the second element in each (key,value) pair and sorts 
#    according to that element
for key, value in sorted(the_dictonary.items(), key=lambda x: x[1], reverse = True):
    print "{} appears: {}".format(key, value)
    
# Delete all key value pairs where the name only appears once
for key, value in the_dictonary.items():
    if value == 1:
        del the_dictonary[key] #delete from the dictonary according to the key value
print
# Sort and print the updated list
for key, value in sorted(the_dictonary.items(), key=lambda x: x[1], reverse = True):
    print "{} appears: {}".format(key, value)