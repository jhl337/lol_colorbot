import cv2  
import numpy as np
from mss import mss
import time
import ghostbox as gb

def colorbot_detect(image):  
    lower_color = np.array([0, 220, 40])  
    upper_color = np.array([10, 255, 70])
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image, lower_color, upper_color)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    font = cv2.FONT_HERSHEY_SIMPLEX  
    font_scale = 0.5  
    font_color = (0, 255, 0) 
    thickness = 1  
    for idx, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)  
        aspect_ratio = float(w) / h  
        if (w / h > 0.85 and w / h < 1.03 and w > 10 and area > 100):  
            cv2.rectangle(image, (x, y), (x+w, y+h), font_color, 2)
            text = f"Area:{area:.2f} Ratio:{aspect_ratio:.2f}"  
            text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]  
            text_x = x if x + text_size[0] < image.shape[1] else x - text_size[0]  
            text_y = y - 5 if y - 5 > 0 else y + h + 10  
            cv2.putText(image, text, (text_x, text_y), font, font_scale, font_color, thickness)
            center_x = x + w // 2  
            center_y = y + h // 2
            offset_x = 44
            offset_y = 89
            cv2.circle(image, (center_x + offset_x, center_y + offset_y), 5, font_color, -1)
            # gb.movemouserelative(center_x + offset_x - screen_width / 2, center_y + offset_y - screen_height / 2)

    cv2.imshow('Image', image)  
    cv2.waitKey(1)  
    # cv2.destroyAllWindows()

if __name__ == '__main__':
    # gb.opendevice(0)
    screen_capture = mss()
    screen_region = screen_capture.monitors[1]
    screen_width = screen_region['width']
    screen_height = screen_region['height']
    screen_region['left'] = screen_width - 100
    screen_region['top'] = screen_height - 50
    screen_region['width'] = screen_width - 100 * 2
    screen_region['height'] = screen_height - 50 * 2
    while True:
        colorbot_detect(np.array(screen_capture.grab(screen_region)))
        time.sleep(0.001)