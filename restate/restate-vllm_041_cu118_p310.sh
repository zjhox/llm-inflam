# method come form 【cu118 安装vllm 极简教程 & 踩坑笔记】https://blog.csdn.net/phynikesi/article/details/146153068
# nvcc -V
# nvidia-smi

conda create -n vllm_041_cu118_p310 python=3.10 -y
conda activate vllm_041_cu118_p310
pip install torch==2.2.1 torchvision==0.17.1 torchaudio==2.2.1 --index-url https://download.pytorch.org/whl/cu118
pip install numpy==1.26.0
wget https://archive1.piwheels.org/simple/vllm-nccl-cu11/vllm_nccl_cu11-2.18.1.0.4.0-py3-none-any.whl#sha256=3b54bb2ebf3ee2d395cc4b4fe2178f018f109d97af9a5b4ec85f2efcc862a135
pip install vllm_nccl_cu11-2.18.1.0.4.0-py3-none-any.whl
cp /mnt/vllm-0.4.1+cu118-cp310-cp310-manylinux1_x86_64.whl .
pip install vllm-0.4.1+cu118-cp310-cp310-manylinux1_x86_64.whl
cp /mnt/xformers-0.0.25+cu118-cp310-cp310-manylinux2014_x86_64.whl .
pip install xformers-0.0.25+cu118-cp310-cp310-manylinux2014_x86_64.whl
pip install transformers==4.45.0

python -c "import os; import torch; from vllm import LLM, SamplingParams; import xformers.info; 
os.environ["VLLM_NCCL_SO_PATH"] = "/root/miniconda3/envs/vllm_041_cu118_p310/lib/python3.10/site-packages/nvidia/nccl/lib/libnccl.so.2";
print(torch.__version__);
print(xformers.info.__version__);
print(torch.cuda.nccl.version()) # 输出 NCCL 版本号;"


# 实际运行遇到 RuntimeError: Triton Error [CUDA]: device kernel image is invalidpip
    # 据说是因为 triton 版本问题，470开头的驱动太老，triton需要降级到2.1.0
    # 总之 torch高版本 需要 trition 高版本 ， 进而需要新驱动 