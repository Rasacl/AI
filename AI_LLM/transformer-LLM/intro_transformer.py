# 从 Transformers 库创建一个简单的 LLM - 简单
from transformers import pipeline, AutoTokenizer

def create_simple_llm():
    '''
      创建一个简单的 LLM 用GPT2模型
      GPT2模型是一个基于Transformer架构的语言模型，
      它在大量的文本数据上进行了预训练，
      可以用于生成文本、回答问题、翻译等任务。
    '''
    # 加载预训练的模型和分词器
    model_name = "uer/gpt2-chinese-cluecorpussmall"
    # 加载预训练的模型和分词器 参数 pad_token_id=50256 表示填充token的id 
    # 这里的50256是gpt2模型的特殊token，用于填充文本到固定长度
    generator = pipeline("text-generation", model=model_name, pad_token_id=50256)
    # 返回生成器
    return generator

generator = create_simple_llm()

prompt = "你好，我是一个语言模型，l"
 
# 生成文本 prompt是提示参数 max_length=50 表示生成的文本长度为50个token
# num_return_sequences=1 表示生成1个文本
generator_text = generator(prompt, max_length=1000, num_return_sequences=1)
print(generator_text[0])