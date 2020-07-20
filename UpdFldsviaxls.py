import sys, os, arcpy
import pandas as pd

workspace = r'D:\LGEKU\Users\Rahul\data\test.gdb'     
filepath=  r'D:\LGEKU\Users\Rahul\data\log.txt'
xlsFile = r"D:\LGEKU\Users\Rahul\1.xls"

df = pd.read_excel(xlsFile, sheetname=0)

fclassname = 'UtilityNetwork\Pipelinedevice'
fclass = r"{}\{}".format(workspace, fclassname)

listOid = df['OBJECTID'].tolist()
updFld = df['fieldName'].tolist()

updobjid=[]
	

fields = ['OBJECTID','fieldName']
MyDict = dict(zip(listOid,updFld))
print "updating--"+str(len(listOid))+ " "+str(len(updFld))
cnt=0
#edit = arcpy.da.Editor(workspace)
#edit.startEditing(True, False)
with arcpy.da.UpdateCursor(fclass, fields) as cursor:
    for row in cursor:
        objid = int(row[0])
        try: 
            var1=MyDict[objid]
            row[1] = var1
            cursor.updateRow(row)
            cnt = cnt + 1
            updobjid.append(str(objid))
            print str(cnt)
        except KeyError, e:
           pass
#edit.stopEditing(True)
print "writing updated id!"
with open(filepath,"w") as file:
    for item in updobjid:
        file.write(str(item) + '\n')
print ("Done")        
