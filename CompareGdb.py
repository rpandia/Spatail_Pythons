import arcpy
import os
from arcpy import env
import datetime
import json, ast

arcpy.env.overwriteOutput = True
StrtTime = datetime.datetime.now().strftime("%a, %d %B %Y %H:%M:%S")
print "Started At :"+StrtTime

# set our current workspace
#bseGdb=r'C:/Workspace/P1D6.gdb'
#tgtGdb=r'C:/Workspace/P1D6_CPY.gdb'
#outPathWorkspace = r'C:/Workspace/'

bseGdb = arcpy.GetParameterAsText(0)
tgtGdb = arcpy.GetParameterAsText(1)
outPathWorkspace = arcpy.GetParameterAsText(2)

#define a field to sort by
sortField="OBJECTID"

# define an output file 
outPath=os.path.join(outPathWorkspace,'log.txt')
compare_file = os.path.join(outPathWorkspace,'tmp.txt')
outCsv = os.path.join(outPathWorkspace,'Error.csv' )

fields = "Feature Class Name,Object Id,Error Message,Base GDb Value, Target Gdb Value\n"  
#fields = "Feature Class Name,Object Id,Error Message\n"  
f = open(outCsv, "w")
f.write(fields)
f.close()

fn = open(outPath, "w")
bseFcLst=[]
tgtFcLst=[]

bseTbLst=[]
tgtTbLst=[]

bseFc=[]
bseTb=[]

tgtFc=[]
tgtTb=[]


env.workspace = bseGdb
print bseGdb
print tgtGdb
print outPathWorkspace

#call ListFeatureClass function
fcList = arcpy.ListFeatureClasses()
# Print the name of the current fc:
for fc in fcList:
    bseFc.append(fc)
datasets = arcpy.ListDatasets(feature_type='feature')
datasets = [''] + datasets if datasets is not None else []
for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path = os.path.join(ds, fc)
        bseFc.append(path)

# Get and print a list of tables
tables = arcpy.ListTables()
for table in tables:
    bseTb.append(table)
        
bseDomDict = {} # empty dictionary
domains = arcpy.da.ListDomains()
for domain in domains:
    if domain.domainType == 'CodedValue':
        if domain.name not in bseDomDict:
            vList = [] # empty list
            coded_values = domain.codedValues
            for val, desc in coded_values.items():
                vList.append({val:desc})
        bseDomDict[domain.name] = vList
"""
#print "bseDomDict***"+str(bseDomDict)
for key in bseDomDict.keys():
    for value in bseDomDict[key]:
        print key,value
"""
env.workspace = tgtGdb

#call ListFeatureClass function
fcList = arcpy.ListFeatureClasses()
# Print the name of the current fc:
for fc in fcList:
    tgtFc.append(fc)
datasets = arcpy.ListDatasets(feature_type='feature')
datasets = [''] + datasets if datasets is not None else []
for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path = tgtFc.append(os.path.join(ds, fc))  
        tgtFc.append(path)        
# Get and print a list of tables
tables = arcpy.ListTables()
for table in tables:
    tgtTb.append(table)

tgtDomDict = {} # empty dictionary
domains = arcpy.da.ListDomains()
for domain in domains:
    if domain.domainType == 'CodedValue':
        if domain.name not in tgtDomDict:
            vList = [] # empty list
            coded_values = domain.codedValues
            for val, desc in coded_values.items():
                vList.append({val:desc})
        tgtDomDict[domain.name] = vList
"""
for key in tgtDomDict.keys():
    for value in tgtDomDict[key]:
        print key,value
"""
f1=open(outCsv,'a')
value = { k : tgtDomDict[k] for k in set(tgtDomDict) - set(bseDomDict) }
#print value
for key in value.keys():
    for vv in value[key]:
        #print key,value
        wlLine = "DomainName:"+str(key)+",-1,value not found in Base Gdb,, "+ str(ast.literal_eval(json.dumps(vv)))+"\n"
        fn.write(wlLine)
        f1.write(wlLine)
bseFc.sort()
tgtFc.sort()
bseTb.sort()
tgtTb.sort()
a = bseFc
b = tgtFc
c = bseTb
d = tgtTb

