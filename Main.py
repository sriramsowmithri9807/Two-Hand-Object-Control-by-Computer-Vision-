import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=2)  # Enable 2 hands

class CapturedObject:
    def __init__(self, img, x, y, w, h, obj_id):
        self.img = img
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.original_w = w
        self.original_h = h
        self.rotation = 0
        self.scale = 1.0
        self.velocity_y = 0
        self.velocity_x = 0  # Add horizontal velocity for better physics
        self.is_controlled = False
        self.obj_id = obj_id

# Object management
captured_objects = []
selected_object_index = 0
max_objects = 5

# Improved Physics
GRAVITY = 0.4
BOUNCE_DAMPING = 0.7
FRICTION = 0.98
GROUND_LEVEL = 680  # Fixed ground level

# Capture area
roi_x, roi_y, roi_w, roi_h = 200, 150, 300, 250
show_capture_box = True

# Two-hand gesture detection
last_peace_time = 0
peace_cooldown = 1.5
peace_detected_last_frame = False

def get_hand_type(hand):
    """Determine if hand is left or right"""
    return hand["type"]  # cvzone provides this

def get_hand_rotation(lmList):
    """Calculate hand rotation from wrist to middle finger"""
    wrist = lmList[0]
    middle_tip = lmList[12]
    dx = middle_tip[0] - wrist[0]
    dy = middle_tip[1] - wrist[1]
    angle = math.atan2(dy, dx)
    return math.degrees(angle)

def is_peace_sign(lmList):
    """Detect peace sign: only index and middle fingers up"""
    fingers = []
    
    # Thumb (special case for left/right hand)
    if lmList[4][0] > lmList[3][0]:  # Right hand
        fingers.append(1 if lmList[4][0] > lmList[3][0] else 0)
    else:  # Left hand  
        fingers.append(1 if lmList[4][0] < lmList[3][0] else 0)
    
    # Other fingers (compare tip with pip joint)
    for i in range(1, 5):
        fingers.append(1 if lmList[4*i][1] < lmList[4*i-2][1] else 0)
    
    # Peace: index(1) and middle(2) up, others down
    return (fingers[1] == 1 and fingers[2] == 1 and 
            fingers[0] == 0 and fingers[3] == 0 and fingers[4] == 0)

def rotate_image_with_transparency(image, angle):
    """Rotate image with transparent background"""
    if image is None or image.size == 0:
        return image, None
    
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    
    # Get rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Calculate new dimensions
    cos_a = abs(M[0, 0])
    sin_a = abs(M[0, 1])
    new_w = int((h * sin_a) + (w * cos_a))
    new_h = int((h * cos_a) + (w * sin_a))
    
    # Adjust translation
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]
    
    # Create mask for non-black pixels
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    
    # Rotate both image and mask
    rotated_img = cv2.warpAffine(image, M, (new_w, new_h))
    rotated_mask = cv2.warpAffine(mask, M, (new_w, new_h))
    
    return rotated_img, rotated_mask

def apply_improved_physics(obj):
    """Apply realistic physics with proper boundaries"""
    if not obj.is_controlled:
        # Apply gravity
        obj.velocity_y += GRAVITY
        
        # Apply friction to horizontal movement
        obj.velocity_x *= FRICTION
        
        # Update position
        obj.x += int(obj.velocity_x)
        obj.y += int(obj.velocity_y)
        
        # Screen boundaries
        screen_width = 1280
        screen_height = 720
        
        # Left and right boundaries
        if obj.x <= 0:
            obj.x = 0
            obj.velocity_x = -obj.velocity_x * BOUNCE_DAMPING
        elif obj.x + obj.w >= screen_width:
            obj.x = screen_width - obj.w
            obj.velocity_x = -obj.velocity_x * BOUNCE_DAMPING
        
        # Ground collision (bottom)
        if obj.y + obj.h >= GROUND_LEVEL:
            obj.y = GROUND_LEVEL - obj.h  # Keep object above ground
            obj.velocity_y = -obj.velocity_y * BOUNCE_DAMPING
            
            # Stop tiny bounces
            if abs(obj.velocity_y) < 2:
                obj.velocity_y = 0
                
        # Top boundary
        if obj.y <= 0:
            obj.y = 0
            obj.velocity_y = -obj.velocity_y * BOUNCE_DAMPING
    else:
        # Reset velocities when controlled
        obj.velocity_y = 0
        obj.velocity_x = 0

