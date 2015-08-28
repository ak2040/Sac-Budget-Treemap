

import pandas as pd 
import numpy as np
import json
import math

INPATH=''
DESCPATH=''
OUTPATH=''

OTHER_CUTOFF=.04

df_all=pd.read_excel(INPATH+'sac_budget_t1_v2.xlsx', 'Sheet1')
df_all=df_all.reset_index(drop=True)
del df_all['department_text']

tf=pd.read_excel(DESCPATH+'descriptions.xlsx', 'Sheet1').reset_index(drop=True)
tf_dept=tf[['department','department_text']].drop_duplicates()
tf_div=tf[['division','division_text']].drop_duplicates()

merged=pd.merge(df_all, tf_dept, how='left', on='department')   #merging text descriptions
merged=pd.merge(merged, tf_div, how='left', on='division')

df_all=merged
df_all.ix[df_all.division_text.isnull(), 'division_text']=''
df_all.ix[df_all.department_text.isnull(), 'department_text']=''
TIER2=[]
T2_SUM=df_all.amount2016.sum()
OTHERGRP2=[]
for T1 in np.unique(df_all.department.values.ravel()):
    TIER1=[]
    df1=df_all[df_all.department==T1]
    T1_text=df1.reset_index().department_text[0]
    T1_SUM=df1.amount2016.sum()
    OTHERGRP1=[]
    for T0 in np.unique(df1.division.values.ravel()):
        tf=df1[df1.division==T0]
        T0_text=tf.reset_index().division_text[0].encode('utf-8')
        tf=tf.ix[:, 'departmentdescription':'change']
        tf=tf.rename(columns={'departmentdescription': 'name'})    
        del tf['change']    #don't need this will do in javascript
        T0_SUM=tf.amount2016.sum()
        tfbig=tf[tf.amount2016/T0_SUM>=OTHER_CUTOFF].reset_index(drop=True)
        tfsm=tf[tf.amount2016/T0_SUM<OTHER_CUTOFF].reset_index(drop=True)
        JSONCHILDS=json.loads(tfbig.to_json(orient="records"))
        JSONSMALLS=json.loads(tfsm.to_json(orient="records"))
        JSONCHILDS.append({"name" : "Other", "children": JSONSMALLS})
        if T0_SUM/T1_SUM<OTHER_CUTOFF:
            OTHERGRP1.append({"name": T0, "children": JSONCHILDS})
        else:       
            TIER1.append({"name": T0, "desc" : T0_text, "children": JSONCHILDS})
    TIER1.append({"name": "Other", "children": OTHERGRP1})
    if T1_SUM/T2_SUM<OTHER_CUTOFF:
        OTHERGRP2.append({"name": T1, "desc": T1_text, "children": TIER1})
    else:   
        TIER2.append({"name": T1, "desc": T1_text, "children": TIER1})
TIER2.append({"name": "Other", "children": OTHERGRP2})
TIER3={"name": "Sacramento Budget 2015/16", "children": TIER2}

j = json.dumps(TIER3, indent=1)
f = open(OUTPATH+'sacbudget_v2.json', 'w')
print >> f, j
f.close()
