from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
import torch
import transformers, accelerate
from langchain.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings
from langchain import VectorDBQA 
from langchain.llms import HuggingFacePipeline

load_dotenv()

qdrant_host = os.getenv('QDRANT_HOST')
qdrant_api_key = os.getenv('QDRANT_API_KEY')
qdrant_collection_name = os.getenv('QDRANT_COLLECTION_NAME')

bnb_config = transformers.BitsAndBytesConfig(
    load_in_8bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16
)


class chain:
    def __init__(self):
        model_id = "meta-llama/Llama-2-7b-chat-hf"
        model_config = transformers.AutoConfig.from_pretrained(
            model_id
        )

        self.model = transformers.AutoModelForCausalLM.from_pretrained(
            model_id,
            trust_remote_code=True,
            config=model_config,
            quantization_config=bnb_config,
            device_map='auto',
        )

        self.model.eval()
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(
            model_id
        )
        generate_text = transformers.pipeline(
                model=self.model,
                tokenizer=self.tokenizer,
                task="text-generation",
                return_full_text=True,
                temperature=0.01,
                max_new_tokens=1025
            )
        self.llm = HuggingFacePipeline(pipeline=generate_text)
    def make_qa(self):
        client = QdrantClient(
        os.getenv('QDRANT_HOST'),
        api_key = qdrant_api_key)

        embed_model_id = 'WhereIsAI/UAE-Large-V1' 
        embeddings = HuggingFaceEmbeddings(model_name = embed_model_id) 
 
        doc_store = Qdrant(client=client,
            collection_name=qdrant_collection_name,
                            embeddings=embeddings)
        qa = VectorDBQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            vectorstore=doc_store,
            return_source_documents=False,
            k = 8
        ) 

        return qa