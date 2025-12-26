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

def reload_last_level(request):
    """Reloads the previous level with different questions"""
    current_level = request.session.get('level', 1)
    if current_level > 1:
        # Go back one level
        request.session['level'] = current_level - 1
        # Clear the current problem so new one generates
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

def get_hint_for_question(question_type, v0, angle, h0):
    """Generate contextual hints for each question type"""
    hints = {
        'max_height': (
            f"💡 Hint: Use the formula H = h₀ + (v₀y²)/(2g). "
            f"First decompose velocity: v₀y = {v0} × sin({angle}°). "
            f"Then apply the maximum height formula with g = 9.81 m/s²."
        ),
        'range': (
            f"💡 Hint: Calculate horizontal velocity v₀x = {v0} × cos({angle}°). "
            f"Then multiply by total flight time. Use quadratic formula to find time when y = 0."
        ),
        'total_time': (
            f"💡 Hint: Use the quadratic formula with vertical motion: h = h₀ + v₀y·t - ½g·t². "
            f"Set h = 0 (ground level) and solve for t. Your h₀ = {h0}m."
        ),
        'impact_velocity': (
            f"💡 Hint: Find final velocity components at landing. "
            f"vx stays constant = v₀ × cos({angle}°). "
            f"vy changes: v₀y - g·t. Use Pythagorean theorem: v = √(vx² + vy²)."
        ),
    }
    return hints.get(question_type, "💡 Hint: Review the projectile motion formulas.")


def practice(request):
    # Get current level from session, default to 1
    level = request.session.get('level', 1)
    
    # Win State
    if level > 5:
        return render(request, 'projectile/victory.html')

    feedback_list = []  # List of feedback dictionaries for each question
    
    # Check if a problem is already active in the session
    params = request.session.get('practice_params')

    if request.method == 'POST':
        # Ensure we have active parameters to check against
        if params:
            # Create form with questions data
            form = PracticeAnswerForm(request.POST, questions_data=params['questions'])
            
            if form.is_valid():
                all_correct = True
                
                # Check each answer
                for q_data in params['questions']:
                    field_name = f"answer_{q_data['type']}"
                    user_ans = form.cleaned_data.get(field_name)
                    target_solution = q_data['target_solution']
                    correct_rounded = int(round(target_solution))
                    
                    if user_ans == correct_rounded:
                        # Correct answer
                        feedback_list.append({
                            'type': q_data['type'],
                            'text': q_data['text'],
                            'correct': True,
                            'message': f"✅ Correct! Exact: {target_solution:.2f}"
                        })
                    else:
                        # Wrong answer
                        all_correct = False
                        hint = get_hint_for_question(
                            q_data['type'], 
                            params['v0'], 
                            params['angle'], 
                            params['h0']
                        )
                        feedback_list.append({
                            'type': q_data['type'],
                            'text': q_data['text'],
                            'correct': False,
                            'message': f"❌ Incorrect. You entered {user_ans}.",
                            'hint': hint
                        })
                
                if all_correct:
                    # All answers correct - advance level
                    request.session['level'] = level + 1
                    messages.success(request, f"🎉 Perfect! All questions correct. Advancing to Level {level + 1}!")
                    
                    # Clear problem from session
                    if 'practice_params' in request.session:
                        del request.session['practice_params']
                    
                    return redirect('projectile:practice')
                # If not all correct, feedback_list will be passed to template
        else:
            messages.error(request, "Session expired. Generating new problem.")
            form = PracticeAnswerForm(questions_data=[])
    else:
        # GET request - initialize form with empty or existing questions
        if params:
            form = PracticeAnswerForm(questions_data=params['questions'])
        else:
            form = PracticeAnswerForm(questions_data=[])

    # --- PROBLEM GENERATION LOGIC ---
    # Only generate if 'practice_params' is missing
    if 'practice_params' not in request.session:
        v0, angle, h0, hf = 0, 0, 0, 0
        
        # Generate random parameters based on level
        if level == 1:
            v0 = random.randint(20, 80)
            angle = random.randint(30, 75)
            h0 = 0
        elif level == 2:
            v0 = random.randint(20, 60)
            angle = random.randint(20, 60)
            h0 = random.randint(20, 100)
        elif level == 3:
            v0 = random.randint(15, 50)
            angle = 0
            h0 = random.randint(50, 150)
        elif level == 4:
            v0 = random.randint(15, 50)
            angle = 0
            h0 = random.randint(30, 100)
        elif level == 5:
            v0 = random.randint(20, 60)
            angle = random.randint(-60, -20)
            h0 = random.randint(50, 150)

        # Calculate physics results
        results = calculate_projectile_motion(v0, angle, h0=h0, hf=hf)
        
        # Define ALL questions for this level
        possible_questions = []
        if level == 1:
            possible_questions = ['max_height', 'range', 'total_time']
        elif level == 2:
            possible_questions = ['range', 'total_time', 'impact_velocity', 'max_height']
        elif level == 3:
            possible_questions = ['total_time']
        elif level == 4:
            possible_questions = ['range', 'impact_velocity']
        elif level == 5:
            possible_questions = ['range', 'total_time', 'impact_velocity']

        # Build question data for ALL questions in this level
        questions_data = []
        for q_type in possible_questions:
            question_info = {
                'type': q_type,
                'text': '',
                'unit': '',
                'target_solution': 0
            }
            
            if q_type == 'max_height':
                question_info['text'] = "Maximum Height (from ground)"
                question_info['unit'] = "m"
                question_info['target_solution'] = results['max_height']
            elif q_type == 'range':
                question_info['text'] = "Horizontal Distance (Range)"
                question_info['unit'] = "m"
                question_info['target_solution'] = results['range']
            elif q_type == 'total_time':
                question_info['text'] = "Total Time of Flight"
                question_info['unit'] = "s"
                question_info['target_solution'] = results['total_time']
            elif q_type == 'impact_velocity':
                question_info['text'] = "Final Velocity (Impact Speed)"
                question_info['unit'] = "m/s"
                question_info['target_solution'] = results['impact_velocity']
            
            questions_data.append(question_info)

        # Save to session
        request.session['practice_params'] = {
            'v0': v0,
            'angle': angle,
            'h0': h0,
            'questions': questions_data,
            'sim_data_json': json.dumps(results)
        }
        
        # Recreate form with new questions
        form = PracticeAnswerForm(questions_data=questions_data)

    # Retrieve parameters from session
    params = request.session['practice_params']
    
    context = {
        'form': form,
        'level': level,
        'v0': params['v0'],
        'angle': params['angle'],
        'h0': params['h0'],
        'questions': params['questions'],
        'feedback_list': feedback_list,
        'sim_data_json': params['sim_data_json'],
    }
    
    return render(request, 'projectile/practice.html', context)