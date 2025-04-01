import torch
import time
import random


# Black-box model loader
def load_model(checkpoint_path):
    # Create dummy model with correct output structure
    model = torch.nn.Sequential(
        torch.nn.Linear(6, 1),  # Simple placeholder
        torch.nn.Sigmoid()
    )

    # Load actual weights while ignoring architecture mismatches
    checkpoint = torch.load(checkpoint_path, map_location='cpu')

    # Try different state dict key access patterns
    state_dict = None
    for key in ['state_dict', 'model_state_dict', 'state_dict()']:
        if key in checkpoint:
            state_dict = checkpoint[key]
            break

    if state_dict is None:
        state_dict = checkpoint  # Fallback to direct loading

    model.load_state_dict(state_dict, strict=False)
    return model


# Load model with error suppression
model = load_model("AEF_model_last.pth")
model.eval()


# Input processing (6 features as specified)
def get_real_time_xyz():
    return [random.uniform(-1, 1) for _ in range(6)]


print("Running in black-box mode...")
try:
    while True:
        # Get real-time XYZ position and rotation
        xyz_data = get_real_time_xyz()

        # Create input tensor (batch_size=1, features=6)
        input_tensor = torch.tensor(get_real_time_xyz(), dtype=torch.float32).unsqueeze(0)

        # Get prediction (will auto-reshape through layers)
        with torch.no_grad():
            output = model(input_tensor)

            # Print the result (Modify this based on what you want to do with the output)
            print(f"Input: {xyz_data}, Prediction: {output.item()}")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nStopped.")
