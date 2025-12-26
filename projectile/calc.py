"""
Projectile Motion Physics Calculator
=====================================
Function-based implementation for calculating projectile motion trajectories.

Physics Formulas Reference:
- Velocity Components: vx = v₀·cos(θ), vy = v₀·sin(θ)
- Position: x(t) = v₀x·t, y(t) = h₀ + v₀y·t - ½g·t²
- Maximum Height: H = h₀ + (v₀y²)/(2g)
- Flight Time: Quadratic formula from y(t) = hf
- Range: R = v₀x · t_total
"""

import numpy as np

# ============================================================================
# PHYSICS CONSTANTS
# ============================================================================
G = 9.81  # Gravitational acceleration (m/s²)


# ============================================================================
# VELOCITY COMPONENT CALCULATIONS
# ============================================================================
def calculate_velocity_components(v0, angle_deg):
    """
    Calculate horizontal and vertical velocity components.
    
    Physics Formula:
        vx = v₀ · cos(θ)  [Horizontal component - constant]
        vy = v₀ · sin(θ)  [Vertical component - changes with time]
    
    Args:
        v0: Initial velocity magnitude (m/s)
        angle_deg: Launch angle in degrees
    
    Returns:
        tuple: (v0x, v0y) velocity components in m/s
    """
    theta = np.radians(angle_deg)
    v0x = v0 * np.cos(theta)
    v0y = v0 * np.sin(theta)
    return v0x, v0y


# ============================================================================
# MAXIMUM HEIGHT CALCULATIONS
# ============================================================================
def calculate_max_height(v0y, h0):
    """
    Calculate maximum height and time to reach it.
    
    Physics Formula:
        At max height, vy = 0
        From: vy = v₀y - g·t
        Solve: t_max = v₀y / g
        
        Then: H = h₀ + v₀y·t_max - ½g·t_max²
        Simplified: H = h₀ + (v₀y²)/(2g)
    
    Args:
        v0y: Initial vertical velocity (m/s)
        h0: Initial height (m)
    
    Returns:
        tuple: (max_height, time_to_max_height) in meters and seconds
    """
    # Time to reach maximum height
    t_max_h = v0y / G
    
    # Maximum height using kinematic equation
    max_height = h0 + (v0y * t_max_h) - (0.5 * G * t_max_h ** 2)
    
    return max_height, t_max_h


# ============================================================================
# FLIGHT TIME CALCULATIONS
# ============================================================================
def calculate_flight_time(v0y, h0, hf):
    """
    Calculate total time of flight using quadratic formula.
    
    Physics Formula:
        Position equation: y(t) = h₀ + v₀y·t - ½g·t²
        At landing: hf = h₀ + v₀y·t - ½g·t²
        
        Rearrange: ½g·t² - v₀y·t - (h₀ - hf) = 0
        Standard form: at² + bt + c = 0
        where: a = ½g, b = -v₀y, c = -(h₀ - hf)
        
        Quadratic formula: t = [-b ± √(b² - 4ac)] / 2a
    
    Args:
        v0y: Initial vertical velocity (m/s)
        h0: Initial height (m)
        hf: Final height (m)
    
    Returns:
        float: Total flight time in seconds (0 if impossible)
    """
    # Quadratic equation coefficients
    a_coeff = 0.5 * G
    b_coeff = -v0y
    c_coeff = -(h0 - hf)
    
    # Calculate discriminant
    discriminant = b_coeff**2 - 4*a_coeff*c_coeff
    
    if discriminant < 0:
        # No real solution - projectile never reaches final height
        return 0
    
    # Quadratic formula
    t1 = (-b_coeff + np.sqrt(discriminant)) / (2*a_coeff)
    t2 = (-b_coeff - np.sqrt(discriminant)) / (2*a_coeff)
    
    # Take the positive, larger time (landing time, not launch time)
    total_time = max(t1, t2)
    
    return total_time


# ============================================================================
# RANGE CALCULATION
# ============================================================================
def calculate_range(v0x, total_time):
    """
    Calculate horizontal range.
    
    Physics Formula:
        R = v₀x · t
        (Horizontal velocity is constant, no acceleration in x-direction)
    
    Args:
        v0x: Horizontal velocity component (m/s)
        total_time: Total flight time (s)
    
    Returns:
        float: Horizontal range in meters
    """
    range_distance = v0x * total_time
    return range_distance


# ============================================================================
# IMPACT VELOCITY CALCULATIONS
# ============================================================================
def calculate_impact_velocity(v0x, v0y, total_time):
    """
    Calculate velocity at impact (landing).
    
    Physics Formula:
        vx(t) = v₀x  (constant)
        vy(t) = v₀y - g·t
        
        Impact velocity magnitude: v = √(vx² + vy²)
        Impact angle: θ = arctan(vy/vx)
    
    Args:
        v0x: Horizontal velocity component (m/s)
        v0y: Initial vertical velocity (m/s)
        total_time: Total flight time (s)
    
    Returns:
        tuple: (impact_velocity, impact_angle) in m/s and degrees
    """
    if total_time <= 0:
        return 0, 0
    
    # Final velocity components
    final_vx = v0x  # Horizontal velocity stays constant
    final_vy = v0y - (G * total_time)  # Vertical velocity changes
    
    # Impact velocity magnitude
    impact_velocity = np.sqrt(final_vx**2 + final_vy**2)
    
    # Impact angle
    impact_angle = np.degrees(np.arctan2(final_vy, final_vx))
    
    return impact_velocity, impact_angle


