# Sal's Shipper

premium_ground_shipping = 125
 
def ground_shipping(weight):
	if (weight <= 2):
		cost = (weight * 1.5) + 20
		return cost
	elif (weight > 2) and (weight <= 6):
		cost = (weight * 3) + 20
		return cost
	elif (weight > 6) and (weight <= 10):
		cost = (weight * 4) + 20
		return cost
	else:
		cost = (weight * 4.75) + 20
		return cost

def drone_shipping(weight):
	if (weight <= 2):
		cost = weight * 4.5
		return cost
	elif (weight > 2) and (weight <= 6):
		cost = weight * 9
		return cost
	elif (weight > 6) and (weight	<= 10):
		cost = weight * 12
		return cost
	else:
		cost = weight * 14.25
		return cost

def comparison(weight):
	ground_cost = ground_shipping(weight)
	drone_cost = drone_shipping(weight)
	if (ground_cost < drone_cost) and (ground_cost < premium_ground_shipping):
		print("Ground Shipping is the best option")
		print("Total: $"+str(ground_cost))
	elif (drone_cost < ground_cost) and (drone_cost < premium_ground_shipping):
		print("Drone Shipping is the best option")
		print("Total: $"+str(drone_cost))
	else:
		print("Premium Ground Shipping is the best option")
		print("Total: $"+str(premium_ground_shipping))

total_comparison = comparison()