import numpy as np
from scipy.sparse import csr_matrix

class ALSTrainModel:
    def __init__(self, factors=10, regularization=0.1, iterations=10, alpha=0.01):
        self.factors = factors
        self.regularization = regularization
        self.iterations = iterations
        self.alpha = alpha
        self.user_factors = None
        self.item_factors = None

    def fit(self, user_item_matrix):
        user_item_sparse = csr_matrix(user_item_matrix).toarray()
        num_users, num_items = user_item_sparse.shape
        
        # Initialize user and item latent factor matrices
        self.user_factors = np.random.rand(num_users, self.factors)
        self.item_factors = np.random.rand(num_items, self.factors)

        # Alternating Least Squares optimization
        for iteration in range(self.iterations):
            if not (iteration % 200): print(f"Iteration : {iteration}/{self.iterations}")
            # Update user factors
            for u in range(num_users):
                A = self.item_factors.T @ self.item_factors + self.regularization * np.eye(self.factors)
                b = user_item_sparse[u, :] @ self.item_factors
                self.user_factors[u, :] = np.linalg.solve(A, b)

            # Update item factors
            for i in range(num_items):
                A = self.user_factors.T @ self.user_factors + self.regularization * np.eye(self.factors)
                b = user_item_sparse[:, i] @ self.user_factors
                self.item_factors[i, :] = np.linalg.solve(A, b)

    def get_predicted_matrix(self):
        # Calculate R^ (predicted user-item interaction matrix)
        return np.dot(self.user_factors, self.item_factors.T)

    def get_user_item_factors(self):
        # Return user factors (P) and item factors (Q)
        return self.user_factors, self.item_factors

    def recommend(self, user_id, num_items=3):
        user_vector = self.user_factors[user_id]
        scores = np.dot(self.item_factors, user_vector)
        item_indices = np.argsort(scores)[::-1][:num_items]
        return item_indices

    def evaluate(self, ratings):
        actual_ratings = []
        predicted_ratings = []
        for _, row in ratings.iterrows():
            user_id = row['user']
            item_id = row['item']
            actual_ratings.append(row['rating'])
            predicted_ratings.append(np.dot(self.user_factors[user_id], self.item_factors[item_id - 1]))
        rmse = np.sqrt(np.mean((np.array(actual_ratings) - np.array(predicted_ratings)) ** 2))
        return rmse