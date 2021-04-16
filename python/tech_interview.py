#estimate pi, given random points (0,1)
import random


def estimate_pi(n):
  num_points_circle = 0
  num_points_total = 0
  for _ in range(n):
    x = random.uniform(0,1)
    y = random.uniform(0,1)
    distance = x**2 + y**2
    if distance <= 1:
      num_points_circle += 1
    num_points_total += 1 
  return 4 * num_points_circle/num_points_total

n = int(input("Type the number of points:"))
result = estimate_pi(n)
print(result)