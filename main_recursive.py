
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

def attention_kernel(x_i, x):
    return np.exp(-np.abs(x_i - x)**2)

def recursive_query(G_field, x, iterations=3):
    result = G_field.copy()
    for _ in range(iterations):
        new_result = []
        for i in range(len(x)):
            weights = attention_kernel(x[i], x)
            new_result.append(np.tanh(np.sum(weights * result)))
        result = np.array(new_result)
    return result

if __name__ == "__main__":
    x = np.linspace(0, 10, 500)
    t = 1.0

    G = geo_sentient_field(x, t)
    R = recursive_query(G, x, iterations=5)

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(x, G, label="GeoSentient Field G(x, t)", color='green')
    plt.title("Original GeoSentient Field")
    plt.xlabel("Position x")
    plt.ylabel("Field Intensity")
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(x, R, label="Recursive Response R(x)", color='blue')
    plt.title("Recursive Environmental Feedback")
    plt.xlabel("Position x")
    plt.ylabel("Response Intensity")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
