# 🚀 Projectile Motion Physics Game

An interactive educational game that teaches **projectile motion physics** through gamified challenges and real-time simulations.

## 📚 Physics Concepts Covered

### Core Topics
- **Projectile Motion** - Motion of objects under gravity with initial velocity and angle
- **Kinematics** - Position, velocity, and acceleration calculations
- **Vector Decomposition** - Breaking velocity into horizontal (vₓ) and vertical (vᵧ) components
- **Kinematic Equations** - Using equations of motion to solve physics problems

### Key Formulas Used

#### Maximum Height
```
H = h₀ + (v₀ₓ sin θ)² / (2g)
```
- `h₀` = initial height
- `v₀` = initial velocity
- `θ` = launch angle
- `g` = 9.81 m/s²

#### Horizontal Range
```
R = v₀ cos θ × t
```
Where `t` is the total time of flight

#### Total Time of Flight
```
0 = h₀ + v₀ sin θ × t - ½g × t²
```
Solved using quadratic formula

#### Impact Velocity
```
v = √(vₓ² + vᵧ²)
```
- `vₓ` = horizontal velocity (constant)
- `vᵧ` = vertical velocity (changes with time)

## 🎮 Game Levels

| Level | Scenario | Physics Concepts | Questions |
|-------|----------|-----------------|-----------|
| **1** | Horizontal launch (h₀=0) | Basic projectile motion | Max Height, Range, Time |
| **2** | Launch with height | Initial height effects | Range, Time, Impact Velocity, Max Height |
| **3** | Horizontal drop (θ=0°) | Free fall dynamics | Total Time of Flight |
| **4** | Horizontal drop higher | Free fall from altitude | Range, Impact Velocity |
| **5** | Downward angle (θ<0°) | Negative angle trajectory | Range, Time, Impact Velocity |

## 🧮 Physics Engine

The simulation calculates all projectile motion parameters:

```python
def calculate_projectile_motion(v0, angle, h0=0, hf=0):
    """
    Calculate physics for projectile motion
    
    Parameters:
    - v0: Initial velocity (m/s)
    - angle: Launch angle (degrees)
    - h0: Initial height (m)
    - hf: Final height (m, default 0)
    
    Returns: Dictionary with all calculated values
    """
```

## 📊 Calculated Values

- ✅ Maximum height reached
- ✅ Horizontal distance traveled (range)
- ✅ Total flight time
- ✅ Impact velocity (final speed)
- ✅ Velocity components (vₓ, vᵧ)
- ✅ Time to maximum height
- ✅ Trajectory points for visualization

## 🔬 Real-world Applications

This game demonstrates physics used in:
- 🏹 Ballistics and weapons systems
- ⚽ Sports physics (basketball, football, golf)
- 🛸 Space missions and orbital mechanics
- 🎯 Military targeting systems
- 🌍 Environmental projectile modeling

## 🛠️ Technical Features

- **Real-time Simulation** - Canvas-based trajectory animation
- **Precision Calculations** - Accurate physics equations
- **Visual Feedback** - Animated projectile path and results
- **Progressive Difficulty** - 5 levels with increasing complexity
- **Answer Validation** - Rounded integer comparisons (±1 margin)

## 📖 How to Play

1. **Read the Problem** - Understand the initial conditions
2. **Calculate** - Use projectile motion formulas to solve
3. **Submit** - Enter your answer as a rounded integer
4. **Get Feedback** - Hints if incorrect, advance if correct
5. **Progress** - Complete all 5 levels to win

## ✨ Learning Outcomes

After completing this game, students will understand:
- ✓ How gravity affects projectile motion
- ✓ Why angle and height matter in trajectories
- ✓ How to decompose velocity vectors
- ✓ When and how to apply kinematic equations
- ✓ Real-world physics problem-solving

---

**Physics Level**: High School / Early University (Ages 14-18)
**Difficulty**: Progressive (Easy → Expert)
