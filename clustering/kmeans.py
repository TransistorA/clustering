from collections import defaultdict
from math import inf
import random
import csv


def point_avg(points):
    """
    Accepts a list of points, each with the same number of dimensions.
    (points can have more dimensions than 2)
    
    Returns a new point which is the center of all the points.
    """
    number = len(points)
    dimension = len(points[0])
    center = []

    for i in range(dimension):
        value = 0
        for j in range(number):
            value += points[j][i]
        value /= number
        center.append(value)

    return center


def update_centers(data_set, assignments):
    """
    Accepts a dataset and a list of assignments; the indexes 
    of both lists correspond to each other.
    Compute the center for each of the assigned groups.
    Return `k` centers in a list
    """
    clusters = {}
    for point, assignment in zip(data_set, assignments):
        if assignment not in clusters.keys():
            clusters[assignment] = []
        clusters[assignment].append(point)

    centers = []
    for key in clusters.keys():
        centers.append(point_avg(clusters[key]))

    return centers
 

def assign_points(data_points, centers):
    """
    """
    assignments = []
    for point in data_points:
        shortest = inf  # positive infinity
        shortest_index = 0
        for i in range(len(centers)):
            val = distance(point, centers[i])
            if val < shortest:
                shortest = val
                shortest_index = i
        assignments.append(shortest_index)
    return assignments


def distance(a, b):
    """
    Returns the Euclidean distance between a and b
    """
    assert len(a) == len(b)
    
    dis = 0
    for i in range(len(a)):
        dis += (a[i]-b[i])**2
        
    return dis**(1/2)


def generate_k(data_set, k):
    """
    Given `data_set`, which is an array of arrays,
    return a random set of k points from the data_set
    """
    return random.sample(data_set, k)


def get_list_from_dataset_file(dataset_file):
    data = []
    file =  open(dataset_file, "r")
    reader = csv.reader(file)
    for line in reader:
        data.append([int(i) for i in line])
    return data


def cost_function(clustering):
    cost = 0
    for key, points in clustering.items():
        center = point_avg(points)
        for point in points:
            cost += distance(center, point)
    return cost


def k_means(dataset_file, k):
    dataset = get_list_from_dataset_file(dataset_file)
    k_points = generate_k(dataset, k)
    assignments = assign_points(dataset, k_points)
    old_assignments = None
    while assignments != old_assignments:
        new_centers = update_centers(dataset, assignments)
        old_assignments = assignments
        assignments = assign_points(dataset, new_centers)
    clustering = defaultdict(list)
    for assignment, point in zip(assignments, dataset):
        clustering[assignment].append(point)
    return clustering

