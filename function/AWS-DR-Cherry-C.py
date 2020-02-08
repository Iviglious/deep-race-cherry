

def reward_function(params):
    '''
    Example of penalize steering, which helps mitigate zig-zag behaviors
    '''
    # Import libraries
    import math

    # PARAMETERS (CONSTANTS)
    # Total num of steps we want the car to finish the lap, it will vary depends on the track length
    TOTAL_NUM_STEPS = 300
    # Max angle threshold (degrees). Heading direction of the car in regards to the track (closest waypoints).
    DIRECTION_THRESHOLD = 10.0
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
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
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


     # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]) 
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize the reward if the difference is too large
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5

    # Give additional reward if the car pass every 100 steps faster than expected 
    if (steps % 100) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100 :
        reward += 10.0*progress

    # Penalize if the car goes off track
    if not all_wheels_on_track:
        reward = 1e-3
    
    return float(reward)
    

# Test function
print(reward_function({'distance_from_center':0, 'track_width':10, 'steering_angle':0, 'speed':1}))
