import chromadb
import csv

def getCollection():
	chroma_client= chromadb.PersistentClient(path="./chromadb")
	try:
		collection=chroma_client.create_collection(name="claims")
		print("Created Claims collection ")
	    #chroma_client.delete_collection("countries")
	except chromadb.db.base.UniqueConstraintError:
		print("Claims collection already exists, deleting")
		chroma_client.delete_collection(name="claims")
		collection=chroma_client.create_collection(name="claims")
		print("Created Claims collection ")
	return collection

def getContext():


	collection=getCollection()


	
	with open("context_help.csv",mode='r') as f:
		lines=list(csv.reader(f))
	i=0
	for line in lines:
                i+=1
                if i==1: continue
                
                claim_string=f"""Member Id= {line[0]}, Claimd ID= {line[1]}, date of service= {line[2]}, Provider ID ={line[3]}, provider name= {line[4]}, Service code={line[5]}, claim status= {line[6]}, billed amount= {line[7]}, paid amount={line[8]}, copayment = {line[9]}, deductible ={line[10]}, deniedreason ={line[11]}, holdreason={line[12]}"""
                #print(claim_string)
                collection.upsert(documents=claim_string,metadatas=[{"member_id":line[0], "provider_id":line[3] }],ids=[str(i)])    
	#print(collection.peek())

if __name__=="__main__":
        getContext()

