TJU-AI-Demo
基于 LangChain + RAG 的文档问答 Demo，并包含针对个人敏感信息的数据脱敏脚本。项目用于验证"大模型 + 本地知识库"问答链路的可行性，以及 AI 处理数据前的隐私保护实践。

技术栈
Python
LangChain / langchain-community / langchain-text-splitters
FAISS（向量检索）
DashScope Embeddings（text-embedding-v3）+ 通义千问 qwen-plus
pypdf（PDF 读取）
re（正则，数据脱敏规则）

功能模块
1. RAG 文档问答（主流程）
完整链路：
文档读取： PyPDFLoader  加载本地 PDF
文本切分： RecursiveCharacterTextSplitter （chunk_size=500，chunk_overlap=50）
向量化建库： DashScopeEmbeddings  生成向量， FAISS.from_documents  建库
相似度检索： as_retriever  +  invoke ，召回最相关片段（top-k=3）
大模型生成：检索结果与问题拼接进  ChatPromptTemplate ，交给  ChatTongyi （qwen-plus）生成回答
2. 数据脱敏脚本
基于正则规则（ FIELD_RULES  +  desensitize ）对身份证、手机号、姓名、民族、学院、专业等字段做脱敏处理，用于在把数据交给大模型之前先做隐私保护。

项目结构
rag_test.py ：RAG 完整链路演示（主流程）
test.py ：RAG 链路测试脚本（与 rag_test.py 结构相近，用于对比验证）
rag_demo.py ：数据脱敏脚本
README.md ：项目说明
.gitignore ：忽略规则

运行方式
安装依赖：
pip install langchain langchain-community langchain-text-splitters faiss-cpu pypdf 

配置 API Key（建议用环境变量，不要硬编码）：
 set DASHSCOPE_API_KEY=你的key 

准备测试 PDF，放到代码中指定的路径

运行：
 python rag_test.py 
**输入：** 张三的学院和专业是什么？
**输出：** 该同学的学院为**，专业为**
**说明：** 涉及个人身份信息的字段在送入大模型前已由 desensitize() 处理，
因此模型返回的内容中不包含原始敏感信息。
 --- 原文 ---
姓名 张三 民族 汉族 学院 精密仪器与光电子工程学院 专业 测控技术与仪器 手机号 13800138000
--- 脱敏后 ---
姓名 张** 民族 ** 学院 ** 专业 **
PS D:\pycode> 


说明
项目目前处于学习验证阶段，后续计划加入交互界面、支持更多文档类型，并把脱敏模块与 RAG 流程打通，形成"先脱敏、再入库、再问答"的完整链路。
