from transformers import PreTrainedTokenizerFast

# 加载 tokenizer.model 文件
tokenizer = PreTrainedTokenizerFast(tokenizer_file="llama3-tokenizer.model")

# 需要分词的句子
sentence = "这是一个示例句子。"

# 使用tokenizer进行分词
token_list = tokenizer.tokenize(sentence)

# 打印分词后的结果
print(token_list)
