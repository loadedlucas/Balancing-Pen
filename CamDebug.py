import cv2
from pseyepy import Camera

# Initialize PS3 Eye camera
cam = Camera(fps=60, resolution=Camera.RES_SMALL)

# Read frame
frame, timestamp = cam.read()
# Save image using OpenCV
while True:
        # Read the latest frame from the camera
        frame, timestamp = cam.read()

        # Display the frame in an OpenCV window
        cv2.imshow("PS3 Eye 1 Live Feed", frame[0])
        cv2.imshow("PS3 Eye 2 Live Feed", frame[1])

        # Wait 1ms for the 'q' key press to break the loop

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.waitKey(1) & 0xFF == ord('p'):
            cv2.imwrite(f"calibration_1{timestamp}.jpg", frame[0])
            cv2.imwrite(f"calibration_2{timestamp}.jpg", frame[1])
            
# Clean up
cv2.destroyAllWindows()
cam.end()
print("Camera feed closed cleanly.")