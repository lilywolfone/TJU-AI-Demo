from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings

pdf_path = r"D:\pycode\docs\text1.pdf"
docs = PyPDFLoader(pdf_path).load()

docs = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
).split_documents(docs)
print(f"切分后共 {len(docs)} 个片段")

emb = DashScopeEmbeddings(model="text-embedding-v3")
db = FAISS.from_documents(docs, emb)

qa = db.as_retriever()
results = qa.invoke("第一章主要讲了哪些概念")

if results:
    print("=== 检索到的第一段内容 ===")
    print(results[0].page_content)
else:
    print("没检索到内容，检查 PDF 是否成功读取")
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatTongyi(model="qwen-plus")

prompt = ChatPromptTemplate.from_template(
    """请根据以下参考资料回答问题。
如果资料中没有相关信息，请直接说明「资料中未提及」，不要自行编造。

参考资料：
{context}

问题：{question}"""
)

chain = prompt | llm | StrOutputParser()

question = "宿舍楼内有哪些禁止行为"

if results:
    context = "\n\n".join(r.page_content for r in results)
    answer = chain.invoke({"context": context, "question": question})
    print("=== 生成答案 ===")
    print(answer)
else:
    print("没检索到内容，检查 PDF 是否提取到文字")