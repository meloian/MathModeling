# V - 16

import random
import matplotlib.pyplot as plt

# Define the vertices of the polygon
polygon = [
    (0, 0),
    (0, 4),
    (1, 4),
    (3, 2),
    (4, 2),
    (4, 1),
    (2, 1),
    (2, 0)
]

def is_point_inside_polygon(x, y, polygon):
    # check if the point (x, y) is inside the polygon using the Ray-Casting algorithm
    num = len(polygon)
    j = num - 1  # connect last vertex to the first
    c = False
    for i in range(num):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-10) + xi):
            c = not c  # toggle crossing state
        j = i
    return c

def calculate_polygon_area(polygon):
    # calculate the polygon area using the Shoelace theorem
    area = 0.0
    n = len(polygon)
    for i in range(n):
        xi, yi = polygon[i]
        xi1, yi1 = polygon[(i + 1) % n]  # next vertex
        area += xi * yi1 - xi1 * yi
    return abs(area) / 2.0

def monte_carlo_integration(polygon, N, visualize=False):
    # estimate the polygon area using Monte Carlo method
    min_x = min(point[0] for point in polygon)
    max_x = max(point[0] for point in polygon)
    min_y = min(point[1] for point in polygon)
    max_y = max(point[1] for point in polygon)

    hits = 0  # count points inside the polygon
    inside_points = []  # for visualization
    outside_points = []

    for _ in range(N):
        # generate a random point
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)
        if is_point_inside_polygon(x, y, polygon):
            hits += 1
            inside_points.append((x, y))
        else:
            outside_points.append((x, y))

    rectangle_area = (max_x - min_x) * (max_y - min_y)
    estimated_area = (hits / N) * rectangle_area

    if visualize:
        visualize_polygon(polygon, inside_points, outside_points)

    return estimated_area

def visualize_polygon(polygon, inside_points, outside_points):
    # visualize the polygon and the points
    plt.figure(figsize=(6, 6))
    
    polygon_x, polygon_y = zip(*polygon)
    plt.fill(polygon_x, polygon_y, 'gray', alpha=0.3, label='Polygon')

    # plot inside points (green) and outside points (red)
    if inside_points:
        inside_x, inside_y = zip(*inside_points)
        plt.scatter(inside_x, inside_y, color='green', s=2, label='Inside Polygon')

    if outside_points:
        outside_x, outside_y = zip(*outside_points)
        plt.scatter(outside_x, outside_y, color='red', s=2, label='Outside Polygon')

    plt.xlim(min(polygon_x) - 0.5, max(polygon_x) + 0.5)
    plt.ylim(min(polygon_y) - 0.5, max(polygon_y) + 0.5)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.legend()
    plt.title("Visualization of Polygon and Random Points")
    plt.show()

def main():
    N = int(input("Enter the number of iterations N: "))

    # estimate the area using Monte Carlo method
    estimated_area = monte_carlo_integration(polygon, N, visualize=True)

    # calculate the actual area
    actual_area = calculate_polygon_area(polygon)

    print(f"Estimated Area (Monte Carlo): {estimated_area}")
    print(f"Actual Area: {actual_area}")
    print(f"Error: {abs(estimated_area - actual_area)}")

if __name__ == "__main__":
    main() 
    
# result: N = 3000

"""
Enter the number of iterations N: 3000
Estimated Area (Monte Carlo): 9.92
Actual Area: 10.0
Error: 0.08000000000000007

""" 
