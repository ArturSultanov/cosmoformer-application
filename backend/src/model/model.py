import torch
from huggingface_hub import hf_hub_download
from PIL import Image
import torchvision.transforms.v2 as v2

label_mapping = {
    0: 'barred_spiral',
    1: 'edge_on_disk',
    2: 'featured_without_bar_or_spiral',
    3: 'irregular',
    4: 'smooth_cigar',
    5: 'smooth_inbetween',
    6: 'smooth_round',
    7: 'unbarred_spiral'
}

ts_path = hf_hub_download(
    repo_id="artursultanov/cosmoformer-model",
    filename="cosmoformer_traced_cpu.pt"
)

model = torch.jit.load(ts_path, map_location="cpu")
model.eval()

transform = v2.Compose([
    v2.Resize((224, 224)),
    v2.Compose([v2.ToImage(), v2.ToDtype(torch.float32, scale=True)])
])

image_path = "test_image.jpg"
image = Image.open(image_path).convert("RGB")

tensor = transform(image)
tensor = tensor.unsqueeze(0)

with torch.no_grad():
    output = model(tensor)
    predicted_idx = torch.argmax(output, dim=1).item()

predicted_label = label_mapping[predicted_idx]
print("Predicted class:", predicted_label)
