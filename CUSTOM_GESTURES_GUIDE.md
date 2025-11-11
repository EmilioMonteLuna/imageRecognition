# Custom Gestures Guide

Want to add your own gestures? This guide shows you how to extend the Gesture Detector with custom hand or face gestures.

## Quick Steps

1. **Add your detection function** to `main.py`
2. **Load your reaction image/GIF** in the `__init__` method
3. **Call your detector** in the `process_frame` method
4. **Test and tune** your gesture thresholds

## Example: Adding a "Rock On" 🤘 Gesture

### Step 1: Create the Detection Function

Add this function to the `GestureDetector` class in `main.py`:

```python
def detect_rock_on(self, hand_landmarks):
    """Detect rock on gesture (index and pinky up, others down)"""
    # Get finger tips and bases
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    middle_tip = hand_landmarks.landmark[12]
    ring_tip = hand_landmarks.landmark[16]
    pinky_tip = hand_landmarks.landmark[20]
    
    # Check if index and pinky are up, others down
    index_up = index_tip.y < hand_landmarks.landmark[6].y
    pinky_up = pinky_tip.y < hand_landmarks.landmark[18].y
    middle_down = middle_tip.y > hand_landmarks.landmark[10].y
    ring_down = ring_tip.y > hand_landmarks.landmark[14].y
    thumb_down = thumb_tip.y > hand_landmarks.landmark[2].y
    
    return index_up and pinky_up and middle_down and ring_down and thumb_down
```

### Step 2: Add Reaction Image Loading

In the `__init__` method, add your gesture to the `self.reactions` dictionary:

```python
self.reactions = {
    'heart': self.load_image('lovely.gif'),
    'tongue_out': self.load_image('tongue.gif'),
    'eyes_closed': self.load_image('closed_eyes.gif'),
    'peace_sign': self.load_image('peace.gif'),
    'thumbs_up': self.load_image('thumbs_up.gif'),
    'open_palm': self.load_image('open_palm.gif'),
    'fist': self.load_image('fist.gif'),
    'rock_on': self.load_image('rock_on.gif'),  # ← Add this line
    'default': (self.create_default_image(), False)
}
```

### Step 3: Add Detection Logic

In the `process_frame` method, add your gesture check in the single-hand detection section:

```python
# Detect single-hand gestures (only if no gesture detected yet)
if not detected_gesture:
    # Check specific gestures first (peace, thumbs, palm)
    if self.detect_peace_sign(hand_landmarks):
        detected_gesture = 'peace_sign'
    elif self.detect_thumbs_up(hand_landmarks):
        detected_gesture = 'thumbs_up'
    elif self.detect_rock_on(hand_landmarks):  # ← Add this line
        detected_gesture = 'rock_on'
    elif self.detect_open_palm(hand_landmarks):
        detected_gesture = 'open_palm'
    # Check fist last (only if no other gesture matched)
    elif self.detect_fist(hand_landmarks):
        detected_gesture = 'fist'
```

### Step 4: Add Your Image

Put your reaction image in the `assets/` folder:
- `assets/rock_on.gif` (or `.jpg`, `.png`)

### Step 5: Test and Tune

Run the app and test your gesture. If it's not detecting properly:

- **Too sensitive?** Make conditions stricter (use `<` instead of `<=`)
- **Not sensitive enough?** Make conditions more lenient
- **Wrong fingers detected?** Check the landmark numbers below

## Hand Landmark Reference

MediaPipe hand landmarks (useful for creating gestures):

```
Landmarks:
0  = Wrist
1-4  = Thumb (1=base, 4=tip)
5-8  = Index (5=base, 8=tip)
9-12 = Middle (9=base, 12=tip)
13-16= Ring (13=base, 16=tip)
17-20= Pinky (17=base, 20=tip)
```

**Key landmarks for gesture detection:**
- **Fingertips:** 4, 8, 12, 16, 20
- **Finger bases:** 2, 6, 10, 14, 18
- **Palm center:** 9 (middle finger base)

## Face Landmark Reference

For facial expressions, useful landmarks:

```
Eyes:
- Left eye top: 159, bottom: 145
- Right eye top: 386, bottom: 374

Mouth:
- Upper lip: 13
- Lower lip: 14
- Corners: 61, 291
```

## Tips for Good Gesture Detection

1. **Start simple** - Use basic up/down finger positions first
2. **Test in good lighting** - MediaPipe works best with clear hand visibility
3. **Use relative positions** - Compare fingertips to bases, not absolute coordinates
4. **Add gesture priority** - Put more specific gestures before general ones
5. **Consider hand orientation** - Some gestures work better from certain angles

## Two-Hand Gestures

For gestures requiring both hands (like the heart), check the existing `detect_heart_gesture` function as a template. Key points:

- Check `len(hand_landmarks_list) == 2`
- Calculate distances between corresponding landmarks
- Consider hand separation and positioning

## Example: Simple "Okay" Gesture 👌

```python
def detect_okay_sign(self, hand_landmarks):
    """Detect okay sign (thumb and index forming circle)"""
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    
    # Distance between thumb and index tips
    distance = ((thumb_tip.x - index_tip.x)**2 + 
                (thumb_tip.y - index_tip.y)**2)**0.5
    
    # Other fingers should be extended
    middle_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
    ring_up = hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y
    pinky_up = hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y
    
    # Thumb and index close together, other fingers up
    return distance < 0.05 and middle_up and ring_up and pinky_up
```

## Testing Your Gesture

1. Add print statements for debugging:
   ```python
   if self.detect_your_gesture(hand_landmarks):
       print("Your gesture detected!")  # Add this for testing
       detected_gesture = 'your_gesture'
   ```

2. Use the landmarks toggle (`L` key) to see hand points while testing

3. Adjust thresholds based on testing - start loose, then tighten

## Troubleshooting

**Gesture not detecting:**
- Check landmark numbers are correct
- Print values to see what's happening
- Make conditions less strict

**False positives:**
- Add more specific conditions
- Check for conflicting gestures
- Reorder detection priority

**Gesture too slow:**
- Reduce calculation complexity
- Cache expensive operations
- Use simpler math

---

Happy gesture creating! 🤘✌️👍
