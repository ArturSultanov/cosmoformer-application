import os
import requests

ALLOWED_LABELS: set = ("Barred Spiral", 
                       "Edge On Disk", 
                       "Featured Without Bar Or Spiral", 
                       "Irregular", "Smooth Cigar", 
                       "Smooth Inbetween", 
                       "Smooth Round", 
                       "Unbarred Spiral")

backend_url:str = "http://localhost:8000"

def test_inference_for_all_images():
    images_folder = "../images"

    for filename in os.listdir(images_folder):

        image_path = os.path.join(images_folder, filename)
        with open(image_path, "rb") as image_file:
            files = {"file": (filename, image_file, "image/jpeg")}
            response = requests.post(backend_url + "/inference", files=files)

        assert response.status_code == 200, f"Status code for {filename}: {response.status_code}"

        data = response.json()
        assert "predicted_class" in data, f"Response for {filename} must have key 'predicted_class'"

        predicted_label = data["predicted_class"]
        assert predicted_label in ALLOWED_LABELS, (
            f"Predicted label '{predicted_label}' for {filename} is not in: {ALLOWED_LABELS}"
        )
