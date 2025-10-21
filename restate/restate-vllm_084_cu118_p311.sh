# method come from 【cuda11.8安装vllm】https://zhuanlan.zhihu.com/p/1898821639820539615
# nvcc -V
# nvidia-smi

conda create -n vllm_084_cu118_p311 python=3.11 -y
conda activate vllm_084_cu118_p311

# 高亮输出echo结果
echo -e "\033[1;32m 这里以下调换了安装torch和vllm的顺序，不确定是否可行 \033[0m"

pip3 install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 -i https://download.pytorch.org/whl/cu118
cp /mnt/vllm-0.8.4+cu118-cp38-abi3-manylinux1_x86_64.whl .
pip install vllm-0.8.4+cu118-cp38-abi3-manylinux1_x86_64.whl
pip3 install -U xformers==0.0.29.post3 --index-url https://download.pytorch.org/whl/cu118

python -c "import os; import torch; from vllm import LLM, SamplingParams; import xformers.info; 
print(torch.__version__);
print(xformers.info.__version__);
print(torch.cuda.nccl.version()) # 输出 NCCL 版本号;"
