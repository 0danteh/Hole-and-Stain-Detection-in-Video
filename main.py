import cv2
import numpy as np
import os

def detect_holes_and_stains(video_path, output_path=None):
    if not os.path.exists(video_path):
        print(f"Error: Input video file '{video_path}' not found!")
        return
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file '{video_path}'")
        return
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    if output_path:
        try:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
            
            if not out.isOpened():
                fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                output_path = output_path.replace('.mp4', '.avi')
                out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
                print(f"Using alternative codec. Output will be saved as '{output_path}'")
        
        except Exception as e:
            print(f"Error initializing video writer: {str(e)}")
            return
    
    white_lower = np.array([250, 250, 250])
    white_upper = np.array([255, 255, 255])
    
    orange_lower = np.array([0, 70, 50])
    orange_upper = np.array([25, 255, 255])
    
    stain_lower = np.array([0, 0, 0])
    stain_upper = np.array([50, 50, 50])
    
    blue_stain_lower = np.array([100, 100, 50])
    blue_stain_upper = np.array([140, 255, 255])
    
    green_stain_lower = np.array([40, 50, 50])
    green_stain_upper = np.array([80, 255, 255])
    
    red_stain_lower1 = np.array([0, 50, 50])
    red_stain_upper1 = np.array([10, 255, 255])
    red_stain_lower2 = np.array([170, 50, 50])
    red_stain_upper2 = np.array([180, 255, 255])
    
    min_hole_area = 100
    max_hole_area = 5000
    min_stain_area = 50
    max_stain_area = 3000
    
    frame_count = 0
    kernel = np.ones((3, 3), np.uint8)
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_count += 1
            if frame_count % 30 == 0:
                print(f"Processing frame {frame_count}")
                
            output_frame = frame.copy()
            
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            white_mask = cv2.inRange(frame, white_lower, white_upper)
            orange_mask = cv2.inRange(hsv, orange_lower, orange_upper)
            orange_mask = cv2.GaussianBlur(orange_mask, (5, 5), 0)
            orange_mask = cv2.morphologyEx(orange_mask, cv2.MORPH_CLOSE, kernel)
            orange_mask = cv2.morphologyEx(orange_mask, cv2.MORPH_OPEN, kernel)
            combined_hole_mask = cv2.bitwise_or(white_mask, orange_mask)
            combined_hole_mask = cv2.morphologyEx(combined_hole_mask, cv2.MORPH_CLOSE, kernel)
            
            stain_mask = cv2.inRange(frame, stain_lower, stain_upper)
            stain_mask = cv2.morphologyEx(stain_mask, cv2.MORPH_CLOSE, kernel)
            
            blue_stain_mask = cv2.inRange(hsv, blue_stain_lower, blue_stain_upper)
            blue_stain_mask = cv2.morphologyEx(blue_stain_mask, cv2.MORPH_CLOSE, kernel)
            
            green_stain_mask = cv2.inRange(hsv, green_stain_lower, green_stain_upper)
            green_stain_mask = cv2.morphologyEx(green_stain_mask, cv2.MORPH_CLOSE, kernel)
            
            red_stain_mask1 = cv2.inRange(hsv, red_stain_lower1, red_stain_upper1)
            red_stain_mask2 = cv2.inRange(hsv, red_stain_lower2, red_stain_upper2)
            red_stain_mask = cv2.bitwise_or(red_stain_mask1, red_stain_mask2)
            red_stain_mask = cv2.morphologyEx(red_stain_mask, cv2.MORPH_CLOSE, kernel)
            
            combined_stain_mask = cv2.bitwise_or(stain_mask, blue_stain_mask)
            combined_stain_mask = cv2.bitwise_or(combined_stain_mask, green_stain_mask)
            combined_stain_mask = cv2.bitwise_or(combined_stain_mask, red_stain_mask)
            
            hole_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
            
            contours, _ = cv2.findContours(combined_hole_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if min_hole_area < area < max_hole_area:
                    cv2.drawContours(hole_mask, [contour], 0, 255, -1)
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(output_frame, [box], 0, (0, 255, 0), 2)
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.putText(output_frame, "Hole", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            combined_stain_mask = cv2.bitwise_and(combined_stain_mask, cv2.bitwise_not(hole_mask))

            contours, _ = cv2.findContours(combined_stain_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if min_stain_area < area < max_stain_area:
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(output_frame, [box], 0, (255, 0, 0), 2)
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.putText(output_frame, "Stain", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            
            if output_path and out.isOpened():
                out.write(output_frame)
            
            cv2.imshow('Hole and Stain Detection', output_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except Exception as e:
        print(f"Error during video processing: {str(e)}")
    
    finally:
        print("Cleaning up...")
        cap.release()
        if output_path and 'out' in locals():
            out.release()
        cv2.destroyAllWindows()
        
        if output_path:
            if os.path.exists(output_path):
                print(f"Video saved successfully to: {output_path}")
                print(f"Processed {frame_count} frames")
            else:
                print("Error: Output video file was not created successfully")

if __name__ == "__main__":
    video_path = "D:/Documents/VS Projects/mech_ai_vision/AnomCotton.mp4"
    output_path = "output.avi" 
    detect_holes_and_stains(video_path, output_path)
