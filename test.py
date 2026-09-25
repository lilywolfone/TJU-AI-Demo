# 1.读取文档
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(r"D:\pycode\docs\test.pdf")
docs = loader.load()
print(f"共加载{len(docs)}页")

# 2.切分
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)
chunks = splitter.split_documents(docs)
print(f"切分后{len(chunks)}个片段")

# 3.向量化 + 存库
from langchain_commmunity.vectores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings

embeddings = DashScopeEmbeddings(model="text-embedding-v3")
vectorstore = FAISS.from_documents(chunks,embeddings)

# 4.检索
retriever = vectorstore.as_retriever(search_kwargs={"k":3})
results = retriever.invoke("你的问题")
for r in results:
    print(r.page_content[:100])

    # 5.交给大模型生产答案
    from langchain_community.llms import Tongyi
    from langchain_core.prompts import ChatPromptTemplate
    llm = Tongyi(model="qwen-max")
    prompt = ChatPromptTemplate.from_template(
        "根据以下上下文回答问题，上下文没有的就说不知道： \n{context}\n\n问题: {question}"
    )

    context = "\n\n".join([r.page_content for r in results])
    response = llm.invoke(prompt.format(context=context,question="你的问题"))
    print(response)