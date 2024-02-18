from exif import Image
from datetime import datetime
import cv2
import math
import logzero
from logzero import logger

logzero.logfile("space.log")

def get_time(image):
    with open(image, 'rb') as image_file:
        img = Image(image_file)
        time_str = img.get("datetime_original")
        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
    return time    
        
            
def get_time_difference(image_1, image_2):
     time_1 = get_time(image_1)
     time_2 = get_time(image_2)
     time_difference = time_2 - time_1
     return time_difference.seconds

def convert_to_cv(image_1, image_2):
     image_1_cv = cv2.imread(image_1, 0)
     image_2_cv = cv2.imread(image_2, 0)
     return image_1_cv, image_2_cv
    
    
def calculate_features(image_1_cv, image_2_cv, feature_number):
    orb = cv2.ORB_create(nfeatures = feature_number)
    keypoints_1, descriptors_1 = orb.detectAndCompute(image_1_cv, None)
    keypoints_2, descriptors_2 = orb.detectAndCompute(image_2_cv, None)
    return keypoints_1, keypoints_2, descriptors_1, descriptors_2
    
def calculate_matches(descriptors_1, descriptors_2):
    brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = brute_force.match(descriptors_1, descriptors_2)
    matches = sorted(matches, key=lambda x: x.distance)
    clean_matches = []
    for match in matches:
        if match.distance < 30:
            print(match.distance)
            clean_matches.append(match)
#     return matches
    return clean_matches


def display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches):
    match_img = cv2.drawMatches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches, None)
    resize = cv2.resize(match_img, (1600,600), interpolation = cv2.INTER_AREA)
    cv2.imshow('matches', resize)
    cv2.waitKey(0)
    cv2.destroyWindow('matches')


def find_matching_coordinates(keypoints_1, keypoints_2, matches):
    coordinates_1 = []
    coordinates_2 = []
    for match in matches:
        image_1_idx = match.queryIdx
        image_2_idx = match.trainIdx
        (x1,y1) = keypoints_1[image_1_idx].pt
        (x2,y2)  = keypoints_2[image_2_idx].pt
        coordinates_1.append((x1,y1))
        coordinates_2.append((x2,y2))
    return coordinates_1, coordinates_2 


def calculate_mean_distance(coordinates_1, coordinates_2):
    all_distance = 0
    all_distances = []
    merged_coordinates = list(zip(coordinates_1, coordinates_2))
    for coordinate in merged_coordinates:
        x_difference = coordinate[0][0] - coordinate[1][0]
        y_difference = coordinate[0][1] - coordinate[1][1]
        distance = math.hypot(x_difference, y_difference)
#         logger.debug(f'Distance {distance} px')
        print(distance)
        all_distances.append(distance)
    return sum(all_distances) / len(all_distances)

def calculate_speed_in_kmps(feature_distance, GSD, time_difference):
    distance = feature_distance * GSD / 100000
    speed = distance / time_difference
    return speed


def incredible_snake_sky_speedy(image_1, image_2):
    # print(merged_coordinates[0])
    time_difference = get_time_difference(image_1, image_2) # Get time difference between image
    image_1_cv, image_2_cv = convert_to_cv(image_1, image_2) # Create OpenCV image objects
    keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000) # Get keypoints and descriptors
    matches = calculate_matches(descriptors_1, descriptors_2) # Match descriptors
    
    try:
        display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches) # Display matches
    except:
        pass
    coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)
#     print(coordinates_1[0], coordinates_2[0])
    average_feature_distance = calculate_mean_distance(coordinates_1, coordinates_2)
    logger.debug(f'Average feature distance {average_feature_distance} pixels')
    speed = calculate_speed_in_kmps(average_feature_distance, 12648, time_difference)   
    logger.info(f'Speed: {speed} km / second!')
    logger.info(f'Speed: {speed*60*60} km / hour!')

    logger.info("We Love SPACE!")
    
    return speed



if __name__ == "__main__":
    image_1 = 'run_0_gps_image_0.jpg'
    image_2 = 'run_0_gps_image_1.jpg'
    incredible_snake_sky_speedy(image_1, image_2)
    

