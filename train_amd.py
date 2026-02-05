import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
import os

# -------------------
# Config
# -------------------
DATA_DIR = "amd_dataset"
BATCH_SIZE = 16
EPOCHS = 6
LR = 1e-4
VAL_SPLIT = 0.2  # 20% for validation
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("🖥️ Using device:", DEVICE)

# -------------------
# Transforms
# -------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# -------------------
# Dataset
# -------------------
full_dataset = datasets.ImageFolder(root=DATA_DIR, transform=transform)
dataset_size = len(full_dataset)
val_size = int(dataset_size * VAL_SPLIT)
train_size = dataset_size - val_size

train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE)

print("Classes:", full_dataset.classes)  # ['AMD', 'normal']
print(f"Total images: {dataset_size}, Train: {train_size}, Val: {val_size}")

# -------------------
# Model
# -------------------
model = models.resnet50(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, 2)  # binary classification
model = model.to(DEVICE)

# -------------------
# Training setup
# -------------------
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LR)

# -------------------
# Training loop with batch updates
# -------------------
for epoch in range(EPOCHS):
    model.train()
    running_loss = 0

    for i, (images, labels) in enumerate(train_loader, 1):
        images = images.to(DEVICE)
        labels = labels.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

        # Print progress every 5 batches
        if i % 5 == 0 or i == len(train_loader):
            print(f"Epoch [{epoch+1}/{EPOCHS}] Batch [{i}/{len(train_loader)}] - Loss: {loss.item():.4f}")

    avg_loss = running_loss / len(train_loader)

    # Validation
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in val_loader:
            images = images.to(DEVICE)
            labels = labels.to(DEVICE)

            outputs = model(images)
            preds = torch.argmax(outputs, dim=1)

            correct += (preds == labels).sum().item()
            total += labels.size(0)

    acc = 100 * correct / total

    print(f"Epoch [{epoch+1}/{EPOCHS}] - Avg Loss: {avg_loss:.4f} - Val Acc: {acc:.2f}%\n")

# -------------------
# Save model
# -------------------
torch.save(model.state_dict(), "amd_model.pth")
print("✅ Training complete. Saved as amd_model.pth")
