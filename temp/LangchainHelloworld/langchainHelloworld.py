from langchain_openai.chat_models.base import BaseChatOpenAI

llm = BaseChatOpenAI(
    model='deepseek-chat',  # 使用DeepSeek聊天模型
    openai_api_key='sk-000c2ac6c4164fb882a676b467323439',
    openai_api_base='https://api.deepseek.com',
    max_tokens=1024  # 设置最大生成token数
)

response = llm("你好")
print(response.content)  # 打印模型的回复内容

