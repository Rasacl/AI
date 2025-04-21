## 简单的语言模型
## 必须先安装 transformers 和 torch

# 基本导入
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM


def create_simple_llm():
    """
    创建一个使用小型 GPT-2 模型的简单语言模型。
    GPT-2（最小版本）非常适合演示，因为它：
    - 相对较小（124M 参数）
    - 在 CPU 上运行速度足够快
    - 适合理解基本概念
    """
    # 初始化模型和分词器
    model_name = "uer/gpt2-chinese-cluecorpussmall"  # 使用 DistilGPT-2（GPT-2 的小型版本）

    # 创建生成器管道
    generator = pipeline("text-generation", model=model_name, pad_token_id=50256)

    return generator


def generate_text(generator, prompt, max_length=1000):
    """
    基于提示生成文本
    """
    # 生成文本
    result = generator(
        prompt,  # 输入文本
        max_length=max_length,  # 生成文本的最大长度
        num_return_sequences=1,  # 生成的不同序列数量
        do_sample=True,  # 使用采样而不是贪婪解码
        temperature=0.7,  # 采样的随机性（0 = 确定性，1 = 随机）
    )

    return result[0]["generated_text"]


# 教育演示
def run_llm_demo():
    """
    演示基本的语言模型功能并附带解释
    """
    print("🤖 正在加载简单语言模型...")
    generator = create_simple_llm()

    print("\n✨ 简单语言模型演示 ✨")
    print("这个演示展示了使用小型语言模型的基本文本生成")

    # 用于演示不同功能的示例提示
    prompts = [
        "快速的棕色狐狸",
        "很久很久以前",
        "Python编程是",
    ]

    for prompt in prompts:
        print("\n🔹 提示:", prompt)
        print("🔸 生成:", generate_text(generator, prompt))
        input("\n按回车键查看下一个示例...")


# 交互式演示
def interactive_demo():
    """
    允许用户与模型交互
    """
    generator = create_simple_llm()

    print("\n🤖 交互式语言模型演示")
    print("输入你的提示（输入 'quit' 退出）")

    while True:
        prompt = input("\n✍️ 输入你的提示: ")
        if prompt.lower() == "quit":
            break

        response = generate_text(generator, prompt)
        print("\n💭 生成的响应:")
        print(response)


# 过程的教育可视化
def explain_process():
    """
    通过简单示例解释语言模型的工作过程
    """
    print("\n🎓 工作原理:")
    print("1. 输入文本 → 分词 → 数字")
    print("2. 数字 → 模型处理 → 预测")
    print("3. 预测 → 新标记 → 输出文本")

    # 简单的分词示例
    tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
    text = "Hello world!"
    tokens = tokenizer.encode(text)
    decoded = tokenizer.decode(tokens)

    print("\n📝 分词示例:")
    print(f"原始文本: '{text}'")
    print(f"转换为标记（数字）: {tokens}")
    print(f"解码回文本: '{decoded}'")


if __name__ == "__main__":
    print("选择演示:")
    print("1. 运行基本演示")
    print("2. 交互模式")
    print("3. 解释工作过程")

    choice = input("输入你的选择 (1-3): ")

    if choice == "1":
        run_llm_demo()
    elif choice == "2":
        interactive_demo()
    elif choice == "3":
        explain_process()
    else:
        print("无效的选择!")