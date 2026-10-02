"""Optional CPU generation with cached model loading; no remote API key required."""
import os
from functools import lru_cache
@lru_cache(maxsize=1)
def load_model():
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    torch.set_num_threads(min(4,os.cpu_count() or 1))
    name=os.getenv('LOCAL_LLM_MODEL','Qwen/Qwen2.5-0.5B-Instruct')
    tokenizer=AutoTokenizer.from_pretrained(name)
    model=AutoModelForCausalLM.from_pretrained(name,torch_dtype=torch.float32)
    model.eval()
    return tokenizer,model

def generate(messages):
    import torch
    tokenizer,model=load_model()
    prompt=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
    inputs=tokenizer(prompt,return_tensors='pt',truncation=True,max_length=3072)
    with torch.inference_mode():
        out=model.generate(**inputs,max_new_tokens=220,do_sample=False,pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(out[0][inputs['input_ids'].shape[1]:],skip_special_tokens=True).strip()
