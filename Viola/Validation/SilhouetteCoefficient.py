from sklearn.metrics import silhouette_score, silhouette_samples
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


def silhouette_score_mean_validation(distance_matrix, clusters):
    return silhouette_score(X=distance_matrix, labels=clusters, metric='precomputed')


def silhouette_score_samples_validation(distance_matrix, clusters):
    return silhouette_samples(X=distance_matrix, labels=clusters, metric='precomputed')


def plot_silhouette_analysis(values, distance_matrix, n_clusters, clusters):
    ax1 = plt.gca()

    # silhouette coefficient can range from -1, 1
    ax1.set_xlim([-1, 1])
    # insert blank space between silhouette plots of individual clusters
    ax1.set_ylim([0, len(values) + (n_clusters + 1) * 10])

    silhouette_avg = silhouette_score_mean_validation(distance_matrix, clusters)
    print("For n_clusters =", n_clusters,
          "The average silhouette_score is :", silhouette_avg)

    # Compute the silhouette scores for each sample
    sample_silhouette_values = silhouette_score_samples_validation(distance_matrix, clusters)

    y_lower = 10
    for i in range(n_clusters):
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        ith_cluster_silhouette_values = \
            sample_silhouette_values[clusters == i]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cm.nipy_spectral(float(i) / n_clusters)
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)

        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

        # Compute the new y_lower for next cluster
        y_lower = y_upper + 10  # 10 for the 0 samples

    ax1.set_ylim([0, y_lower])

    #ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_xlabel("Silhouette coefficient values")
    ax1.set_ylabel("Cluster label")

    ax1.axvline(x=0, color='k')

    # vertical line for average silhouette score
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

    ax1.set_yticks([])  # Clear yaxis labels / ticks
    ax1.set_xticks([-1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1])

    plt.suptitle(("Silhouette analysis with n_clusters = %d" % n_clusters),
                 fontsize=14, fontweight='bold')

    plt.show()
