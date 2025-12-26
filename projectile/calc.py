
import numpy as np

G = 9.81 


def calculate_velocity_components(v0, angle_deg):
    theta = np.radians(angle_deg)
    v0x = v0 * np.cos(theta)
    v0y = v0 * np.sin(theta)
    return v0x, v0y


def calculate_max_height(v0y, h0):
    t_max_h = v0y / G
    max_height = h0 + (v0y * t_max_h) - (0.5 * G * t_max_h ** 2)
    return max_height, t_max_h


def calculate_flight_time(v0y, h0, hf):
    a_coeff = 0.5 * G
    b_coeff = -v0y
    c_coeff = -(h0 - hf)
    
    discriminant = b_coeff**2 - 4*a_coeff*c_coeff
    
    if discriminant < 0:
        return 0
    
    t1 = (-b_coeff + np.sqrt(discriminant)) / (2*a_coeff)
    t2 = (-b_coeff - np.sqrt(discriminant)) / (2*a_coeff)
    
    total_time = max(t1, t2)
    
    return total_time


def calculate_range(v0x, total_time):
    range_distance = v0x * total_time
    return range_distance


def calculate_impact_velocity(v0x, v0y, total_time):
    if total_time <= 0:
        return 0, 0
    
    final_vx = v0x
    final_vy = v0y - (G * total_time)
    
    impact_velocity = np.sqrt(final_vx**2 + final_vy**2)
    impact_angle = np.degrees(np.arctan2(final_vy, final_vx))
    
    return impact_velocity, impact_angle


def generate_trajectory_data(v0x, v0y, h0, hf, total_time, num_points=100):
    if total_time <= 0:
        return []
    
    times = np.linspace(0, total_time, num_points)
    
    x_positions = v0x * times
    y_positions = h0 + (v0y * times) - (0.5 * G * times ** 2)
    
    vx_components = np.full_like(times, v0x)
    vy_components = v0y - (G * times)
    
    velocities = np.sqrt(vx_components**2 + vy_components**2)
    
    kinetic_energies = 0.5 * velocities**2
    potential_energies = G * (y_positions - h0)
    total_energies = kinetic_energies + potential_energies
    
    trajectory = []
    for i in range(len(times)):
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


def calculate_projectile_motion(v0, angle_deg, h0=0, hf=0):
    v0x, v0y = calculate_velocity_components(v0, angle_deg)
    
    max_height, t_max_h = calculate_max_height(v0y, h0)
    
    total_time = calculate_flight_time(v0y, h0, hf)
    
    range_distance = calculate_range(v0x, total_time)
    
    impact_velocity, impact_angle = calculate_impact_velocity(v0x, v0y, total_time)
    
    trajectory = generate_trajectory_data(v0x, v0y, h0, hf, total_time)
    
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


