from picamera import PiCamera

cam = PiCamera()


cam.resolution = (4056, 3040)



for i in range(3):
    cam.capture(f"image{i}1.png")
    
    