fn.write("Feature class not found in Target geodatabase ("+ tgtGdb +") class are : \n")
itemlist = list(set(a)-set(b))
if itemlist is not None:
    for nn in itemlist:
        wlLine = str(nn)+",-1,Feature class not found in Target geodatabase "+ str(tgtGdb)+"\n"
        fn.write(wlLine)
        f1.write(wlLine)
    fn.write("\n---------------\n")
fn.write("Feature class not found in base geodatabase ("+ bseGdb +") class are : \n")
itemlist[:] = []
itemlist = list(set(b)-set(a))
if itemlist is not None:
    for nn in itemlist:
        wlLine = str(nn)+",-1,Feature class not found in base geodatabase "+ str(bseGdb)+"\n"
        fn.write(wlLine)
        f1.write(wlLine)
    fn.write("\n---------------\n")
fn.write("Tables not found in Target geodatabase ("+ tgtGdb +") class are : \n")
itemlist[:] = []
itemlist = list(set(c)-set(d))
if itemlist is not None:
    for nn in itemlist:
        wlLine = str(nn)+",-1,Tables class not found in Target geodatabase "+ str(tgtGdb)+"\n"
        fn.write(wlLine)
        f1.write(wlLine)
    fn.write("\n---------------\n")
fn.write("Tables not found in base geodatabase ("+ bseGdb +") class are : \n")
itemlist[:] = []
itemlist = list(set(d)-set(c))
#print itemlist
if itemlist is not None:
    for nn in itemlist:
        wlLine = str(nn)+",-1,Tables class not found in base geodatabase "+ str(bseGdb)+"\n"
        fn.write(wlLine)
        f1.write(wlLine)
    fn.write("\n---------------\n")
f1.close()

bseFcLst = []
for i in a:
    if i  in b:
       bseFcLst.append(i)
bseTclst = []
for i in c:
    if i in d:
       bseTclst.append(i)
for k in bseFcLst:
    try:
        # Set local variables
        base_features = str(os.path.join(bseGdb,k))
        test_features = str(os.path.join(tgtGdb,k))
        sort_field = sortField
        compare_type = "All"
        ignore_option = "IGNORE_M;IGNORE_Z"
        xy_tolerance = "0.001 METERS"
        m_tolerance = 0
        z_tolerance = 0
        attribute_tolerance = "Shape_Length 0.001"
        omit_field = "#"
        continue_compare = "CONTINUE_COMPARE"

        # Process: FeatureCompare
        compare_result = arcpy.FeatureCompare_management(base_features, test_features, sort_field, compare_type, ignore_option, xy_tolerance, m_tolerance, z_tolerance, attribute_tolerance, omit_field, continue_compare, compare_file)
        fn.write("\n---------------\n")
        fn.write("For Feature class name :"+base_features+"\n")
        fn.write("\n---------------\n")
        fn.write(arcpy.GetMessages())
        fn.write("\n---------------\n")
        f=open(compare_file)  
        f1=open(outCsv,'a')
        for x in f.readlines():
            ss = str(x)
            #print "going for Next value"
            #print ss
            checker1 = None  
            #if 'RelationshipClass relationship class ID is different' in ss:
                #checker1 = True
            if 'Feature Types Are Different' in ss:
                checker1 = True                  
            if 'Spatial references are different' in ss:
                wlLine = str(k)+",-1,Spatial references are different \n"
                f1.write(wlLine)
                checker1 = True
            if 'Spatial References have different XY precision' in ss:
                wlLine = str(k)+",-1,Spatial References have different XY precision \n"
                f1.write(wlLine)
                checker1 = True
            if 'Spatial References have different M precision' in ss:
                wlLine = str(k)+",-1,Spatial References have different M precision \n"
                f1.write(wlLine)
                checker1 = True             
            if checker1 is None:
                pp =ss.split(',')
                errMsg= pp[2].strip()
                Basevalue= pp[3].strip()
                Targetvalue= pp[4].strip()
                errMsg= pp[2].strip()
                errMsg = errMsg.replace('"', '')
                #ppVal = errMsg.split(' is ')
                #for p in ppVal:
                    #errMsg = p
                objectId= pp[5].strip()
                errMsg = str(errMsg).title()
                wlLine = str(k)+","+objectId+","+str(errMsg).title()+","+Basevalue+","+Targetvalue+"\n"
                #wlLine = str(k)+","+objectId+","+str(errMsg).title() +"\n"
                checker = None 
                if "-1,Different,\"false\",\"true\"" in wlLine:
                    checker = True               
                if "-1,Different,\"true\",\"false\"" in wlLine:
                    checker = True
                if ",ObjectID,Message" in wlLine:
                    checker = True
                if " Are The Same" in errMsg:
                    checker = True
                if " Same Number Of Fields" in errMsg:
                    checker = True
                if checker is None:
                    #print(wlLine)
                    f1.write(wlLine)
                #print "Going Out"
        f.close()
        f1.close()
        if os.path.isfile(compare_file):
            os.remove(compare_file)
            os.remove(os.path.join(outPathWorkspace,'tmp.xml'))           
    except Exception as err:
        print(err.args[0])

