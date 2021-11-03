"""
PayPal Parse

10/21//2021
by Matt Gnagey

This code imports a csv file generated from PayPal,
separates the payments out under the following categories,
and multiplies them by the current Ogden Nordic Prices. 

"""
import pandas as pd

path = r'D:/Users/Ken Beck/Documents/ONordic/Python/'
# path =r'D:\Users\mattgnagey\Box\Committee\Ogden Nordic\'

ppraw = pd.read_csv("{}{}".format(path,'paypal10192021.csv'))
wixraw = pd.read_csv("{}{}".format(path,'02Nov21 Wix Orders.csv'))


# Clean up the Names of the Columns
ppdata = pd.DataFrame(ppraw, columns = ['Date','Time','From Email Address','Item Title', 'Gross', 'Fee', 'Net', 'Shipping and Handling Amount', 'Quantity'])
ppdata = ppdata.rename(columns={"Item Title": "item", "Shipping and Handling Amount": "shipping","From Email Address":"FromEmail"})
ppdata = ppdata.rename(str.lower, axis='columns')


# How many rows the dataset
pptot=ppdata['item'].count()

print("PayPal records {}".format(pptot))

wixdata = pd.DataFrame(wixraw, columns = ['Date','Time','Contact email','Total order quantity', 'Item', 'Variant','Qty', 'Qty refunded', 'Price', 'Payment status', 'Total', 'Refunded','Total after refund'])
wixdata = wixdata.rename(columns={"Total order quantity": "TotalQty", "Qty refunded": "QtyRfnd","Contact email":"FromEmail","Payment status":"PayStatus","Total after refund":"Net"})
wixdata = wixdata.rename(str.lower, axis='columns')

# How many rows the dataset
wixtot=wixdata['item'].count()

print("Wix records {}".format(wixtot))

# How many unique items in the Wix Data?
wixItems = wixdata["item"].unique()
print("Unique Wix Items: {}".format(wixItems))

wixVarnt = wixdata["variant"].unique()
print("Unique Wix Variants: {}".format(wixVarnt))

# Get prices for these unique options:
wixPrices = []
for w in range(wixtot):
  for ii in wixItems:
    for vv in wixVarnt:
      try:
        if ((pd.isna(vv) and pd.isna(wixdata["variant"][w])) or 
          (wixdata["item"][w].find(ii)>-1) and (wixdata["variant"][w].find(vv)>-1)):
          descr="{}, {}".format(ii,vv)
          descr.replace('|', ',')
          ntry={"descr":descr,"price":wixdata["price"][w]}
          if not any(descr == d["descr"] for d in wixPrices):
            wixPrices.append(ntry)
      except TypeError:
        print("TE ii {}/ vv {}".format(ii,vv))
      except AttributeError:
        print("AE ii {}/ vv {}".format(ii,vv))
 
print("Found {} prices".format(len(wixPrices)))

# Now see if we have matches in the PyPl data:
for pp in ppdata['item']:
  if not pd.isna(pp):
    for wp in wixPrices:
      print("pp: {} \n descr: {}".format(pp,wp['descr']))
      if (pp.find(wp["descr"])>-1):
        print("We found a price {} for item {}".format(pp["price"],pp['item']))                             
   