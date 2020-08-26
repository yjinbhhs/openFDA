# -*- coding: utf-8 -*-
"""

openFDA Case Study for AstraZeneca Oncology Data Scientist Interview, Question 2
What are the different adverse events associated with different disease areas? 

To find out what adverse events are associated with the specific disease a user inputs
Save the top events with the correspoinding numbers of occurrence into an excel spreadsheet and plot the bar plot for visualization

"""

import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from textwrap import wrap


#outcsv = sys.argv[1] 
#disease= sys.argv[2]
#iterations= sys.argv[3]
outcsv = 'disease.csv' # output file name
outfig = 'disease.png' #output figure name
disease= 'Cancer'# user specificed disease
iterations= 6 # the number of adverse events  
 
query = 'https://api.fda.gov/drug/event.json?search=patient.drug.drugindication:'+disease+'&count=patient.reaction.reactionmeddrapt.exact' # query openFDA API
record = requests.get(query).json() # read the json output from openFDA

i=0  
adv_event=[] # variable initialization    
count=[]
       
for result in record.get('results', []):
   
    if i<int(iterations):
       if('term' in str(result)):
          adv_event.append(result['term'])   # read the name of each adverse event
          count.append(str(result['count'])) # read the number of occurrence of each adverse events
          i+=1
       else:
          continue
    else:
        break

# save to the excel spread sheet
data={'Adverse Events':adv_event, 'Count':count}  
df=pd.DataFrame(data)  
df.to_csv(outcsv, header=True, index=False, line_terminator='\n')

# plot the bar plot
objects=adv_event
objects = [ '\n'.join(wrap(l, 12)) for l in objects ]
y_pos=np.arange(len(objects))
inst_num= [int(numeric_string) for numeric_string in count]

fig = plt.figure(1, [15, 10])
plt.bar(y_pos, inst_num, align='center', alpha=0.5, color=['red', 'yellow','green', 'blue', 'cyan', 'black'])
plt.xticks(y_pos, objects, fontsize=20)
plt.ylabel('The Number of Reported Instances', fontsize=20)
plt.title('The Top {} Adverse Events for {}' .format(iterations, disease), fontsize=20)
plt.savefig(outfig)

plt.show()