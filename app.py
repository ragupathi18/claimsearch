import os
import requests

import chromadb





#API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"



class ClaimAssistant():
    def __init__(self)-> None:
        self.API_TOKEN=os.environ["API_TOKEN"] #Set a API_TOKEN environment variable before running
        self.API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"        



    def query(self,prompt):
        headers = {"Authorization": f"Bearer {self.API_TOKEN}"}
        payload = {
            "inputs": prompt,
            "parameters": { #Try and experiment with the parameters
                "max_new_tokens": 1050,
                "temperature": 0.1,
                "top_p": 0.5,
                "do_sample": False,
                "return_full_text": False
            }
        }
        response = requests.post(self.API_URL, headers=headers, json=payload)
        #print(response.json())
        return response.json()[0]['generated_text'].strip()

    def getQuestion(self):
        print("")
        question=input("Enter your question (quit to stop): ")
        return question

    def getCollection(self):
        chroma_client= chromadb.PersistentClient(path="./chromadb")
        collection=chroma_client.get_collection(name="claims")
        return collection
    
##########Main################


#print(collection.peek())

    def main():

        from transformers import AutoTokenizer, AutoModelForTokenClassification
        ner_model_id = 'dslim/bert-base-NER'
        tokenizer = AutoTokenizer.from_pretrained(ner_model_id)
        ner_model = AutoModelForTokenClassification.from_pretrained(ner_model_id)

        from transformers import pipeline
        ner_pipeline = pipeline("ner", model=ner_model, tokenizer=tokenizer)

        mem_id="MEM1"

        while 1:
            question=getQuestion()
            if question.lower()=="quit":
                break
            #print(question)
            #question = "Who is the mayor of Jacksonville, Florida?"
            #context = "Donna Deagon became the mayor of Jacksonville FL in 2023."
            #print(question)
            #country=ner_pipeline(question)
            #print(country)

            #prep_prompt=f"""Use the following context and answer the question. Stop when you've answered the question. Do not generate any more than that     {question}     Question: What is the country name referred?"""

            #answer=query(prep_prompt)
            #print(answer.strip().splitlines())
            #print(answer.strip().splitlines()[0].split(':')[1].strip())
            
            context=collection.query(query_texts=question, where={"member_id":mem_id},n_results=3)["documents"]
            #print(context)

            prompt = f"""Use the following context to answer the question at the end preciously.

            {context}
        {question}
            """
            #print(prompt)
            print("HF Model : ")
            print (prompt)
            print(query(prompt))

if __name__=="__main__":
        getContext()
