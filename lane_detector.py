# Import the required libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
from playsound import playsound
import simpleaudio as sa
from time import time 

height = 0
triangle = None
def canny_edge_detector(image):
    # Convert the image color to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Reduce noise from the image
    blur = cv2.GaussianBlur(gray_image, (7, 7), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def region_of_interest(image):
    global triangle
    height = image.shape[0]
    width = image.shape[1]

    polygons = np.array([
            # bl, br, tr, tl
            [(700, height-100), (1600, height-100), (1125, height - 300), (1075, height - 300)]
            ])
    mask = np.zeros_like(image)

    # Fill poly-function deals with multiple polygon
    cv2.fillPoly(mask, polygons, 255)

    # Bitwise operation between canny image and mask image
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def draw_trap(image, color):
  line_image = np.copy(image)
  triangle = [(700, height), (1750, height), (1300, height - 200), (950, height - 200)]
  cv2.fillConvexPoly(line_image, np.array(triangle), color)
  # for i in range(4):
  #   cv2.line(line_image, triangle[i], triangle[(i + 1) % 4], (255, 0, 0), 1)
  return line_image

def create_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1 * (3 / 5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)

        # It will fit the polynomial and the intercept and slope
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if abs(slope) > 0.1:
          if slope < 0:
              left_fit.append((slope, intercept))
          else:
              right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = create_coordinates(image, left_fit_average)
    right_line = create_coordinates(image, right_fit_average)
    return np.array([left_line, right_line]), left_fit_average, right_fit_average

def display_lines(image, lines, veering = False):
  line_image = np.zeros_like(image)
  color = (0, 0, 255) if veering else (0, 255, 0)
  if lines is not None:
      for x1, y1, x2, y2 in lines:
          cv2.line(line_image, (x1, y1), (x2, y2), color, 5)
  return line_image

# x coordinate of vanishing point
def intersection(values1, values2, calibration = False):
    global height, triangle
    s1 = values1[0]
    y1 = values1[1]
    s2 = values2[0]
    y2 = values2[1]
    value = (y1-y2)/(s2-s1)
    return value

def is_drifting(threshold, margin, vanishing_point):
  return abs(threshold - vanishing_point) > margin

cap = cv2.VideoCapture("data/1608331588-no_lines.avi") 
cap = cv2.VideoCapture("data/last_last.avi") 
   
if (cap.isOpened() == False):  
    print("Error reading video file") 
  
frame_width = int(cap.get(3)) 
frame_height = int(cap.get(4)) 
   
size = (frame_width, frame_height) 
   
filename = 'watchout.wav'
wave_obj = sa.WaveObject.from_wave_file(filename)
play_obj = None

write = True
if write:
  result = cv2.VideoWriter(f"data/{int(time())}.avi",  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         10, size) 

  result_no_lines = cv2.VideoWriter(f"data/{int(time())}-no_lines.avi",  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         10, size) 

calibration_phase = 0
detection_active = False
# threshold = 564
threshold = 0
drift_threshold = 15
v_sum = 0
drift_time = 0
straight_time = 0
while (cap.isOpened()):
    try:
      # frame.shape: (1080, 1920, 3)
      _, frame = cap.read()
      # trap = draw_trap(frame, (255, 0, 0))
      if write:
        result_no_lines.write(frame)
      height = frame.shape[0]
      weighted = cv2.addWeighted(frame, 2, np.zeros_like(frame), 1, 0)
      canny_image = canny_edge_detector(weighted)
      cropped_image = region_of_interest(canny_image)
      # cv2.imshow("img", cropped_image)

      lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 100,
                                                      np.array([]), minLineLength = 40,
                                                      maxLineGap = 10)
      averaged_lines, left_lane, right_lane = average_slope_intercept(frame, lines)
      vanishing_point = intersection(left_lane, right_lane)
      calibration_phase += 1
      if calibration_phase < 100:
          threshold = threshold + vanishing_point
          print(threshold)
      drifting = False if calibration_phase < 100 else is_drifting(threshold/100, 50, vanishing_point)
      
      if calibration_phase < 100:
          trap = draw_trap(frame, (0, 255, 255))
      elif drifting:
        drift_time = (drift_time+1)%100
        print(f"drifting time: {drift_time}")
        if drift_time > drift_threshold and play_obj == None:
          trap = draw_trap(frame, (0, 0, 255))
          print("Playing")
          play_obj = wave_obj.play()
          straight_time = 0
      else:
        straight_time += 1
        if straight_time > 10:
          drift_time = 0
          trap = draw_trap(frame, (0, 255, 0))
        if play_obj != None:
          print("Stopped")
          # play_obj.wait_done()
          play_obj = None
        
      line_image = display_lines(frame, averaged_lines, drifting)
      combo_image = cv2.addWeighted(frame, 1, line_image, 0.5, 1)
      trap_image = cv2.addWeighted(frame, 1, trap, 0.3, 1)
      cv2.imshow("results", trap_image)
      if write:
        result.write(trap_image)
    except:
      if calibration_phase > 100:
        drift_time = (drift_time+1)%100
        print(f"drifting time: {drift_time}")
        if drift_time > drift_threshold and play_obj == None:
            print("Playing")
            trap = draw_trap(frame, (0, 0, 255))
            play_obj = wave_obj.play()
      else:
        trap = draw_trap(frame, (0, 255, 255))
      trap_image = cv2.addWeighted(frame, 1, trap, 0.3, 1)
      cv2.imshow("results", trap_image)
      if write:
        result.write(trap_image)
      pass

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
print(f"avg threshold: {threshold/100}")

cap.release()

cv2.destroyAllWindows()
