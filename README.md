# Traffic Signal Optimization using SUMO and Q-Learning

## Objective
Develop a traffic signal optimization system capable of reducing congestion and vehicle waiting time at a four-way intersection.

## Technologies Used
- Python
- SUMO
- TraCI
- NumPy
- Pandas
- Matplotlib
- Q-Learning

## Methodology

### Fixed Controller
Uses predefined signal timing irrespective of traffic conditions.

### Adaptive Controller
Adjusts traffic signals based on queue lengths.

### Dynamic Controller
Dynamically extends signal duration according to congestion.

### Q-Learning Controller

State:
- North-South queue length
- East-West queue length

Actions:
- Action 0 → North-South green
- Action 1 → East-West green

Reward:
- Negative total queue length

```python
reward = -(ns + ew)