def duplicate_selected_object():
    """Create a duplicate of the currently selected object"""
    if not captured_objects or selected_object_index >= len(captured_objects):
        return False
    
    if len(captured_objects) >= max_objects:
        print(f"Cannot duplicate - maximum {max_objects} objects reached!")
        return False
    
    original = captured_objects[selected_object_index]
    
    # Create new object with offset position
    duplicate = CapturedObject(
        original.img.copy(),
        original.x + 80,  # More offset for clarity
        original.y + 80,
        original.w,
        original.h,
        len(captured_objects)
    )
    
    # Copy current properties
    duplicate.scale = original.scale
    duplicate.rotation = original.rotation
    duplicate.original_w = original.original_w
    duplicate.original_h = original.original_h
    
    captured_objects.append(duplicate)
    print(f"✅ Object duplicated with LEFT hand! Now have {len(captured_objects)} objects")
    return True

while True:
    success, img = cap.read()
    if not success:
        continue

    hands, img = detector.findHands(img)

    # Draw ground line for reference
    cv2.line(img, (0, GROUND_LEVEL), (img.shape[1], GROUND_LEVEL), (100, 100, 100), 2)

    # Show capture box
    if show_capture_box:
        cv2.rectangle(img, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (0, 255, 0), 2)
        cv2.putText(img, "Capture Zone", (roi_x, roi_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    key = cv2.waitKey(1) & 0xFF
    
    # CAPTURE OBJECT
    if key == ord('c') and show_capture_box and len(captured_objects) < max_objects:
        roi = img[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray_roi, 100, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 500:
                x, y, w, h = cv2.boundingRect(largest_contour)
                captured_img = img[roi_y + y:roi_y + y + h, roi_x + x:roi_x + x + w].copy()
                
                new_obj = CapturedObject(captured_img, roi_x + x, roi_y + y, w, h, len(captured_objects))
                captured_objects.append(new_obj)
                selected_object_index = len(captured_objects) - 1
                print(f"📦 Object {len(captured_objects)} captured!")
            else:
                print("❌ Object too small - try a larger object")
        else:
            new_obj = CapturedObject(roi.copy(), roi_x, roi_y, roi_w, roi_h, len(captured_objects))
            captured_objects.append(new_obj)
            selected_object_index = len(captured_objects) - 1
            print(f"📦 Captured area as object {len(captured_objects)}")
    
    # SELECT OBJECTS with number keys
    elif key >= ord('1') and key <= ord('5'):
        obj_index = key - ord('1')
        if obj_index < len(captured_objects):
            selected_object_index = obj_index
            print(f"🎯 Selected object {obj_index + 1}")
    
    # RESET
    elif key == ord('r'):
        captured_objects.clear()
        selected_object_index = 0
        show_capture_box = True
        print("🔄 Reset! All objects cleared")
    
    # QUIT
    elif key == ord('q'):
        break

    # TWO-HAND TRACKING & CONTROL
    right_hand = None
    left_hand = None
    current_peace = False
    
    # Separate hands
    if hands:
        for hand in hands:
            if get_hand_type(hand) == "Right":
                right_hand = hand
            else:
                left_hand = hand
    
    # Control with selected object
    if captured_objects and selected_object_index < len(captured_objects):
        selected_obj = captured_objects[selected_object_index]
        
        # RIGHT HAND: Movement and Rotation
        if right_hand:
            selected_obj.is_controlled = True
            lmList_right = right_hand["lmList"]
            
            # Move with index finger
            cursor = lmList_right[8]
            selected_obj.x = cursor[0] - selected_obj.w // 2
            selected_obj.y = cursor[1] - selected_obj.h // 2
            
            # Rotate with hand tilt
            selected_obj.rotation = get_hand_rotation(lmList_right)
        
        # LEFT HAND: Scale and Duplicate
        if left_hand:
            lmList_left = left_hand["lmList"]
            
            # Scale with thumb-pinky distance
            thumb_pinky_dist = math.sqrt((lmList_left[4][0] - lmList_left[20][0])**2 + 
                                       (lmList_left[4][1] - lmList_left[20][1])**2)
            scale = max(0.3, min(3.0, thumb_pinky_dist / 150))
            selected_obj.scale = scale
            selected_obj.w = int(selected_obj.original_w * scale)
            selected_obj.h = int(selected_obj.original_h * scale)
            
            # Duplicate with peace sign (LEFT HAND)
            current_peace = is_peace_sign(lmList_left)
            current_time = time.time()
            
            if current_peace and not peace_detected_last_frame and (current_time - last_peace_time) > peace_cooldown:
                if duplicate_selected_object():
                    last_peace_time = current_time
        
        # If no hands detected, object is not controlled
        if not right_hand and not left_hand:
            selected_obj.is_controlled = False
        
        # Mark other objects as not controlled
        for i, obj in enumerate(captured_objects):
            if i != selected_object_index:
                obj.is_controlled = False

    # Update peace sign state for next frame
    peace_detected_last_frame = current_peace

    # APPLY IMPROVED PHYSICS
    for obj in captured_objects:
        apply_improved_physics(obj)

    # RENDER OBJECTS
    for i, obj in enumerate(captured_objects):
        if obj.img is not None:
            # First resize the image according to scale
            scaled_w = int(obj.original_w * obj.scale)
            scaled_h = int(obj.original_h * obj.scale)
            
            if scaled_w > 0 and scaled_h > 0:
                scaled_img = cv2.resize(obj.img, (scaled_w, scaled_h))
                
                # Then rotate the scaled image
                rotated_img, rotated_mask = rotate_image_with_transparency(scaled_img, obj.rotation)
                
                if rotated_img is not None and rotated_mask is not None and rotated_img.size > 0:
                    rh, rw = rotated_img.shape[:2]
                    
                    # Position calculation - center the rotated image on object position
                    x1 = max(0, obj.x - rw // 2)
                    y1 = max(0, obj.y - rh // 2)
                    x2 = min(img.shape[1], x1 + rw)
                    y2 = min(img.shape[0], y1 + rh)
                    
                    if x2 > x1 and y2 > y1:
                        # Crop if needed to fit screen
                        crop_x1 = max(0, -x1) if x1 < 0 else 0
                        crop_y1 = max(0, -y1) if y1 < 0 else 0
                        crop_x2 = rw - max(0, x2 - img.shape[1]) if x2 > img.shape[1] else rw
                        crop_y2 = rh - max(0, y2 - img.shape[0]) if y2 > img.shape[0] else rh
                        
                        # Adjust screen coordinates
                        x1 = max(0, x1)
                        y1 = max(0, y1)
                        
                        if crop_x2 > crop_x1 and crop_y2 > crop_y1:
                            cropped_img = rotated_img[crop_y1:crop_y2, crop_x1:crop_x2]
                            cropped_mask = rotated_mask[crop_y1:crop_y2, crop_x1:crop_x2]
                            
                            if cropped_img.size > 0 and cropped_mask.size > 0:
                                # Get background region first to match dimensions
                                bg_region = img[y1:y2, x1:x2]
                                
                                # Ensure cropped image matches background region dimensions
                                bg_h, bg_w = bg_region.shape[:2]
                                crop_h, crop_w = cropped_img.shape[:2]
                                
                                if bg_h != crop_h or bg_w != crop_w:
                                    cropped_img = cv2.resize(cropped_img, (bg_w, bg_h))
                                    cropped_mask = cv2.resize(cropped_mask, (bg_w, bg_h))
                                
                                # Convert mask to 3-channel for blending
                                mask_3d = cv2.cvtColor(cropped_mask, cv2.COLOR_GRAY2BGR) / 255.0
                                
                                # Blend
                                blended = (cropped_img * mask_3d + bg_region * (1 - mask_3d)).astype(np.uint8)
                                img[y1:y2, x1:x2] = blended
            
            # Selection indicator
            if i == selected_object_index:
                cv2.circle(img, (obj.x, obj.y - 15), 8, (0, 255, 255), -1)
                cv2.putText(img, str(i+1), (obj.x - 5, obj.y - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    # STATUS DISPLAY
    if captured_objects:
        selected_obj = captured_objects[selected_object_index] if selected_object_index < len(captured_objects) else None
        if selected_obj:
            cv2.putText(img, f"Selected: {selected_object_index + 1}/{len(captured_objects)} | Scale: {selected_obj.scale:.1f}x", 
                       (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            
            # Show hand control status
            hand_status = ""
            if right_hand and left_hand:
                hand_status = "RIGHT: Move+Rotate | LEFT: Scale+Duplicate"
            elif right_hand:
                hand_status = "RIGHT hand detected - Move & Rotate active"
            elif left_hand:
                hand_status = "LEFT hand detected - Scale & Duplicate active"
            else:
                hand_status = "No hands detected - Object falling"
                
            cv2.putText(img, hand_status, (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # INSTRUCTIONS
    if show_capture_box:
        cv2.putText(img, "Place object in green box and press 'c'", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    else:
        cv2.putText(img, "RIGHT HAND: Move + Rotate | LEFT HAND: Scale + Peace Sign Duplicate", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    cv2.putText(img, "Numbers 1-5: Select | 'r': Reset | 'q': Quit", (10, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Two-Hand Object Control", img)

cap.release()
cv2.destroyAllWindows()