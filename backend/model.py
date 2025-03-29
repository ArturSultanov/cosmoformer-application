import torch
from PIL import Image
import torchvision.transforms.v2 as v2

LABELS = {
    0: "barred_spiral",
    1: "edge_on_disk",
    2: "featured_without_bar_or_spiral",
    3: "irregular",
    4: "smooth_cigar",
    5: "smooth_inbetween",
    6: "smooth_round",
    7: "unbarred_spiral"
}


class Cosmoformer:
    """
    Cosmoformer model.
    """

    _NAME = "Cosmoformer"

    def __init__(self, model_path: str = "model/cosmoformer_traced_cpu.pt"):
        """
        Initialize the Cosmoformer model.
        """
        self.model = torch.jit.load(model_path, map_location="cpu")
        self.model.eval()

        self.transform = v2.Compose([
            v2.Resize((224, 224)),
            v2.Compose([v2.ToImage(), v2.ToDtype(torch.float32, scale=True)])  # v2.ToTensor()
        ])

    def get_name(self):
        return Cosmoformer._NAME

    def predict(self, image: Image.Image) -> str:
        """
        Perform a forward pass on a Image.
        Return the predicted galaxy class label.
        """

        tensor = self.transform(image)  # shape: [3, 224, 224]
        tensor = tensor.unsqueeze(0)    # shape: [1, 3, 224, 224]

        with torch.no_grad():
            output = self.model(tensor)
            predicted_idx = torch.argmax(output, dim=1).item()

        return LABELS.get(predicted_idx, "unknown")