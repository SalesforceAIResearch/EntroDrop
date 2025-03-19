from utils.parser import get_args
from utils.utils import fix_seed, get_loaders
from transformers import AutoTokenizer
from LlamaEntroDrop import LlamaForCausalLMDrop
from MistralEntroDrop import MistralForCausalLMDrop
from transformers import LlamaForCausalLM
import torch
import transformers
from tqdm import tqdm
import torch
from torch.utils.data import DataLoader
import random
import numpy as np


def main():
    args = get_args()
    fix_seed(args.seed)
    args.device = torch.device(args.device)

    tokenizer = AutoTokenizer.from_pretrained(args.model_path)
    tokenizer.pad_token = tokenizer.eos_token

    model = LlamaForCausalLMDrop.from_pretrained(args.model_path, torch_dtype=torch.float16).to(args.device)
    model.eval()


    trainloader, validloader = get_loaders(args.dataset, nsamples=args.num_samples, seed=args.seed, seqlen=256, tokenizer=tokenizer)

    layer_seq = model.process_layers(trainloader)

    with open(args.save_path, "a") as f:
        f.write("\n")
        f.write(args.label)
        f.write(" ")
        f.write(str(layer_seq))

if __name__ == "__main__":
    main()
    
