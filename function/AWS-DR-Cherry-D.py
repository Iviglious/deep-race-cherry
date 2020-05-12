

def reward_function(params):
    '''
    Cosine reward function for heading angle
    '''
    # Import libraries
    import math

    # PARAMETERS (CONSTANTS)
    # Total num of steps we want the car to finish the lap, it will vary depends on the track length
    TOTAL_NUM_STEPS = 300
    # Max angle threshold (degrees). Heading direction of the car in regards to the track (closest waypoints).
    HEADING_THRESHOLD = 40.0
    # Max speed
    MAX_SPEED = 12.1
    # Max steering angle (degree)
    MAX_STEERING = 30.1

    # Read input parameters
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering_abs = abs(params['steering_angle']) # Only need the absolute steering angle (max: 30, min -30)
    speed = params['speed']
    steps = params['steps']
    progress = params['progress']
    all_wheels_on_track = params['all_wheels_on_track']
    #waypoints = params['waypoints']
    #closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # Give higher reward if the agent is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track

    # Penalize the reward if the heading angle is too large
    if abs(heading) > HEADING_THRESHOLD:
        reward *= 0.01
    else:
        reward *= math.cos(math.radians(heading)) * 3.0 - 2.0   # cos * 3 - 2 (0.1 -> 1)

    # Give additional reward if the car pass every 100 steps faster than expected 
    if (steps % 100) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100 :
        reward += progress/100.0

    # Penalize if the car goes off track
    if not all_wheels_on_track:
        reward = 1e-3
    
    return float(reward)
    

# Test function
print(reward_function({
     'distance_from_center': 0
    ,'track_width': 10
    ,'steering_angle': 0
    ,'speed': 1
    ,'steps': 100
    ,'progress': 40
    ,'all_wheels_on_track': True
    ,'heading': 0
}))
