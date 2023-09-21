import math

print("Investment- to calculate the amount of interest you'll earn on your investment")
print("Bond      - to calculaue the amount you'll have to pay on a home loan")

#Get the user to choose between Investment and Bond. '1' is investment and '2' is Bond
choice= 0
choice= int(input("Enter '1' for investment or '2' for bond to proceed"))
if choice!= 1 and choice!= 2:
    print("Invalid Input")

#If user inputs '1', "investment" is selected and they proceed to calculate their interest
if choice== 1:
    print("Investment selected")
    p= float(input("How much money are you depositing:"))
    r= float(input("Enter your interest rate as a number only, No signs or symbols must be entered:"))
    t= float(input("Enter the number of years you plan on investing:")) 
    interest= int(input("Enter '1' for simple interest or enter '2' for compound interest:"))
    
#User chooses between simple interest and compound interest
    if interest== 1:
        a= p*(1 + r/100*t)
        print (a)
    elif interest == 2:
        a=p*math.pow((1+r/100),t)
        print(a)

#user chooses "Bond" instead of "investment" and calculates repayment
elif choice== 2:
    print("Bond selected")
    p= float(input("Enter the value of the house:"))
    i= float(input("Enter your yearly interest rate"))
    n= float(input("Enter the number of months over which the bond will be repaid:"))

    repayment= (i/100/12*p)/(1-(1+i/100/12)**(-n))
    print(repayment)
