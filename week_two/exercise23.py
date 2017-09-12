#the given list
names = ['John', 'Tom', 'Snappy', 'John', 'Kitty', 'Jessie','John', 'Kitty', 'Chester', 'John', 'Doe', 'Tom', 'Stefano', 'Jenny', 'Anna', 'charles']

the_dictonary = {} #initilize a dictionary
for name in names:
    #add to, and updated the dictonary
    if name not in the_dictonary:
        the_dictonary[name] = 1
    else:
        the_dictonary[name] += 1      

#lets also sort the dictonary according to value.. reverse prints the highest number first, the anyomus function
#selects the second element which is the values in the the_dictonary.items()..
for key, value in sorted(the_dictonary.items(), key=lambda x: x[1], reverse = True):
    print "{} appears: {}".format(key, value)
    
for key, value in the_dictonary.items():
    if value == 1:
        del the_dictonary[key] #delete from the dictonary according to the key value
print
for key, value in sorted(the_dictonary.items(), key=lambda x: x[1], reverse = True):
    print "{} appears: {}".format(key, value)