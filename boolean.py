#lets talk logic
#goal: output truth table and simplified version of boolean formula
#secondary goal: program should under no circumstances return an error
#these steps are wrong, too lazy to update
#user inputs boolean formula IE (AB+C'D+C(A+D)')
#step 1: make sure all letters are capital in input (and sanitize input)
#step 2: put equasion in standard form IE: AB+C'D+CA
#   2.a demorgans theorm
#   2.b distribute
#step 3: truth table
#step n-1: ???
#step n: profit

def get_input():
    print("input equation, use + for or, * or (AB) for and, A' for not.")
    equation=input()
    return equation


#takes the input and does 3 main things.
#1. ensure no illegal characters are included
#2. ensure parenthesis are closed. 
#   note: does not actually ensure the parenthesis placement makes sense, just that there are the same number of opening and closing ones
#3. capitalize all letters
def sanitize(equation):
    new_e=''
    equation=equation.replace(' ','')
    lpars=0
    rpars=0

    for i in range(len(equation)):

        a=equation[i]
        if(a.isalpha() or a=='+' or a =='*'):
            continue
        elif(a=='('):
            
            lpars+=1
            #print(a,'l',lpars)
            continue
        elif(a==')'):
            rpars+=1
            #print(a,'r',rpars)
            continue
        elif(a=="'"):
            if(equation[i-1].isalpha() or equation[i-1]=='(' or equation[i-1]==')'):
                continue
            else:
                print('Error: NOTs must be placed after a variable for variables in ()')
                return 0

        else:
            print('Error: unknown value in input')
            print('"{}" is not allowed'.format(a))
            return(0)
    if(lpars != rpars):
        #print(lpars, rpars)
        print('Error: parenthesis not closed')
        return(0)
    i=0

    for i in range(len(equation)):
        try:
            new_e+= equation[i].upper()
        except:
            new_e+=equation[i]
        continue

    return(new_e)

#standard form logic
#step 1: put each 

#some test cases
# abcd+abc+A(ab+d)'
# abc+(ab+cd)(ad+rf+gd)
#(ab+de)(ab+d(ae+ed))
#(ab+d(ae+ed))(ab+de)+abc
#abc'+(ab+d(ae+ed)')(ab+de)+abc+A(ab+d)'
#(ab(a+b+c(a+ed))(d+a+b))
#(ab+cd)(ab+cd)(ab+cd)(ab+cd)
#(ab(ab+de)d')(ab(ab+de)d')(ab(ab+de)d')
#(ab+ac)'
#(a'b+a'c)'
#(ab'+c'+ac)'
#(ab'+c+ac)'
#(a+b+c'+d'+ab+a'c'+c)'

#its a bunch of nasty if statements, there is a much better way to do it, but thats a problem for future me
#the if statements don't work, fix it #wait maybe they do
#does de morgans theorm
#has issue with giving too many parenthesis, but my code seems to be resilient enough to handle it, will fix later though
def de_morgan(part):
    print(part)
    new_str='('
    for i in range(len(part)):
        #a try catch for just in case, not sure how somebody would make it go off though
        try:
            if(part[i].isalpha()):
                if(part[i+1]=="'"):
                    if(part[i+2]=="+"):
                        if(part[i-1]=="+" or part[i-1]=="("):
                            new_str=new_str+part[i]
                        else:
                            new_str=new_str+part[i]+')'
                    elif(part[i+2]==")"):
                        new_str=new_str+part[i]+')'
                        break
                    else:
                        if(i-1==0):
                            new_str=new_str+'('
                        new_str=new_str+part[i]+'+'
                elif(part[i+1].isalpha()):
                    if(i-1==0):
                        new_str=new_str+'('
                    if(part[i-1]=='+'):
                        new_str=new_str+'('+part[i]+"'"+'+'
                    else:
                        new_str=new_str+part[i]+"'"+'+'
                elif(part[i+1]=='+'):
                    if(part[i-1]=="+" or part[i-1]=="("):
                            new_str=new_str+part[i]+"'"
                    else:
                            new_str=new_str+part[i]+"'"+')'

                elif(part[i+1]==')'):
                    new_str=new_str+part[i]+"'"+')'
            if(part[i]=='+'):
                if(part[i+2]!='+' and part[i+3]!='+' and part[i+2]!=')' and part[i+3]!=')'):
                    new_str=new_str+'('
                         
        except:
            print('whoops! we ran into an error while doing de morgans theorm, please check input')
            quit()
    print(new_str)
    return(new_str)