# ============================================================================
# TRAJECTORY GENERATION
# ============================================================================
def generate_trajectory_data(v0x, v0y, h0, hf, total_time, num_points=100):
    """
    Generate trajectory points for visualization.
    
    Physics Formulas:
        x(t) = v₀x · t
        y(t) = h₀ + v₀y·t - ½g·t²
        vx(t) = v₀x (constant)
        vy(t) = v₀y - g·t
        v(t) = √(vx² + vy²)
        KE = ½v² (per unit mass)
        PE = g·(y - h₀) (per unit mass)
    
    Args:
        v0x: Horizontal velocity component (m/s)
        v0y: Vertical velocity component (m/s)
        h0: Initial height (m)
        hf: Final height (m)
        total_time: Total flight time (s)
        num_points: Number of trajectory points to generate
    
    Returns:
        list: List of dictionaries containing trajectory data at each time step
    """
    if total_time <= 0:
        return []
    
    # Create time array
    times = np.linspace(0, total_time, num_points)
    
    # Calculate positions along trajectory
    x_positions = v0x * times
    y_positions = h0 + (v0y * times) - (0.5 * G * times ** 2)
    
    # Calculate velocity components along trajectory
    vx_components = np.full_like(times, v0x)  # Constant horizontal velocity
    vy_components = v0y - (G * times)  # Vertical velocity changes linearly
    
    # Total velocity magnitude at each point
    velocities = np.sqrt(vx_components**2 + vy_components**2)
    
    # Energy calculations (per unit mass, normalized)
    kinetic_energies = 0.5 * velocities**2
    potential_energies = G * (y_positions - h0)
    total_energies = kinetic_energies + potential_energies
    
    # Build trajectory data list
    trajectory = []
    for i in range(len(times)):
        # Only include points above final height
        if y_positions[i] >= hf:
            trajectory.append({
                'time': float(times[i]),
                'x': float(x_positions[i]),
                'y': float(y_positions[i]),
                'vx': float(vx_components[i]),
                'vy': float(vy_components[i]),
                'v': float(velocities[i]),
                'ke': float(kinetic_energies[i]),
                'pe': float(potential_energies[i]),
                'e_total': float(total_energies[i]),
            })
    
    return trajectory


# ============================================================================
# MAIN CALCULATION FUNCTION
# ============================================================================
def calculate_projectile_motion(v0, angle_deg, h0=0, hf=0):
    """
    Calculate complete projectile motion trajectory.
    
    This is the main function called by Django views. It orchestrates all
    the physics calculations by calling helper functions for each component.
    
    Physics Overview:
        1. Decompose initial velocity into x and y components
        2. Calculate maximum height and time to reach it
        3. Calculate total flight time (landing time)
        4. Calculate horizontal range
        5. Calculate impact velocity and angle
        6. Generate trajectory points for visualization
    
    Args:
        v0: Initial velocity magnitude (m/s)
        angle_deg: Launch angle in degrees
        h0: Initial height (m), default = 0
        hf: Final/target height (m), default = 0
    
    Returns:
        dict: Complete physics results including:
            - Initial parameters (v0, angle, h0, hf)
            - Velocity components (v0x, v0y)
            - Maximum height and time to reach it
            - Total flight time
            - Horizontal range
            - Impact velocity and angle
            - Trajectory data for graphing
    """
    # ========================================================================
    # STEP 1: Calculate velocity components
    # ========================================================================
    # Formula: vx = v₀·cos(θ), vy = v₀·sin(θ)
    v0x, v0y = calculate_velocity_components(v0, angle_deg)
    
    # ========================================================================
    # STEP 2: Calculate maximum height
    # ========================================================================
    # Formula: H = h₀ + (v₀y²)/(2g)
    max_height, t_max_h = calculate_max_height(v0y, h0)
    
    # ========================================================================
    # STEP 3: Calculate total flight time
    # ========================================================================
    # Using quadratic formula: 0.5*g*t² - v₀y*t - (h₀ - hf) = 0
    total_time = calculate_flight_time(v0y, h0, hf)
    
    # ========================================================================
    # STEP 4: Calculate horizontal range
    # ========================================================================
    # Formula: R = v₀x · t
    range_distance = calculate_range(v0x, total_time)
    
    # ========================================================================
    # STEP 5: Calculate impact velocity and angle
    # ========================================================================
    # Formula: v = √(vx² + vy²), θ = arctan(vy/vx)
    impact_velocity, impact_angle = calculate_impact_velocity(v0x, v0y, total_time)
    
    # ========================================================================
    # STEP 6: Generate trajectory data
    # ========================================================================
    # Creates 100 points along the trajectory for visualization
    trajectory = generate_trajectory_data(v0x, v0y, h0, hf, total_time)
    
    # ========================================================================
    # RETURN: Complete results dictionary
    # ========================================================================
    return {
        # Input parameters
        'initial_velocity': float(v0),
        'angle': float(angle_deg),
        'initial_height': float(h0),
        'final_height': float(hf),
        
        # Velocity components
        'v0x': float(v0x),
        'v0y': float(v0y),
        
        # Maximum height results
        'max_height': float(max_height),
        'max_height_time': float(t_max_h),
        
        # Flight results
        'total_time': float(total_time),
        'range': float(range_distance),
        
        # Impact results
        'impact_velocity': float(impact_velocity),
        'impact_angle': float(impact_angle),
        
        # Trajectory data for graphing
        'trajectory': trajectory,
    }