for k in bseTclst:
    try:
        # Set local variables
        base_table = str(os.path.join(bseGdb,k))
        test_table = str(os.path.join(tgtGdb,k))
        #print base_table + " <> " +test_table
        sort_field = sortField
        compare_type = "ALL"
        ignore_option = "IGNORE_EXTENSION_PROPERTIES"
        attribute_tolerance = "#"
        omit_field = "#"
        continue_compare = "CONTINUE_COMPARE"
         
        # Process: FeatureCompare
        compare_result = arcpy.TableCompare_management(base_table, test_table, sort_field, compare_type, ignore_option, attribute_tolerance, omit_field, continue_compare, compare_file)
        fn.write("\n---------------\n")
        fn.write("For Table name :"+base_table+"\n")
        fn.write("\n---------------\n")
        fn.write(arcpy.GetMessages())
        fn.write("\n---------------\n")
        f=open(compare_file)  
        f1=open(outCsv,'a')
        for x in f.readlines():
            ss = str(x)
            checker1 = None   
            if ',Different,' in ss:
                checker1 = True
            if 'Feature Types Are Different' in ss:
                checker1 = True                
            if 'Spatial references are different' in ss:
                wlLine = str(k)+",-1,Spatial references are different \n"
                f1.write(wlLine)
                checker1 = True
            if 'Spatial References have different XY precision' in ss:
                wlLine = str(k)+",-1,Spatial References have different XY precision \n"
                f1.write(wlLine)
                checker1 = True
            if 'Spatial References have different M precision' in ss:
                wlLine = str(k)+",-1,Spatial References have different M precision \n"
                f1.write(wlLine)
                checker1 = True            
            if checker1 is None:            
                pp =ss.split(',')
                errMsg= pp[2].strip()
                Basevalue= pp[3].strip()
                Targetvalue= pp[4].strip()
                errMsg= pp[2].strip()
                errMsg = errMsg.replace('"', '')
                #ppVal = errMsg.split(' is ')
                #for p in ppVal:
                    #errMsg = p
                objectId= pp[5].strip()
                errMsg = str(errMsg).title()
                wlLine = str(k)+","+objectId+","+str(errMsg).title()+","+Basevalue+","+Targetvalue+"\n"
                #wlLine = str(k)+","+objectId+","+str(errMsg).title() +"\n"
                checker = None 
                if ",ObjectID,Message" in wlLine:
                    checker = True
                if " Are The Same" in errMsg:
                    checker = True
                if " Same Number Of Fields" in errMsg:
                    checker = True
                if checker is None:
                    #print(wlLine)
                    f1.write(wlLine)
        f.close()
        f1.close()
        if os.path.isfile(compare_file):
            os.remove(compare_file)
            os.remove(os.path.join(outPathWorkspace,'tmp.xml'))           
    except Exception as err:
        print(err.args[0])
fn.close()
EndTime = datetime.datetime.now().strftime("%a, %d %B %Y %H:%M:%S")
print "Ended At :"+EndTime
print "Done"
