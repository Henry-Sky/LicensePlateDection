import torch


def check_gpu():
    # 检查是否有可用的GPU
    if torch.cuda.is_available():
        device = torch.device(0)
        print("GPU is available. Device:", torch.cuda.get_device_name(device))

        # 创建一个简单的张量并在GPU上进行运算
        x = torch.rand(3, 3).to(device)
        y = torch.rand(3, 3).to(device)
        z = x + y
        print("Tensor operations on GPU are successful. Result:\n", z)
    else:
        print("GPU is not available. Using CPU instead.")
        device = torch.device("cpu")

        # 创建一个简单的张量并在CPU上进行运算
        x = torch.rand(3, 3).to(device)
        y = torch.rand(3, 3).to(device)
        z = x + y
        print("Tensor operations on CPU are successful. Result:\n", z)


if __name__ == '__main__':
    print(torch.cuda.is_available())