#two different distrutes for slightly different things
#distribute_1 is for A(B+C) or (B+C)A
#distribute_2 is for (B+C)(A+D)

#more test cases
#(A+B)ABC'
#A(A+B)
#ABCD(A'+B)
#(c+D)A'
#(a+BCD+D)ACD'
def distribute_1(part,mult):
    #part is **(a+b) (** is unused part)
    #mult is CD(**) (** is unused part)
    #print(part, mult)
    new_str=''
    for i in range(len(part)):
        if(part[i]=='+' or part[i]==')'):
           new_str+=mult+part[i]
        else:
            new_str+=part[i]
    #new_str=new_str.replace('(','')
    #new_str=new_str.replace(')','')
    return(new_str)

    
#for distributing (x+y)(x+y)
#example of how it works:
#(x+y)(x+y)
#(x+y)x + (x+y)y
# uses distribute_1, no need to write same code twice

def distribute_2(part,part2):
    #print(part,part2)
    part2=part2.replace('(','')
    part2=part2.replace(')','')
    arr=part2.split('+')
    newstr='('
    for i in arr:
        x= distribute_1(part,i)
        x=x.replace('(','')
        x=x.replace(')','')
        if(i==arr[-1]):
            newstr+=(x+')')
        else:
            newstr+=(x+'+')
    
    return(newstr)


def remove_unneeded_pars(part, left, right):
    if((part[left-1]=='+' or part[left-1]=='(')and left!=0):
        part=part.replace(part[left:right+1],part[left+1:right])
        return part
    else:
        return part
            

        
#the one true test case
#

def standard_form(equation):
    #note: split('+') will not work for this issue without some... help
    equation_array=[]
    final_equation_array=[]
    lpars=0
    rpars=0
    j=0
    #this for loop is to put the parts of an equation in a list
    #parts are seperated by '+' and any part with () is put together for further distributing or other things
    for i in range(len(equation)):
        letter=equation[i]
        #right and left parenthesis
        if(letter=='('):
            lpars+=1
        elif(letter ==')'):
            rpars+=1
        if(letter=='+' and rpars==lpars):
            equation_array.append(equation[j:i])
            j=i+1
    equation_array.append(equation[j:i+1])
    #debug print statement, comment out/delete on final release
    print(equation_array)
    i=0
    l=0
    run=0
    #this is for figuring out if code needs distributing or demorgan-ing
    for part in equation_array:
        if ('(' in part or ')' in part):

            #what does this while and for statement do, well let me tell ya
            #as i said earlier its for checking if stuff needs distributing and demorganing
            #when ever something is changed, the length of the string is also changed, so i break after every time i distribute
            # I leave the for loop and restart the while loop which rechecks the length of the string
            # Then if nothing happens in the code for long enough, I leave the while loop
            keep_going=True
            while(keep_going):
                i=0 #not sure if this is necessary, will do proper testing later
                len_part=len(part)
                for i in range(len_part):
                    if(part[i]=='('):
                        l=i
                    elif(part[i] ==')'):
                        #for de morganing
                        if(i+1<len_part):
                            if(part[i+1]=="'"):
                                part=part.replace(part[l:i+2],de_morgan(part[l:i+2]),1)
                                #print(part)
                                break
                            #for distributing
                            elif(part[i+1].isalpha()):
                                m=i+2

                                try:
                                    while(part[m].isalpha() or part[m]=="'"):
                                        m+=1
                                except:
                                    part=part.replace(part[l:m],distribute_1(part[l:i+1],part[i+1:m]),1)
                                    #print(part)
                                    break

                                part=part.replace(part[l:m],distribute_1(part[l:i+1],part[i+1:m]),1)
                                #print(part)
                                break
                            
                        #for distributing
                        if(part[l-1].isalpha() or part[l-1]=="'"):
                            m=l-1
                            

                            while((part[m].isalpha() or part[m]=="'") and m>=0):
                                m-=1
                            m+=1
                                
                            part=part.replace(part[m:i+1],distribute_1(part[l:i+1],part[m:l]),1)

                            #print(part)
                            break
                            #for distributing
                        elif(part[l-1]==')'and (l-1)>=0):
                            
                            m=l-1
                            while(part[m]!='(' and m>=0):
                                m-=1
                            m=0 if m<0 else m
                            
                            part=part.replace(part[m:i+1],distribute_2(part[l:i+1],part[m:l]),1)
                            #print(part)
                            break
                        elif((i+1<len_part) and (part[i+1]==')' or part[i+1]=='+')):
                                part=remove_unneeded_pars(part, l, i)
                                break                  

                if(run>3):
                    keep_going=False
                run+=1
                        
            part=part.replace('(','')
            part=part.replace(')','')
            part=part.split('+')
            #final_equation_array.append('filler')
            final_equation_array[-1:-1]=part
            
                                    
        else:
            final_equation_array.append(part)
            continue
    return(final_equation_array)

