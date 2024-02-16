estimate_kmps = 3.1415926  # pi for debug
from logzero import logger, logfile
from time import sleep
from random import random

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
        

def estimate_speed():
    return 7 + random()

estimates = []
for i in range(100):
    logger.info(f"Loop number {i+1} started")
    # come up with next estimate
    new_estimate = estimate_speed()
    logger.info(f"Estimate {new_estimate}")
    estimates.append(new_estimate)
    average_estimate = sum(estimates)/len(estimates)
    # write every time we have a new estimate in case program crashes
    write_result(average_estimate)
    sleep(0.1)
    
