
import numpy as np
import matplotlib.pyplot as plt

def phi(x, t):
    return np.sin(x - 0.5 * t)

def fractal_harmonic(x, t):
    return np.cos(2 * x + t) + 0.5 * np.random.randn(*x.shape)

def soil_entropy(x, t):
    return np.exp(-((x - t)**2)) + 0.1 * np.random.randn(*x.shape)

def geo_sentient_field(x, t, alpha=0.7, beta=0.2, gamma=0.1):
    laplacian_phi = np.gradient(np.gradient(phi(x, t)))
    return alpha * laplacian_phi + beta * fractal_harmonic(x, t) + gamma * np.gradient(soil_entropy(x, t))

if __name__ == "__main__":
    x = np.linspace(0, 10, 500)
    t = 1.0

    G = geo_sentient_field(x, t)

    plt.figure(figsize=(10, 5))
    plt.plot(x, G, label="GeoSentient Field G(x, t)", color='green')
    plt.title("GeoSentientAI — Simulated Living Field")
    plt.xlabel("Position x")
    plt.ylabel("Field Intensity")
    plt.legend()
    plt.grid(True)
    plt.show()