#This function exists to hopefully make future steps easier
#current form of array is Max terms, basically i want to:
# input: [A'BCD+AB'CD]
# output: [ [A',B,C,d],[A,B',C,D]]
#I believe this will help with future steps, if not ill just delete it
def reformat_for_future_steps(equation_array):
    new_equation_array=[]
    temp_arr=[]
    for step in equation_array:
        for i in  range(len(step)):
            if(step[i].isalpha()):
                try:
                    if(step[i+1]=="'"):
                        temp_arr.append(step[i]+"'")
                    else:
                        temp_arr.append(step[i])
                except:
                    temp_arr.append(step[i])
            else:
                continue
        temp_arr = list(dict.fromkeys(temp_arr))
        temp_arr.sort()
        new_equation_array.append(temp_arr)
        temp_arr=[]
    return(new_equation_array)

#removes duplicate items from list
def remove_dupes(a):
    b=[]
    [b.append(item) for item in a if item not in b]
    b.sort()
    return b

#removes any items in list b from list a
def list_diff(inputa,inputb):

    a=[]
    b=[]
    final =[]
    for item in inputa:
        a.append(set(item))
    
    for item in inputb:
        b.append(set(item))
    
    [a.remove(item) for item in b if item in a]
  
    for item in a:
        final.append(list(item))

    return final

#takes difference; example:
# ABC+ABC' = AB
#or AB+ABC = AB
#returns either original list or simplified
def diff(a):
    if(a[0]==a[1]):
        return a
    aset=set(a[0])

    bset=set(a[1])

    c1=list(aset.difference(bset))
    c2=list(bset.difference(aset))

    if(not c1 or not c2):
        return [list(aset.intersection(bset))]
    elif((c1[0][0]==c2[0][0])and len(c1)==1 and len(c2)==1):
        return [list(aset.intersection(bset))]
    else:
        return a

#I am using the tabular method for logic optimization. it is extremely inefficient but it works and computers are fast.
#difference
#steps:
#1 sort lists by size
#2. compare all lists that are the same size
    # a=b.difference(c)
#removes duplicate items from a list


def more_opt(nested_eqn):
    newlist=[]
    usedlist=[]
    for i in range(len(nested_eqn)):
        used = False
        for j in range(i,len(nested_eqn)):
            a=diff([nested_eqn[i],nested_eqn[j]])
            if len(a)==1: 
        
                used = True

                if(a[0]!=nested_eqn[i]):
                    usedlist.append(nested_eqn[i])
                if(a[0]!=nested_eqn[j]):
                    usedlist.append(nested_eqn[j])
                newlist.append(a[0])                
        if not used:  
            newlist.append(nested_eqn[i])
      
    #removes duplicate values from the list
    newlist= remove_dupes(newlist)
    usedlist= remove_dupes(usedlist)

    #takes difference between two lists
    newlist=list_diff(newlist,usedlist)

    return newlist


def logic_optimization2(nested_equation):
    nested_equation.sort(key=len, reverse=True)
    size =len(nested_equation[0])
    for i in range(size):
        nested_equation=more_opt(nested_equation)
        if(len(nested_equation)==1):break
    return nested_equation

    

    
#a test case or two
#ABCD+ABC'D+AB'CD+A'BC'D+A'B'C'D'+A'B'CD+ABC'D'+A'BCD'
equation=0
while(equation==0):
    equation=get_input()
    equation=sanitize(equation)
#print(equation)
equation=standard_form(equation)
#print(equation)
nested_equation=reformat_for_future_steps(equation)
#print(nested_equation)
final=logic_optimization2(nested_equation)
print(final)



