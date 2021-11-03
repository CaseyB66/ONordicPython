"""
PayPal Parse

10/21//2021
by Matt Gnagey

This code imports a csv file generated from PayPal,
separates the payments out under the following categories,
and multiplies them by the current Ogden Nordic Prices. 

"""
import pandas as pd
#### SET OGDEN NORDIC PRICES HERE #####
skiadult = 100
skifamily = 200
skiaddchild= 25
skiteen= 40

snowshoeadult = 50
snowshoefamily = 100
snowshoeaddchild= 5

fatbikeadult = 80
fatbikefamily = 160
fatbikeaddchild = 15
fatbiketeen = 35

path = r'D:/Users/Ken Beck/Documents/ONordic/Python/'
# path =r'D:\Users\mattgnagey\Box\Committee\Ogden Nordic\'

df = pd.read_csv("{}{}".format(path,'paypal10192021.csv'))


# Clean up the Names of the Columns
data = pd.DataFrame(df, columns = ['Item Title', 'Gross', 'Fee', 'Net', 'Shipping and Handling Amount', 'Quantity'])
data = data.rename(columns={"Item Title": "item", "Shipping and Handling Amount": "shipping"})
data = data.rename(str.lower, axis='columns')


# How many rows the dataset
data['item'].count()

# Find Fat Bikers
data['bike'] = 0
data.loc[data['item'].str.find('Fat Bike')>1 , 'bike' ] =1

# Find Skiers
data['ski'] = 0
data.loc[data['item'].str.find('Ski')>1 , 'ski' ] =1
     
# Find Snowshoers
data['snowshoe'] = 0
data.loc[data['item'].str.find('Snowshoe')>1 , 'snowshoe' ] =1
     
# Find Individual or Family
data['individual'] = 0
data.loc[data['item'].str.find('Individual')>1 , 'individual' ] =1
data['family'] = 0
data.loc[data['item'].str.find('Family (Immediate)')>1 , 'family' ] =1
data['addchild'] = 0
data.loc[data['item'].str.find('Additional Child (Family Only-Select 0 if N/A): 1')>1 , 'addchild' ] =1

# Correct if multiple quantities that are different activities
data['multiple'] = 0
data['temp'] = data['item'].str.count('Primary Activity')
data.loc[data['temp'] > 1, 'multiple'] =1

# Fix the quantity
data.loc[data['bike']+ data['ski'] + data['snowshoe'] >1 , 'quantity' ] =1

# Append in the multiple observation
##############NEED TO FIX MULTIPLES #############
addrow = data['multiple']==1
dataadd = data[addrow]
data = data.append(dataadd)

# Correct for those needing refunds
data['refund'] = 0
data.loc[data['gross']<0, 'refund'] = 1


#### Checking to see if the code works
data['comparegross']  = 0
data['comparegross'] = data['quantity'] *(data['individual']*data['bike']*fatbikeadult + \
data['family']*data['bike']*fatbikefamily + \
data['addchild']*data['bike']*fatbikeaddchild + \
data['individual']*data['ski']*skiadult + \
data['family']*data['ski']*skifamily + \
data['addchild']*data['ski']*skiaddchild + \
data['individual']*data['snowshoe']*snowshoeadult + \
data['family']*data['snowshoe']*snowshoefamily + \
data['addchild']*data['snowshoe']*snowshoeaddchild) + \
data['shipping']

data['check'] = data['comparegross'] - data['gross']

data['type'] = "Adult"
data.loc[data['family']>0, 'type'] = "Family"
data.loc[data['addchild']>0, 'type'] = "Family with an added Child"


data['activity'] = "Ski"
data.loc[data['bike']>0, 'activity'] = "Bike"
data.loc[data['snowshoe']>0, 'activity'] = "Snowshoe"

data['count'] = 1
data.loc[data['refund']==1, 'count'] = -1





##### Creates the summary for each product based on the Chart of Accounts
data['product'] = 'Adult Bike Season Pass'
data.loc[(data['ski']>0) & (data['type']=='Adult'), 'product'] = "Adult Ski Season Pass"
data.loc[(data['snowshoe']>0) & (data['type']=='Adult'), 'product'] = "Adult Snowshoe Season Pass"
data.loc[(data['bike']>0) & (data['type']=='Family'), 'product'] = "Family Bike Season Pass"
data.loc[(data['ski']>0) & (data['type']=='Family'), 'product'] = "Family Ski Season Pass"
data.loc[(data['snowshoe']>0) & (data['type']=='Family'), 'product'] = "Family Snowshoe Season Pass"




data[['type', 'gross']].groupby('type').count()
data[['type', 'gross']].groupby('type').sum()
data.groupby(["type", 'activity'])['gross'].count()
data.groupby(["type", 'activity'])['gross'].sum()



s = data.groupby(["type", 'activity']).agg({'gross':['count', 'sum']})
s.to_csv (r'D:\Users\mattgnagey\Box\Committee\Ogden Nordic\Paypal\test.csv', header=True)






















