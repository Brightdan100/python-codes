import mysql.connector

'''mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Success222.",
  database="protonMail"
)

myCursor = mydb.cursor()

myCursor.execute("SELECT BlobStorageID FROM BlobStorage")
myResult = myCursor.fetchall()
myCursor.execute("SELECT NumReferences FROM BlobStorage")
myResult2 = myCursor.fetchall()

dictionary = {}
for row1, row2 in zip(myResult, myResult2):
    dictionary[row1[0]] = row2[0]
    
print(dictionary)

import mysql.connector'''

def makeDictionary(firstList, secondList):
  dictionary = {}
  for firstRow, secondRow in zip(firstList, secondList):
    dictionary[firstRow[0]] = secondRow[0]
  return dictionary

def getTableColumn(cursor, columnName, tableName):
  cursor.execute("SELECT " + columnName + " FROM " + tableName)
  return cursor.fetchall()

def combineDict(dictToBeAdded, mainDict):
  for item in dictToBeAdded:
    if item in mainDict.keys():
      mainDict[item] += dictToBeAdded[item]
    else:
      mainDict[item] = dictToBeAdded[item]
  return mainDict
 

ProtonMailGlobal = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Success222.",
  database="ProtonMail"
)

ProtonMailShard = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Success222.",
  database="ProtonMailShard"
)


globalCursor = ProtonMailGlobal.cursor()
shardCursor = ProtonMailShard.cursor()

#Blob Master dictionary
blobStorageId = getTableColumn(globalCursor, "BlobStorageID", "BlobStorage")
blobNumRef = getTableColumn(globalCursor, "NumReferences", "BlobStorage")
blobDict = makeDictionary(blobStorageId, blobNumRef)

#other dictionaries that reference the blob

#for ProtonMailShard.Attachment
attachmentNumRef = getTableColumn(
  shardCursor, "COUNT(BlobStorageID)","Attachment group by BlobStorageID order by BlobStorageID asc"
)
attachmentBlobId = getTableColumn(
  shardCursor, "DISTINCT BlobStorageID", "Attachment"
)
attachmentDict = makeDictionary(attachmentBlobId, attachmentNumRef)

#for ProtonMailShard.OutsideAttachment
#.......Currently this table is empty, but once it has values
# we can create a dictionary for it, we can as well create values for it even without values
# we would just have an empty dictionary which will do no harm to the code 

#for ProtonMailShard.ContactData
#.......Same condition as ProtonMailShard.OutsideAttachment

#for ProtonMailGlobal.SentMessage
sentMessageNumRef = getTableColumn(
  shardCursor, "COUNT(BlobStorageID)","ContactData group by BlobStorageID order by BlobStorageID asc"
)
sentMessageBlobId = getTableColumn(
  shardCursor, "DISTINCT BlobStorageID", "ContactData"
)
sentMessageDict = makeDictionary(sentMessageBlobId, sentMessageNumRef)

#for ProtonMailGlobal.SentAttachment
sentAttachmentNumRef = getTableColumn(
  globalCursor, "COUNT(BlobStorageID)","SentAttachment group by BlobStorageID order by BlobStorageID asc"
)
sentAttachmentBlobId = getTableColumn(
  globalCursor, "DISTINCT BlobStorageID", "SentAttachment"
)
sentAttachmentDict = makeDictionary(sentAttachmentBlobId, sentAttachmentNumRef)

#for headers in ProtonMailShard.MessageData (I assumed that the Body is the blobStorageId)
messageDataNumRef = getTableColumn(
  shardCursor, "COUNT(Body)","MessageData group by Body order by Body asc"
)
messageDataBlobId = getTableColumn(
  shardCursor, "DISTINCT Body", "MessageData"
)
messageDataDict = makeDictionary(messageDataBlobId, messageDataNumRef)


#Logic for testing the inconsistencies

#we want to combine the Dictionaries
combinedDict = attachmentDict
combinedDict = combineDict(sentMessageDict, combinedDict)
combinedDict = combineDict(sentAttachmentDict, combinedDict)
combinedDict = combineDict(messageDataDict, combinedDict)

print(combinedDict)
print(blobDict)
#now we compute the reference count mismatch & Wrong BlobStorageId
refCountMismatchList = []
wrongBlobId = []
unreferencedBlobId = []

for item in combinedDict:
  if item not in blobDict.keys():
    wrongBlobId += [item]
  elif blobDict[item] != combinedDict[item]:
    refCountMismatchList += [item]

for item1 in blobDict:
  if item1 not in combinedDict and blobDict[item1] > 0:
    unreferencedBlobId += [item1]

#print("List of BlobStorageId(s) with the reference count mismatch\n", refCountMismatchList)
#print("List of BlobStorageId(s) with the wrongBlob storage ID\n", wrongBlobId)
#print("List of unreferencd Blob storage ID\n", unreferencedBlobId)
#
#The output can ofcourse be modified to suit a purpose
#This is just an MVP.
'''for item in unreferencedBlobId:
  print(item)'''

ProtonMailGlobal.close()
ProtonMailShard.close()
#--------------------------------------------------------------------------------------------
