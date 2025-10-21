import os

# os.environ["VLLM_NCCL_SO_PATH"] = "/root/miniconda3/envs/vllm_310/lib/python3.10/site-packages/nvidia/nccl/lib/libnccl.so.2"

import torch
from vllm import LLM, SamplingParams
import xformers.info

print(torch.__version__)
print(xformers.info.__version__)
print(torch.cuda.nccl.version()) # 输出 NCCL 版本号