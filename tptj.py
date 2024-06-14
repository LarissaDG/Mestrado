import numpy as np
import matplotlib.pyplot as plt

# Number of agents, artworks, and features
num_agents = 5
num_artworks = 10
num_features = 5

# Generate random feature values for artworks
#artworks = np.random.rand(num_artworks, num_features)

# Generate random feature values for artworks using Gaussian distribution
artworks = np.random.normal(loc=0.5, scale=0.2, size=(num_artworks, num_features))


"""class Agent:
    def __init__(self, num_features, num_artworks):
        self.preferences = np.random.rand(num_features)
        self.evaluations = np.zeros(num_artworks)
        
    def evaluate_artworks(self, artworks):
        self.evaluations = np.dot(artworks, self.preferences)
    
    def adjust_evaluations(self, rankings):
        for i in range(len(self.evaluations)):
            average_ranking = np.mean([rankings[j][i] for j in range(len(rankings))])
            self.evaluations[i] = (self.evaluations[i] + average_ranking) / 2"""

class Agent:
    def __init__(self, num_features, num_artworks, learning_rate=0.01):
        self.preferences = np.random.rand(num_features)
        self.evaluations = np.zeros(num_artworks)
        self.payoffs = np.zeros(num_artworks)
        self.learning_rate = learning_rate

    def evaluate_artworks(self, artworks):
        self.evaluations = np.dot(artworks, self.preferences)

    def calculate_payoffs(self, rankings):
        for i in range(len(self.payoffs)):
            average_ranking = np.mean(rankings[:, i])
            self.payoffs[i] = self.evaluations[i] - average_ranking

    def adjust_preferences(self, artworks):
        gradients = np.dot(self.payoffs, artworks)
        self.preferences += self.learning_rate * gradients
        self.preferences = np.clip(self.preferences, 0, 1)  # Manter as preferências no intervalo [0, 1]


# Initialize agents
agents = [Agent(num_features, num_artworks) for _ in range(num_agents)]

# Initial evaluation
for agent in agents:
    agent.evaluate_artworks(artworks)

# Collect initial rankings
initial_rankings = np.array([agent.evaluations for agent in agents])
initial_rankings_mean = np.mean(initial_rankings, axis=0)
initial_sorted_indices = np.argsort(initial_rankings_mean)[::-1]

print("Initial Artwork Rankings:")
for idx in initial_sorted_indices:
    print(f"Artwork {idx + 1}: Score {initial_rankings_mean[idx]:.2f}")

# Plot the initial rankings
plt.figure(figsize=(10, 5))
plt.bar(range(1, num_artworks + 1), initial_rankings_mean[initial_sorted_indices])
plt.xlabel("Artwork")
plt.ylabel("Initial Score")
plt.title("Initial Artwork Rankings")
plt.show()

"""# Iterative adjustment process
iterations = 100
for iteration in range(iterations):
    rankings = np.array([agent.evaluations for agent in agents])
    for agent in agents:
        agent.adjust_evaluations(rankings)"""

# Processo iterativo de ajuste
#Comparação interpessoal de payoffs? Mas isso vale para jogos como Tit for tat? Ou colaborativos?
iterations = 100
for iteration in range(iterations):
    rankings = np.array([agent.evaluations for agent in agents])
    for agent in agents:
        agent.calculate_payoffs(rankings)
    for agent in agents:
        agent.adjust_preferences(artworks)
    for agent in agents:
        agent.evaluate_artworks(artworks)

# Display final rankings
final_rankings = np.mean(rankings, axis=0)
sorted_indices = np.argsort(final_rankings)[::-1]

print("Final Artwork Rankings:")
for idx in sorted_indices:
    print(f"Artwork {idx + 1}: Score {final_rankings[idx]:.2f}")

# Plot the final rankings
plt.bar(range(1, num_artworks + 1), final_rankings[sorted_indices])
plt.xlabel("Artwork")
plt.ylabel("Final Score")
plt.title("Final Artwork Rankings")
plt.show()
