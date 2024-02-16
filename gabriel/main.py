from orbit import ISS
from picamera import PiCamera

cam = PiCamera()
cam.resolution = (4056,3040)

def convert(angle):

    # Convert a `skyfield` Angle to an Exif-appropriate
    # representation (positive rationals)
    # e.g. 98° 34' 58.7 to "98/1,34/1,587/10"

    # Return a tuple containing a Boolean and the converted angle,
    # with the Boolean indicating if the angle is negative

    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return sign < 0, exif_angle

def custom_capture(iss, camera, image):
    # Use `camera` to capture an `image` file with lat/long Exif data
    point = iss.coordinates()

    # Convert the latitude and longitude to Exif-appropriate
    # representations
    south, exif_latitude = convert(point.latitude)
    west, exif_longitude = convert(point.longitude)

    # Set the Exif tags specifying the current location
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"

    # Capture the image
    camera.capture(image)


custom_capture(ISS(), cam, "gps_image1.jpg")