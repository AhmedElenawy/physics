import json
import numpy as np

# Physics Constants
G = 9.81  # m/s^2 gravitational acceleration

def calculate_projectile_motion(v0, angle_deg, h0=0, hf=0):
    """
    Calculate complete projectile motion trajectory.
    
    Args:
        v0: Initial velocity (m/s)
        angle_deg: Launch angle (degrees)
        h0: Initial height (m)
        hf: Final/target height (m)
    
    Returns:
        dict with trajectory data and physics results
    """
    # Convert angle to radians
    theta = np.radians(angle_deg)
    
    # Velocity components
    v0x = v0 * np.cos(theta)
    v0y = v0 * np.sin(theta)
    
    # Physics calculations
    # Time to reach maximum height
    # frist law
    t_max_h = v0y / G
    max_height = h0 + (v0y * t_max_h) - (0.5 * G * t_max_h ** 2)
    
    # Total flight time (when projectile hits ground level hf)
    # Using quadratic formula: 0 = h0 - hf + v0y*t - 0.5*g*t^2
    # Rearranged: 0.5*g*t^2 - v0y*t - (h0 - hf) = 0
    a_coeff = 0.5 * G
    b_coeff = -v0y
    c_coeff = -(h0 - hf)
    
    discriminant = b_coeff**2 - 4*a_coeff*c_coeff
    
    if discriminant < 0:
        # No real solution - projectile never reaches final height
        total_time = 0
    else:
        t1 = (-b_coeff + np.sqrt(discriminant)) / (2*a_coeff)
        t2 = (-b_coeff - np.sqrt(discriminant)) / (2*a_coeff)
        # Take the positive, larger time
        total_time = max(t1, t2)
    
    # Horizontal range
    range_distance = v0x * total_time
    
    # Generate trajectory points for graphing (100 points)
    num_points = 100
    if total_time > 0:
        times = np.linspace(0, total_time, num_points)
    else:
        times = np.array([0])
    
    # Position along trajectory
    x_positions = v0x * times
    y_positions = h0 + (v0y * times) - (0.5 * G * times ** 2)
    
    # Velocity components along trajectory
    vx_components = np.full_like(times, v0x)  # Constant horizontal velocity
    vy_components = v0y - (G * times)  # Vertical velocity changes
    
    # Total velocity magnitude at each point
    velocities = np.sqrt(vx_components**2 + vy_components**2)
    
    # Kinetic energy (per unit mass, normalized)
    kinetic_energies = 0.5 * velocities**2
    
    # Potential energy (per unit mass, relative to h0, normalized)
    potential_energies = G * (y_positions - h0)
    
    # Total mechanical energy (normalized per unit mass)
    total_energies = kinetic_energies + potential_energies
    
    # Build trajectory data for frontend
    trajectory = []
    for i in range(len(times)):
        if y_positions[i] >= hf:  # Only include points above final height
            trajectory.append({
                'time': float(times[i]),
                'x': float(x_positions[i]),
                'y': float(y_positions[i]),
                'vx': float(vx_components[i]),
                'vy': float(vy_components[i]),
                'v': float(velocities[i]),
                'ke': float(kinetic_energies[i]),  # Kinetic energy
                'pe': float(potential_energies[i]),  # Potential energy
                'e_total': float(total_energies[i]),  # Total mechanical energy
            })
    
    # Calculate impact velocity and angle
    if total_time > 0:
        final_vx = v0x
        final_vy = v0y - (G * total_time)
        impact_velocity = np.sqrt(final_vx**2 + final_vy**2)
        impact_angle = np.degrees(np.arctan2(final_vy, final_vx))
    else:
        impact_velocity = 0
        impact_angle = 0
    
    return {
        'initial_velocity': float(v0),
        'angle': float(angle_deg),
        'initial_height': float(h0),
        'final_height': float(hf),
        'v0x': float(v0x),
        'v0y': float(v0y),
        'max_height': float(max_height),
        'max_height_time': float(t_max_h),
        'total_time': float(total_time),
        'range': float(range_distance),
        'impact_velocity': float(impact_velocity),
        'impact_angle': float(impact_angle),
        'trajectory': trajectory,
    }
