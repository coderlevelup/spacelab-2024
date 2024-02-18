estimate_kmps = 3.1415926  # pi for debug
from logzero import logger, logfile
from time import sleep
from random import random
import merliandrocam
import ISS_speedy

logfile("spacelab.log")

def write_result(result):
    # Format the estimate_kmps to have a precision
    # of 5 significant figures
    estimate_kmps_formatted = "{:.4f}".format(result)

    # Create a string to write to the file
    output_string = estimate_kmps_formatted

    # Write to the file
    file_path = "result.txt"
    try:
        with open(file_path, 'w') as file:
            try:
                file.write(output_string)
                logger.info(f"Result {output_string} written to file.")
            except (IOError, OSError):
                logger.error("Error writing to file")
    except (FileNotFoundError, PermissionError, OSError):
        logger.error("Error opening file")
        

def estimate_speed(run_number):
    photos = merliandrocam.capture_images(run_number, 7)
    if not photos:
        logger.error("No filenames returned") 
        return
    image_files_a = photos[:-1]
    image_files_b = photos[1:]
    pairs = list(zip(image_files_a, image_files_b))
    pair_speeds = []
    for pair in pairs:
        logger.debug(f'Calculating speed for {pair[0]}, {pair[1]}')
        speed = ISS_Speedy.incredible_snake_sky_speedy(pair[0], pair[1])
        print(speed)
        pair_speeds.append(speed)
    return sum(pair_speeds) / len(pair_speeds)

estimates = []
for i in range(6):
    logger.info(f"Loop number {i+1} started")
    # come up with next estimate
    new_estimate = estimate_speed(i)
    logger.info(f"Estimate {i+1}: {new_estimate}")

    if new_estimate:
        estimates.append(new_estimate)
        
    # write every time we have a new estimate in case program crashes
    if len(estimates) > 0:
        average_estimate = sum(estimates)/len(estimates)
        write_result(average_estimate)
    else:
        logger.error("Ne estimates calculated")
        write_result(0)

    
