import torch
from transformers import AutoModelForCausalLM
from janus.models import MultiModalityCausalLM, VLChatProcessor
from janus.utils.io import load_pil_images

# Specify the path to the model
model_path = "deepseek-ai/Janus-1.3B"

# Load the processor (no tokenizer)
vl_chat_processor: VLChatProcessor = VLChatProcessor.from_pretrained(
    model_path,
    use_flash_attention_2=False  # Ensure FlashAttention2 is disabled
)

# Load the model and configure for CPU usage
vl_gpt: MultiModalityCausalLM = AutoModelForCausalLM.from_pretrained(
    model_path, 
    trust_remote_code=True
)
vl_gpt = vl_gpt.to(torch.float32).eval()  # Use float32 for CPU

# Define the conversation
conversation = [
    {
        "role": "User",
        "content": "<image_placeholder>\nConvert the formula into latex code.",
        "images": ["images/equation.png"],
    },
    {"role": "Assistant", "content": ""},
]

# Load images and prepare inputs
pil_images = load_pil_images(conversation)
prepare_inputs = vl_chat_processor(
    conversations=conversation, 
    images=pil_images, 
    force_batchify=True
).to(vl_gpt.device)  # Ensure inputs are on the same device as the model

# Run image encoder to get the image embeddings
inputs_embeds = vl_gpt.prepare_inputs_embeds(**prepare_inputs)

# Run the model to get the response using embeddings directly
outputs = vl_gpt.language_model.generate(
    inputs_embeds=inputs_embeds,
    attention_mask=prepare_inputs.attention_mask,
    max_new_tokens=512,
    do_sample=False,
    use_cache=True,
)

# Directly print the raw model output (no decoding)
print(f"Raw output tensor: {outputs}")




#__________________________python test34.py