import numpy as np
import random


def euclidean(point, data):
    return np.sqrt(np.sum((point - data) ** 2, axis=1))

class kmeans:
    def __init__(self, n_clusters=8, max_iter=1000):
        self.n_clusters = n_clusters
        self.max_iter = max_iter

    def fit(self, data):
        self.centroids = [random.choice(data)]
        for _ in range(self.n_clusters-1):
            
            dists = np.sum([euclidean(centroid, data) for centroid in self.centroids], axis=0)
            
            dists /= np.sum(dists)
            
            new_centroid_idx, = np.random.choice(range(len(data)), size=1, p=dists)
            self.centroids += [data[new_centroid_idx]]

        iteration = 0
        prev_centroids = None

        while np.not_equal(self.centroids, prev_centroids).any() and iteration < self.max_iter:
            sorted_points = [[] for _ in range(self.n_clusters)]
            for x in data:
                dists = euclidean(x, self.centroids)
                centroid_idx = np.argmin(dists)
                sorted_points[centroid_idx].append(x)
            prev_centroids = self.centroids
            self.centroids = [np.mean(cluster, axis=0) for cluster in sorted_points]
            for i, centroid in enumerate(self.centroids):
                if np.isnan(centroid).any(): 
                    self.centroids[i] = prev_centroids[i]
            iteration += 1

    def evaluate(self, X):
        centroids = []
        centroid_idxs = []
        for x in X:
            dists = euclidean(x, self.centroids)
            centroid_idx = np.argmin(dists)
            centroids.append(self.centroids[centroid_idx])
            centroid_idxs.append(centroid_idx)
        return centroids, centroid_idxs