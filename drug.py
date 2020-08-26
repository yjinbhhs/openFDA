# -*- coding: utf-8 -*-
"""

openFDA Case Study for AstraZeneca Oncology Data Scientist Interview, Question 3
What drugs tend to be taken together? 
 
To find out other drugs associated with the specific drug a user inputs
Save the top related drugs into an excel spreadsheet and plot the bar plot for visualization

"""

import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from textwrap import wrap


#outcsv = sys.argv[1] 
#drug= sys.argv[2]
#iterations= sys.argv[3]
outcsv = 'drug.csv' # output file name
outfig = 'drug.png' #output figure name
drug= 'OXALIPLATIN'# user specificed drug
iterations= 6 # the number of related drugs  
 
query = 'https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name.exact:'+drug+'&count=patient.drug.openfda.generic_name.exact' # query openFDA API
record = requests.get(query).json() # read the json output from openFDA



i=0  
adj_drug=[] # variable initialization    
count=[]
       
for result in record.get('results', []):
   
    if i<int(iterations)+1:
       if('term' in str(result)):
          adj_drug.append(result['term'])   # read the name of each drug
          count.append(str(result['count'])) # read the number of occurrence of each drug
          i+=1
       else:
          continue
    else:
        break

# save to the excel spread sheet
data={'Related Drugs':adj_drug, 'Count':count}
del data['Related Drugs'][0] #remove the input drug
del data['Count'][0] 
df=pd.DataFrame(data)  
df.to_csv(outcsv, header=True, index=False, line_terminator='\n')

# plot the bar plot
objects=adj_drug
objects = [ '\n'.join(wrap(l, 16)) for l in objects ]
y_pos=np.arange(len(objects))
inst_num= [int(numeric_string) for numeric_string in count]

fig = plt.figure(1, [15, 10])
plt.bar(y_pos, inst_num, align='center', alpha=0.5, color=['red', 'yellow','green', 'blue', 'cyan', 'black'])
plt.xticks(y_pos, objects, fontsize=15)
plt.ylabel('The Number of Reported Instances', fontsize=20)
plt.title('The Top {} Related Drugs for {}' .format(iterations, drug), fontsize=20)
plt.savefig(outfig)

plt.show()