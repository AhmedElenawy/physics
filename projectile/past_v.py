from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProjectileMotionForm, PracticeAnswerForm
from .calc import calculate_projectile_motion
import random
import json

def index(request):
    """Main Game Menu"""
    level = request.session.get('level', 1)
    return render(request, 'projectile/index.html', {'level': level})

def reset_progress(request):
    """Resets the game to Level 1 and clears active problem"""
    request.session['level'] = 1
    # Clear any active problem data so a new one is generated
    if 'practice_params' in request.session:
        del request.session['practice_params']
    return redirect('projectile:index')

def reload_question(request):
    """Clears the current question from session and reloads practice view"""
    # Delete the current problem from session so a new one is generated
    if 'practice_params' in request.session:
        del request.session['practice_params']
    return redirect('projectile:practice')

def projectile_simulation(request):
    simulation_data = None
    physics_results = None
    
    if request.method == 'POST':
        form = ProjectileMotionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            v0 = float(data['initial_velocity'])
            angle = float(data['angle'])
            h0 = float(data['initial_height'] or 0)
            # hf = float(data['final_height'] or 0)
            
            physics_results = calculate_projectile_motion(v0, angle, h0)
            simulation_data = json.dumps(physics_results)
    else:
        form = ProjectileMotionForm()

    context = {
        'form': form,
        'simulation_data': simulation_data,
        'physics_results': physics_results,
    }
    return render(request, 'projectile/simulation.html', context)

def practice(request):
    # Get current level from session, default to 1
    level = request.session.get('level', 1)
    
    # Win State
    if level > 5:
        return render(request, 'projectile/victory.html')

    feedback = None
    
    # Check if a problem is already active in the session
    params = request.session.get('practice_params')

    if request.method == 'POST':
        form = PracticeAnswerForm(request.POST)
        
        # Ensure we have active parameters to check against
        if form.is_valid() and params:
            user_ans = form.cleaned_data['answer']
            target_solution = params['target_solution']
            
            # ROUNDING CHECK: User must match the rounded integer value
            correct_rounded = int(round(target_solution))
            
            if user_ans == correct_rounded:
                # Correct Answer Logic
                request.session['level'] = level + 1
                messages.success(request, f"Correct! The exact answer was {target_solution:.2f}, rounded to {correct_rounded}.")
                
                # CLEAR the current problem from session so a new one is generated next time
                if 'practice_params' in request.session:
                    del request.session['practice_params']
                
                return redirect('projectile:practice')
            else:
                # Wrong Answer Logic
                # We do NOT clear 'practice_params', so the user sees the exact same numbers again
                feedback = f"Incorrect. You entered {user_ans}. Try calculating again."
        elif not params:
            messages.error(request, "Session expired. Generating new problem.")
    else:
        form = PracticeAnswerForm()

    # --- PROBLEM GENERATION LOGIC ---
    # Only generate if 'practice_params' is missing (Fresh start or just leveled up)
    if 'practice_params' not in request.session:
        v0, angle, h0, hf = 0, 0, 0,0
        
        # Level 1: Ground-to-Ground (h=0)
        if level == 1:
            v0 = random.randint(20, 80)
            angle = random.randint(30, 75)
            h0 = 0
            
        # Level 2: Cliff Launch Upwards (h!=0, h < h_max, v!=0)
        elif level == 2:
            v0 = random.randint(20, 60)
            angle = random.randint(20, 60) # Positive angle = launch up
            h0 = random.randint(20, 100)
            
        #
        elif level == 3:
            v0 = random.randint(15, 50) # Epsilon for math stability
            angle = 0
            h0 = random.randint(50, 150)
            
            
        # Level 4: Horizontal Launch (Start from h_max, so angle=0)
        elif level == 4:
            v0 = random.randint(15, 50)
            angle = 0 
            h0 = random.randint(30, 100)
            
        # Level 5: Downward Throw (Start from h_max, angle < 0)
        elif level == 5:
            v0 = random.randint(20, 60)
            angle = random.randint(-60, -20) # Negative angle = downwards
            h0 = random.randint(50, 150)

        # Calculate Truth
        results = calculate_projectile_motion(v0, angle, h0=h0, hf=hf)
        
        # Select Question Type
        possible_questions = []
        if level == 1:
            possible_questions = ['max_height', 'range', 'total_time']
        elif level == 3: # Drop
            possible_questions = ['total_time']
        elif level == 4: # Horizontal Launch
            possible_questions = ['range', 'impact_velocity']
        elif level == 5: # Horizontal Launch
            possible_questions = ['range', 'total_time', 'impact_velocity']
        elif level == 2:
            possible_questions = ['range', 'total_time', 'impact_velocity', 'max_height']

        q_type = random.choice(possible_questions)
        
        question_text = ""
        target_val = 0
        unit = ""

        if q_type == 'max_height':
            question_text = "Calculate the Maximum Height (from ground)."
            target_val = results['max_height']
            unit = "m"
        elif q_type == 'range':
            question_text = "Calculate the Horizontal Distance (Range)."
            target_val = results['range']
            unit = "m"
        elif q_type == 'total_time':
            question_text = "Calculate the Total Time of Flight."
            target_val = results['total_time']
            unit = "s"
        elif q_type == 'impact_velocity':
            question_text = "Calculate the Final Velocity (Impact Speed)."
            target_val = results['impact_velocity']
            unit = "m/s"

        # SAVE TO SESSION
        # This persists the problem until the user solves it
        request.session['practice_params'] = {
            'v0': v0,
            'angle': angle,
            'h0': h0,
            'question': question_text,
            'unit': unit,
            'target_solution': target_val,
            'sim_data_json': json.dumps(results)
        }

    # Retrieve parameters from session (whether new or existing)
    params = request.session['practice_params']
    
    context = {
        'form': form,
        'level': level,
        'v0': params['v0'],
        'angle': params['angle'],
        'h0': params['h0'],
        'question': params['question'],
        'unit': params['unit'],
        'feedback': feedback,
        'sim_data_json': params['sim_data_json'],
    }
    
    return render(request, 'projectile/practice.html', context)