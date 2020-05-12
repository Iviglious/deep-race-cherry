# Import libraries
import math

def get_reward_distance_center(track_width, distance_from_center):
    ####################################
    ## Distance from center
    ####################################
    DISTANCE_THRESHOLD = 60 # degrees: cos(0)=1; cos(60)=0.5
    
    # Convert distance to degrees
    distance_deg = distance_from_center * DISTANCE_THRESHOLD * 2 / track_width
    
    # Default value
    reward = 0.01  # likely crashed/ close to off track

    # Give higher reward if the agent is closer to center line and vice versa
    if distance_deg <= DISTANCE_THRESHOLD:
        reward = math.cos(math.radians(distance_deg))
    
    return reward


def get_reward_car_angle(waypoints, closest_waypoints, heading):
    ####################################
    ## Car angle vs track angle
    ####################################
    # Max angle threshold (degrees). Heading direction of the car in regards to the track (closest waypoints).
    HEADING_THRESHOLD = 30
    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_angle = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]) 
    # Convert to degree
    track_angle = math.degrees(track_angle)
    # Calculate angle between track and car heading
    abs_angle = abs(track_angle - heading)
    if (abs_angle >= 360 - HEADING_THRESHOLD):
        abs_angle = 360 - abs_angle
    
    # Default value
    reward = 0.01
    
    # Penalize the reward if the heading angle is too large
    if (abs_angle <= HEADING_THRESHOLD):
        reward = math.cos(math.radians(abs_angle)) * 3.0 - 2.0     # cos * 3 - 2 (0.1 -> 1)

    return reward


def get_reward_speed(speed):
    ####################################
    ## Car Speed
    ####################################
    # Max speed. Used to normalize speed between 0 and 1
    SPEED_THRESHOLD = 1.0   # meters per second

    return speed/SPEED_THRESHOLD


def get_reward_car_steer(waypoints, closest_waypoints, heading, steering):
    ####################################
    ## Car angle vs track angle vs Car steering angle
    ####################################
    # Max angle threshold (degrees). Heading direction of the car in regards to the track (closest waypoints).
    HEADING_THRESHOLD = 30
    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_angle = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]) 
    # Convert to degree
    track_angle = math.degrees(track_angle)
    # Calculate angle between track and car heading
    abs_angle = abs(track_angle - heading - steering)
    if (abs_angle >= 360 - HEADING_THRESHOLD):
        abs_angle = 360 - abs_angle
    
    # Default value
    reward = 0.01

    if (abs_angle <= HEADING_THRESHOLD):
        reward = math.cos(math.radians(abs_angle)) * 3.0 - 2.0

    return reward


def reward_function(params):
    '''
    Center * Car Angle * Car Speed * Car Steer
    '''
    # PARAMETERS (CONSTANTS)
    # Importance of the distance from center
    DISTANCE_CENTER_COEF = 1.0
    # Importance of the heading angle
    HEADING_COEF = 1.0
    # Importance of speed
    SPEED_COEF = 1.0
    # Importance of steer
    STEER_COEF = 1.0

    # Read input parameters
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering = params['steering_angle'] # Car steering angle (max: 30, min -30)
    speed = params['speed']
    #steps = params['steps']
    #progress = params['progress']
    all_wheels_on_track = params['all_wheels_on_track']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']


    ####################################
    ## Elimination rules - no need to check further
    ####################################
    # Penalize if the car goes off track
    if not all_wheels_on_track:
        return float(0.0)
    
    # Get all rewards
    reward = 1.0
    reward *= get_reward_distance_center(track_width, distance_from_center) * DISTANCE_CENTER_COEF
    reward *= get_reward_car_angle(waypoints, closest_waypoints, heading) * HEADING_COEF
    reward *= get_reward_speed(speed) * SPEED_COEF
    reward *= get_reward_car_steer(waypoints, closest_waypoints, heading, steering) * STEER_COEF

    return float(reward)
    



# Test function
'''
print(reward_function({
     'distance_from_center': 0
    ,'track_width': 10
    ,'steering_angle': 0
    ,'speed': 1
    #,'steps': 0
    #,'progress': 0
    ,'all_wheels_on_track': True
    ,'waypoints':[(100,100),(150,100)]
    ,'closest_waypoints':[0,1]
    ,'heading': 40.0
}))
'''
'''
import pandas as pd

ma = 11
mb = 11
mc = 11

tot = ma*mb*mc

xa = [x % ma for x in range(0,tot,1)]
xb = [int(x / ma) % mb for x in range(0,tot,1)]
xc = [int(x / (mb*ma)) for x in range(0,tot,1)]

df = pd.DataFrame({'a':xa, 'b':xb, 'c':xc})

df['distance_from_center'] = df.a * 1.0
df['heading'] = df.b * 80.0/10.0 - 40.0 # from -40 to 40 degrees
df['steering_angle'] = df.c * 80.0/10.0 - 40.0 # from -40 to 40 degrees

# Add rewards column
df['reward'] = [reward_function({
     'distance_from_center': distance_from_center
    ,'track_width': 10
    ,'steering_angle': steering_angle
    ,'speed': 1.0
    ,'all_wheels_on_track': True
    ,'waypoints':[(100,100),(150,100)]
    ,'closest_waypoints':[0,1]
    ,'heading': heading
}) for a,b,c, distance_from_center,heading,steering_angle in df.values]

# Add index column
df['scenario'] = df.a*10000 + df.b*100 + df.c

#print(df.head(12))
#print(df.tail(12))
df.to_csv(path_or_buf='Test_Results_Cherry-I.csv', index=False)

'''