import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

# Устройство (GPU при наличии)
device = "cuda" if torch.cuda.is_available() else "cpu"

# Параметры
batch_size = 128
z_dim = 100     # размер вектора шума
num_epochs = 5  # для демо достаточно нескольких эпох

# Трансформации: переведём в тензор и нормализуем
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))  # стандартизируем к диапазону [-1,1]
])

# Датасет: MNIST
mnist_data = torchvision.datasets.MNIST(
    root='./data', 
    train=True, 
    transform=transform,
    download=True
)
dataloader = torch.utils.data.DataLoader(
    mnist_data,
    batch_size=batch_size,
    shuffle=True
)

class Generator(nn.Module):
    def __init__(self, z_dim=100, img_dim=28*28):
        super().__init__()
        self.gen = nn.Sequential(
            nn.Linear(z_dim, 128),
            nn.LeakyReLU(0.2),
            nn.Linear(128, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, img_dim),
            nn.Tanh(),  # выход в диапазоне [-1, 1]
        )
    def forward(self, x):
        return self.gen(x)

class Discriminator(nn.Module):
    def __init__(self, img_dim=28*28):
        super().__init__()
        self.disc = nn.Sequential(
            nn.Linear(img_dim, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 128),
            nn.LeakyReLU(0.2),
            nn.Linear(128, 1),
            nn.Sigmoid(),  # выход 0..1 (вероятность подлинности)
        )
    def forward(self, x):
        return self.disc(x)

# Создаём экземпляры сети
gen = Generator(z_dim).to(device)
disc = Discriminator().to(device)

# Функция потерь и оптимизаторы
criterion = nn.BCELoss()  # бинарная кроссэнтропия
lr = 2e-4
opt_gen = torch.optim.Adam(gen.parameters(), lr=lr)
opt_disc = torch.optim.Adam(disc.parameters(), lr=lr)

# Обучение
for epoch in range(num_epochs):
    for batch_idx, (real, _) in enumerate(dataloader):
        real = real.view(-1, 28*28).to(device)
        batch_size_curr = real.shape[0]

        # ============ Тренируем дискриминатор ============
        # Шум -> фейковые картинки
        noise = torch.randn(batch_size_curr, z_dim).to(device)
        fake = gen(noise)

        # Вычисляем вероятность для реальных и фейковых
        disc_real = disc(real).view(-1)
        disc_fake = disc(fake.detach()).view(-1)

        # Метки (1 - настоящие, 0 - фейк)
        lossD_real = criterion(disc_real, torch.ones_like(disc_real))
        lossD_fake = criterion(disc_fake, torch.zeros_like(disc_fake))
        lossD = (lossD_real + lossD_fake) / 2

        disc.zero_grad()
        lossD.backward()
        opt_disc.step()

        # ============ Тренируем генератор ============
        # Новые фейковые картинки, оцениваем дискриминатором
        output = disc(fake).view(-1)
        lossG = criterion(output, torch.ones_like(output))  # хотим, чтобы дискрим. сказал 1

        gen.zero_grad()
        lossG.backward()
        opt_gen.step()

    print(f"Epoch [{epoch+1}/{num_epochs}] | Loss D: {lossD.item():.4f}, Loss G: {lossG.item():.4f}")

# Проверка генерации: берём шум и смотрим, что получится
import matplotlib.pyplot as plt

gen.eval()
with torch.no_grad():
    sample_noise = torch.randn(16, z_dim).to(device)
    generated = gen(sample_noise).view(-1, 1, 28, 28)
    generated = (generated + 1) / 2  # денормализация из [-1,1] в [0,1]

# Отобразим 16 сгенерированных цифр
fig, axes = plt.subplots(4, 4, figsize=(6,6))
for i, ax in enumerate(axes.flatten()):
    ax.imshow(generated[i].cpu().squeeze(), cmap='gray')
    ax.axis('off')
plt.tight_layout()
plt.show()
