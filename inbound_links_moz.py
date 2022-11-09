import numpy as np
import pandas as pd
from urllib.request import urlopen
import os
from mozscape import Mozscape

Access_ID = "<YOUR_ACCESS_ID_HERE>"
Secret_key = "<YOUR_SECRET_KEY_HERE>"
client = Mozscape(Access_ID, Secret_key)

#fill missing values with np.nan
def pad_dict_list(dict_list, padel):
    lmax = 0
    for lname in dict_list.keys():
        lmax = max(lmax, len(dict_list[lname]))
    for lname in dict_list.keys():
        ll = len(dict_list[lname])
        if  ll < lmax:
            dict_list[lname] += [padel] * (lmax - ll)
    return dict_list


while True:
        fileName = str(input("Write the name of the .xlsx file (should be in the same directory): "))
        if os.path.isfile(fileName):
            data = pd.read_excel(fileName)
            break
        else:
            print("Wrong file name, try again!\n")
        
linksLimit = int(input("Write the links limit per .xlsx file you want to retrieve from the api: "))
first_column = data.iloc[0:, 0]
all_links_clean_serie = []

#eliminate non strings
for link in first_column:
    if not isinstance(link, float) and not isinstance(link, int):
        all_links_clean_serie.append(link)


#for i in range(10): to test it with less links
for i in range(len(all_links_clean_serie)):
    dictList = client.links(all_links_clean_serie[i], limit=linksLimit)
    listToXlsx = []
    myexceldict = {"URLs":[], f"Inbound links for {all_links_clean_serie[i]}": []}
    
    for h in range(len(dictList)):
        listToXlsx.append(dictList[h]["uu"])
    
    
    myexceldict["URLs"] = listToXlsx
    myexceldictPadded = pad_dict_list(myexceldict, np.nan)
    df = pd.DataFrame(myexceldictPadded)
    df.to_excel(f"Inbound {i}.xlsx")

print("All .xlsx files have been created!")