import matplotlib.pyplot as plt
import numpy as np
import math
import random
from PIL import Image

# Função para calcular a distância entre dois pontos (antenas)
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Gerar posições aleatórias para as antenas
def generate_random_position(side_length, population_size):
    return [(random.uniform(0, side_length), random.uniform(0, side_length)) for _ in range(population_size)]

# Função para plotar as antenas e suas áreas de cobertura
def plot_antennas(positions, side_length, range_radius, show_plot=False):
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Plotar as antenas
    for i, position in enumerate(positions):
        ax.plot(position[0], position[1], marker='o', markersize=8, color='blue')
        ax.text(position[0], position[1], f'Antena {i+1}', fontsize=12, ha='center', color='white')

        # Colore o fundo de verde para contar a área não coberta pelas antenas
        ax.set_facecolor((0, 1, 0))

        # Calcular os pontos para desenhar o círculo da área de cobertura
        circle = plt.Circle(position, range_radius, color='blue', fill=True)
        ax.add_artist(circle)
        
        # Plotar área de cobertura da antena
        theta = np.linspace(0, 2*np.pi, 100)
        x_cover = position[0] + range_radius * np.cos(theta)
        y_cover = position[1] + range_radius * np.sin(theta)
        ax.plot(x_cover, y_cover, linestyle='--', color='gray', linewidth=1)

    # Configurações de exibição do gráfico
    ax.set_xlim(0, side_length)
    ax.set_ylim(0, side_length)
    ax.set_aspect('equal')
    ax.set_title('Posição das Antenas e Áreas de Cobertura')
    ax.set_xlabel('X (metros)')
    ax.set_ylabel('Y (metros)')
    ax.grid(True)

    # Salva a imagem para contar o espaço não coberto pelas antenas
    plt.savefig('./scatter_plot.png', bbox_inches='tight', pad_inches=0)

    if show_plot == True:
        plt.show()
    
    plt.close(fig)

def calculate_uncovered_area():
    with Image.open('./scatter_plot.png') as image:
        image_np = np.array(image)

    green_mask = (image_np[:, :, 0] == 0) & (image_np[:, :, 1] == 255) & (image_np[:, :, 2] == 0)
    uncovered_area = np.count_nonzero(green_mask)

    return uncovered_area