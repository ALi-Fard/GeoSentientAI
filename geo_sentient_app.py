
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="GeoSentientAI", layout="wide")
st.title("🌱 GeoSentientAI – Living Field Simulation")

# Sidebar controls
st.sidebar.header("Simulation Controls")
alpha = st.sidebar.slider("α (Laplacian weight)", 0.0, 2.0, 0.7, 0.1)
beta = st.sidebar.slider("β (Fractal Harmonic weight)", 0.0, 2.0, 0.2, 0.1)
gamma = st.sidebar.slider("γ (Entropy gradient weight)", 0.0, 2.0, 0.1, 0.1)
iterations = st.sidebar.slider("Recursive Depth", 1, 10, 5)

# Core functions
def phi(x, t):
    return np.sin(x - 0.5 * t)

def fractal_harmonic(x, t):
    return np.cos(2 * x + t) + 0.5 * np.random.randn(*x.shape)

def soil_entropy(x, t):
    return np.exp(-((x - t)**2)) + 0.1 * np.random.randn(*x.shape)

def geo_sentient_field(x, t, alpha, beta, gamma):
    laplacian_phi = np.gradient(np.gradient(phi(x, t)))
    return alpha * laplacian_phi + beta * fractal_harmonic(x, t) + gamma * np.gradient(soil_entropy(x, t))

def attention_kernel(x_i, x):
    return np.exp(-np.abs(x_i - x)**2)

def recursive_query(G_field, x, iterations):
    result = G_field.copy()
    for _ in range(iterations):
        new_result = []
        for i in range(len(x)):
            weights = attention_kernel(x[i], x)
            new_result.append(np.tanh(np.sum(weights * result)))
        result = np.array(new_result)
    return result

# Generate simulation
x = np.linspace(0, 10, 500)
t = 1.0
G = geo_sentient_field(x, t, alpha, beta, gamma)
R = recursive_query(G, x, iterations)

# Plotting
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
ax1.plot(x, G, color='green', label='G(x, t)')
ax1.set_title("GeoSentient Field")
ax1.set_xlabel("Position x")
ax1.set_ylabel("Field Intensity")
ax1.grid(True)
ax1.legend()

ax2.plot(x, R, color='blue', label='R(x)')
ax2.set_title("Recursive Response")
ax2.set_xlabel("Position x")
ax2.set_ylabel("Response Intensity")
ax2.grid(True)
ax2.legend()

st.pyplot(fig)
