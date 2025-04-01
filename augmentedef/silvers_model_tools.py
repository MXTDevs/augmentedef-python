import torch
import time
import random


def load_model_safely(path):
    checkpoint = torch.load(path, map_location='cpu')

    # Extract model weights
    if 'state_dict' in checkpoint:
        state_dict = checkpoint['state_dict']
    else:  # Fallback if structure changed
        state_dict = checkpoint

    # Create dummy model with correct input/output dimensions
    class BlackBoxModel(torch.nn.Module):
        def __init__(self):
            super().__init__()
            # Minimal architecture definition
            self.main = torch.nn.Sequential(
                torch.nn.Linear(6, 1),
                torch.nn.Sigmoid()
            )

        def forward(self, x):
            return self.main(x)

    model = BlackBoxModel()
    model.load_state_dict(state_dict, strict=False)
    return model


# 2. Load Model
model = load_model_safely("AEF_model_last.pth")
model.eval()


# 3. Input/Output Handling
def process_input(raw_data):
    """Expects 6-element list (XYZ + rotation)"""
    return torch.tensor(raw_data, dtype=torch.float32).unsqueeze(0)


def run_model(input_entry):
    model_input_data = process_input(input_entry)

    with torch.no_grad():
        model_output = model(model_input_data)

    # Interpret output (0-1 range)
    # print(f"Transition probability: {model_output.item():.2f}")

    return model_output.item()




