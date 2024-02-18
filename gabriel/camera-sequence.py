from picamera import PiCamera

cam = PiCamera()


cam.resolution = (4056, 3040)



for x in range(3):
    cam.capture(f"image{x}1.png")
    
    
