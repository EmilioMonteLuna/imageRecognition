"""
Gesture Detector - Real-time facial expression and hand gesture recognition
Displays custom images/memes based on detected gestures
"""

import os
import sys

# Suppress TensorFlow and MediaPipe warnings (must be set BEFORE imports)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow warnings
os.environ['GLOG_minloglevel'] = '2'  # Suppress MediaPipe warnings

# Enable UTF-8 encoding for Windows CMD
if sys.platform == 'win32':
    os.system('chcp 65001 > nul 2>&1')

import cv2
import mediapipe as mp
import numpy as np
from pathlib import Path
import time

# Suppress Python warnings
import warnings
warnings.filterwarnings('ignore')

class GestureDetector:
    def __init__(self):
        # Initialize MediaPipe
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils

        # Initialize face mesh and hand detection
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )

        # Asset paths
        self.assets_dir = Path("assets")
        self.assets_dir.mkdir(exist_ok=True)

        # Load reaction images
        self.reactions = {
            'heart': self.load_image('lovely.gif'),
            'tongue_out': self.load_image('tongue.gif'),  # Using hello.gif for tongue
            'eyes_closed': self.load_image('closed_eyes.gif'),  # Note: hyphen not underscore
            'peace_sign': self.load_image('peace.gif'),
            'thumbs_up': self.load_image('thumbs_up.gif'),
            'open_palm': self.load_image('open_palm.gif'),
            'fist': self.load_image('fist.gif'),
            'default': (self.create_default_image(), False)  # Return as tuple for consistency
        }

        # Current state
        self.current_reaction = 'default'
        self.last_detection_time = time.time()
        self.show_landmarks = False  # Toggle for showing face/hand landmarks

    def load_image(self, filename):
        """Load an image or GIF from assets folder"""
        file_path = self.assets_dir / filename

        # Try different extensions
        for ext in ['', '.gif', '.jpg', '.png', '.jpeg']:
            test_path = file_path.with_suffix(ext) if ext else file_path
            if test_path.exists():
                # Check if it's a GIF
                if test_path.suffix.lower() == '.gif':
                    try:
                        import imageio
                        # Load GIF frames
                        gif_frames = imageio.mimread(str(test_path))
                        if gif_frames:
                            print(f"Loaded GIF: {filename} ({len(gif_frames)} frames)")
                            # Return info: (frames, is_gif)
                            return (gif_frames, True)
                    except Exception as e:
                        print(f"Warning: Could not load GIF {filename}: {e}")
                        # Fall through to try loading as static image
                        pass

                # Static image (PNG/JPG)
                img = cv2.imread(str(test_path))
                if img is not None:
                    print(f"Loaded static image: {filename}")
                    return (cv2.resize(img, (640, 480)), False)

        # Return placeholder if not found
        print(f"Warning: Could not find {filename}, using placeholder")
        return (self.create_placeholder_image(filename), False)

    def create_placeholder_image(self, text):
        """Create a placeholder image with text"""
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        img.fill(50)
        cv2.putText(img, f"Add: {text}", (150, 240),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        return img

    def create_default_image(self):
        """Create default reaction image"""
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        img.fill(30)
        cv2.putText(img, "Make a gesture!", (180, 240),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
        return img

    def detect_tongue_out(self, face_landmarks, image_shape):
        """Detect if tongue is sticking out"""
        # Upper lip center (13) and lower lip center (14)
        upper_lip = face_landmarks.landmark[13]
        lower_lip = face_landmarks.landmark[14]

        # Calculate mouth opening
        mouth_opening = abs(upper_lip.y - lower_lip.y)

        # Tongue detection threshold
        return mouth_opening > 0.04

    def detect_eyes_closed(self, face_landmarks):
        """Detect if both eyes are closed"""
        # Left eye landmarks - vertical distance
        left_eye_top = face_landmarks.landmark[159]
        left_eye_bottom = face_landmarks.landmark[145]
        left_eye_ratio = abs(left_eye_top.y - left_eye_bottom.y)

        # Right eye landmarks - vertical distance
        right_eye_top = face_landmarks.landmark[386]
        right_eye_bottom = face_landmarks.landmark[374]
        right_eye_ratio = abs(right_eye_top.y - right_eye_bottom.y)

        # Stricter threshold - eyes need to be more closed to trigger
        # Reduced threshold means eyes must be more tightly closed
        threshold = 0.007  # Much stricter (was 0.012)

        return left_eye_ratio < threshold and right_eye_ratio < threshold

    def detect_peace_sign(self, hand_landmarks):
        """Detect peace/victory sign (index and middle finger up)"""
        # Get finger tip and base positions
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]
        ring_tip = hand_landmarks.landmark[16]
        pinky_tip = hand_landmarks.landmark[20]

        # Get palm base
        wrist = hand_landmarks.landmark[0]

        # Check if index and middle fingers are up
        index_up = index_tip.y < hand_landmarks.landmark[6].y
        middle_up = middle_tip.y < hand_landmarks.landmark[10].y
        ring_down = ring_tip.y > hand_landmarks.landmark[14].y
        pinky_down = pinky_tip.y > hand_landmarks.landmark[18].y

        return index_up and middle_up and ring_down and pinky_down

    def detect_thumbs_up(self, hand_landmarks):
        """Detect thumbs up gesture"""
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]
        ring_tip = hand_landmarks.landmark[16]
        pinky_tip = hand_landmarks.landmark[20]

        # Check if thumb is up and other fingers are down
        thumb_up = thumb_tip.y < hand_landmarks.landmark[2].y
        fingers_down = (index_tip.y > hand_landmarks.landmark[6].y and
                       middle_tip.y > hand_landmarks.landmark[10].y and
                       ring_tip.y > hand_landmarks.landmark[14].y)

        return thumb_up and fingers_down

    def detect_open_palm(self, hand_landmarks):
        """Detect open palm (all fingers extended)"""
        tips = [4, 8, 12, 16, 20]  # Thumb, index, middle, ring, pinky tips
        bases = [2, 6, 10, 14, 18]

        extended_count = 0
        for tip, base in zip(tips, bases):
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[base].y:
                extended_count += 1

        return extended_count >= 4

    def detect_fist(self, hand_landmarks):
        """Detect closed fist (all fingers curled)"""
        # Get reference points
        wrist = hand_landmarks.landmark[0]
        palm_center = hand_landmarks.landmark[9]  # Middle finger base
        thumb_tip = hand_landmarks.landmark[4]

        # Calculate palm-to-wrist distance as reference
        palm_to_wrist = ((palm_center.x - wrist.x)**2 +
                        (palm_center.y - wrist.y)**2)**0.5

        # Check if fingertips are close to palm (curled)
        tips = [8, 12, 16, 20]  # Index, middle, ring, pinky tips
        curled_count = 0

        for tip_idx in tips:
            tip = hand_landmarks.landmark[tip_idx]
            # Distance from fingertip to palm center
            tip_to_palm = ((tip.x - palm_center.x)**2 +
                          (tip.y - palm_center.y)**2)**0.5

            # Balanced threshold - not too strict, not too loose
            if tip_to_palm < palm_to_wrist * 1.0:  # Fingers within palm-wrist distance
                curled_count += 1

        # Also check thumb isn't extended (prevents thumbs up false positive)
        thumb_to_palm = ((thumb_tip.x - palm_center.x)**2 +
                        (thumb_tip.y - palm_center.y)**2)**0.5
        thumb_curled = thumb_to_palm < palm_to_wrist * 1.3

        # Fist: At least 3 fingers curled AND thumb not extended
        return curled_count >= 3 and thumb_curled

    def detect_heart_gesture(self, hand_landmarks_list):
        """Detect heart shape made with both hands"""
        # Need exactly 2 hands
        if len(hand_landmarks_list) != 2:
            return False

        hand1 = hand_landmarks_list[0]
        hand2 = hand_landmarks_list[1]

        # Get key landmarks for both hands
        # Index finger tips and thumb tips are used to form the heart
        thumb1_tip = hand1.landmark[4]
        index1_tip = hand1.landmark[8]
        thumb2_tip = hand2.landmark[4]
        index2_tip = hand2.landmark[8]

        # Get wrist positions to determine left/right hand
        wrist1 = hand1.landmark[0]
        wrist2 = hand2.landmark[0]

        # Calculate distances between key points
        # For a heart: thumbs should be close together (top of heart)
        # and index fingers should be close together (bottom of heart)
        thumb_distance = ((thumb1_tip.x - thumb2_tip.x)**2 +
                         (thumb1_tip.y - thumb2_tip.y)**2)**0.5

        index_distance = ((index1_tip.x - index2_tip.x)**2 +
                         (index1_tip.y - index2_tip.y)**2)**0.5

        # Calculate hand separation (wrists)
        wrist_distance = ((wrist1.x - wrist2.x)**2 +
                         (wrist1.y - wrist2.y)**2)**0.5

        # Heart shape characteristics:
        # 1. Index fingers are close together (forming top curves of heart)
        # 2. Thumbs are close together (meeting at bottom point of heart)
        # 3. Wrists are reasonably separated (hands are in different positions)
        # 4. Index fingers should be higher than thumbs (proper heart orientation)

        # Check if index fingers are close (top of heart)
        indexes_close = index_distance < 0.12  # Adjust threshold as needed

        # Check if thumbs are close (bottom point of heart)
        thumbs_close = thumb_distance < 0.10  # Adjust threshold as needed

        # Check if hands are properly separated
        hands_separated = wrist_distance > 0.15

        # Check vertical alignment - index fingers should be HIGHER than thumbs
        indexes_higher = (index1_tip.y < thumb1_tip.y and index2_tip.y < thumb2_tip.y)

        # Additional check: middle of index fingers should be roughly aligned with middle of thumbs
        index_midpoint_y = (index1_tip.y + index2_tip.y) / 2
        thumb_midpoint_y = (thumb1_tip.y + thumb2_tip.y) / 2
        vertical_spread = abs(index_midpoint_y - thumb_midpoint_y)
        good_vertical_spread = 0.05 < vertical_spread < 0.25

        return (thumbs_close and indexes_close and hands_separated and
                indexes_higher and good_vertical_spread)

    def process_frame(self, frame):
        """Process a single frame and detect gestures"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, _ = frame.shape

        detected_gesture = None

        # Process face landmarks
        face_results = self.face_mesh.process(rgb_frame)
        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                # Draw face mesh (only if enabled)
                if self.show_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame, face_landmarks, self.mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=self.mp_drawing.DrawingSpec(
                            color=(0, 255, 0), thickness=1, circle_radius=1
                        )
                    )

                # Detect facial expressions
                if self.detect_tongue_out(face_landmarks, (h, w)):
                    detected_gesture = 'tongue_out'
                elif self.detect_eyes_closed(face_landmarks):
                    detected_gesture = 'eyes_closed'

        # Process hand landmarks
        hand_results = self.hands.process(rgb_frame)
        if hand_results.multi_hand_landmarks:
            # First, check for heart gesture (requires 2 hands)
            if len(hand_results.multi_hand_landmarks) == 2 and not detected_gesture:
                if self.detect_heart_gesture(hand_results.multi_hand_landmarks):
                    detected_gesture = 'heart'

            # Draw hand landmarks for all detected hands
            for hand_landmarks in hand_results.multi_hand_landmarks:
                # Draw hand landmarks (only if enabled)
                if self.show_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2),
                        self.mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=2)
                    )

                # Detect single-hand gestures (only if no gesture detected yet)
                if not detected_gesture:
                    # Check specific gestures first (peace, thumbs, palm)
                    if self.detect_peace_sign(hand_landmarks):
                        detected_gesture = 'peace_sign'
                    elif self.detect_thumbs_up(hand_landmarks):
                        detected_gesture = 'thumbs_up'
                    elif self.detect_open_palm(hand_landmarks):
                        detected_gesture = 'open_palm'
                    # Check fist last (only if no other gesture matched)
                    elif self.detect_fist(hand_landmarks):
                        detected_gesture = 'fist'

        # Update current reaction
        if detected_gesture:
            self.current_reaction = detected_gesture
            self.last_detection_time = time.time()
        elif time.time() - self.last_detection_time > 1.0:
            # Return to default after 1 second of no detection
            self.current_reaction = 'default'

        # Add gesture label to camera feed
        gesture_text = self.current_reaction.replace('_', ' ').title()
        cv2.putText(frame, f"Gesture: {gesture_text}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return frame

    def get_reaction_image(self):
        """Get the current reaction image (handles both static and animated GIFs)"""
        reaction_data = self.reactions.get(self.current_reaction, self.reactions['default'])

        if isinstance(reaction_data, tuple):
            frames_or_image, is_gif = reaction_data

            if is_gif and frames_or_image:
                # Animated GIF: cycle through frames
                frame_count = len(frames_or_image)
                frame_index = int(time.time() * 10) % frame_count  # 10 FPS
                frame = frames_or_image[frame_index]

                # Convert RGB (imageio) to BGR (OpenCV)
                if len(frame.shape) == 3 and frame.shape[2] == 3:
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                elif len(frame.shape) == 3 and frame.shape[2] == 4:
                    # RGBA to BGR
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

                return cv2.resize(frame, (640, 480))
            else:
                # Static image
                return frames_or_image.copy()

        # Fallback to default
        return self.create_default_image()

    def run(self):
        """Main loop to run the gesture detector"""
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open webcam!")
            return

        print("Gesture Detector Started!")
        print("\nControls:")
        print("  Press 'L' to toggle landmarks (face mesh and hand skeleton)")
        print("  Press 'Q' to quit")
        print("\nSupported Gestures:")
        print("  - Stick tongue out")
        print("  - Close eyes")
        print("  - Peace sign")
        print("  - Thumbs up")
        print("  - Open palm")
        print("  - Fist")
        print("  - Heart (both hands)")
        print(f"\nLandmarks: {'ON' if self.show_landmarks else 'OFF'}")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)

            # Process the frame
            processed_frame = self.process_frame(frame)

            # Get reaction image
            reaction_image = self.get_reaction_image()

            # Display windows
            cv2.imshow('Gesture Detector - Camera Feed', processed_frame)
            cv2.imshow('Reaction', reaction_image)

            # Check for keyboard input
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                print("Shutting down...")
                break
            elif key == ord('l'):
                self.show_landmarks = not self.show_landmarks
                status = "ON" if self.show_landmarks else "OFF"
                print(f"Landmarks: {status}")

        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        self.face_mesh.close()
        self.hands.close()


def main():
    """Entry point"""
    # Avoid printing non-ANSI characters which can raise UnicodeEncodeError on Windows CMD
    print("Starting Gesture Detector...")
    detector = GestureDetector()
    detector.run()


if __name__ == "__main__":
    main()
