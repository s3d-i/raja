import torch

# 假设 'model.pth' 是你的 .pth 文件路径
model = torch.load('E:/llama-models/Meta-Llama-Guard-3-8B/consolidated.00.pth')
torch.save(model, 'Meta-Llama-Guard-3-8B.bin')