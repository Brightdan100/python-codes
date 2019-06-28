import mysql.connector
import easygui #PLEASE INSTALL THIS USING (pip3 install easygui)

def makeDictionary(firstList, secondList):
  dictionary = {}
  for firstRow, secondRow in zip(firstList, secondList):
    dictionary[firstRow[0]] = secondRow[0]
  return dictionary

def getTableColumn(cursor, columnName, tableName):
  cursor.execute("select " + columnName + " from " + tableName)
  return cursor.fetchall()

def combineDict(dictToBeAdded, mainDict):
  for item in dictToBeAdded:
    if item in mainDict.keys():
      mainDict[item] += dictToBeAdded[item]
    else:
      mainDict[item] = dictToBeAdded[item]
  return mainDict

def groupByOrderBy(columnName):
  return "group by " + columnName + " order by " + columnName + " asc"

def blobDictionary(cursor, columnName, tableName):
  tableNumRef = getTableColumn(
    cursor, "count(" + columnName + ")", tableName + " " + groupByOrderBy(columnName)
  )
  tableBlobId = getTableColumn(
    cursor, "distinct " + columnName, tableName
  )
  return makeDictionary(tableBlobId, tableNumRef)
  
 
 #for the connection to MySQL
 #Please input the details of your MySQL database
hostName = "localhost"
userName = ""
password = ""

ProtonMailGlobal = mysql.connector.connect(
  host=hostName,
  user=userName,
  passwd=password,
  database="ProtonMailGlobal1"
)

ProtonMailShard = mysql.connector.connect(
  host=hostName,
  user=userName,
  passwd=password,
  database="ProtonMailShard1"
)

globalCursor = ProtonMailGlobal.cursor()
shardCursor = ProtonMailShard.cursor()

#Blob Master dictionary
blobStorageId = getTableColumn(globalCursor, "BlobStorageID", "BlobStorage")
blobNumRef = getTableColumn(globalCursor, "NumReferences", "BlobStorage")
blobDict = makeDictionary(blobStorageId, blobNumRef)

#other dictionaries that references the blob
attachmentDict = blobDictionary(shardCursor, "BlobStorageID", "Attachment")
outsideAttachmentDict = blobDictionary(shardCursor, "BlobStorageID", "OutsideAttachment")
contactDataDict = blobDictionary(shardCursor, "BlobStorageID", "ContactData")
sentMessageDict = blobDictionary(globalCursor, "BlobStorageID", "SentMessage")
sentAttachmentDict = blobDictionary(globalCursor, "BlobStorageID", "SentAttachment")
messageDataBodyDict = blobDictionary(shardCursor, "Body", "MessageData")
messageDataHeaderDict = blobDictionary(shardCursor, "Header", "MessageData")

#Logic for testing the inconsistencies

#we want to combine the Dictionaries
combinedDict = attachmentDict
combinedDict = combineDict(sentMessageDict, combinedDict)
combinedDict = combineDict(sentAttachmentDict, combinedDict)
combinedDict = combineDict(messageDataBodyDict, combinedDict)
combinedDict = combineDict(messageDataHeaderDict, combinedDict)
combinedDict = combineDict(contactDataDict, combinedDict)
combinedDict = combineDict(outsideAttachmentDict, combinedDict)

#now we compute the reference count mismatch & Wrong BlobStorageId
refCountMismatchList = []
missingBlobId = []
unreferencedBlobId = []

for item in combinedDict:
  if item not in blobDict.keys():
    missingBlobId += [item]
  elif blobDict[item] != combinedDict[item]:
    refCountMismatchList += [item]

for item in blobDict:
  if item not in combinedDict and blobDict[item] > 0:
    unreferencedBlobId += [item]

#This is just an MVP.
#to use the alert command below pls install easygui you can use (pip3 install easygui)
if refCountMismatchList == [] and missingBlobId == [] and unreferencedBlobId == []:
  easygui.msgbox("The DB is consistent!", title="State of Databases")
else:
  easygui.msgbox("The DB is inconsistent\nCheck below for more details", title="State of Databases")
  print("List of BlobStorageId(s) with the reference count mismatch\n", refCountMismatchList)
  print("List of BlobStorageId(s) with the missing Blob storage ID\n", missingBlobId)
  print("List of unreferencd Blob storage ID\n", unreferencedBlobId)

ProtonMailGlobal.close()
ProtonMailShard.close()
#--------------------------------------------------------------------------------------------------------exit
