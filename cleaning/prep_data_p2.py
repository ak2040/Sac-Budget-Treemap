

import pandas as pd 
import numpy as np
import json

INPATH='/Sac_Budget/prep_data/temp/'
OUTPATH='/Sac_Budget/for github/data/'


df_all=pd.read_excel(INPATH+'sac_budget_t1.xlsx', 'Sheet1')
df_all=df_all.reset_index()

TIER3=[]
for T2 in np.unique(df_all.groupsection.values.ravel()):
    TIER2=[]
    df2=df_all[df_all.groupsection==T2]
    for T1 in np.unique(df2.department.values.ravel()):
        TIER1=[]
        df1=df2[df2.department==T1]
        for T0 in np.unique(df1.division.values.ravel()):
            tf=df1[df1.division==T0]
            tf=tf.ix[:, 'departmentdescription':'change']
            tf=tf.rename(columns={'departmentdescription': 'name'})      
            TIER1.append({"name": T0, "children": json.loads(tf.to_json(orient="records"))})
        TIER2.append({"name": T1, "children": TIER1})
    TIER3.append({"name": T2, "children": TIER2})
TIER4={"name": "Sacramento Budget 2015/16", "children": TIER3}

j = json.dumps(TIER4, indent=1)
f = open(OUTPATH+'sacbudget.json', 'w')
print >> f, j
f.close()
