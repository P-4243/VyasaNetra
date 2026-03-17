import math

# configure to your camera
HORIZONTAL_FOV_DEG = 62.0    # change to your camera's H-FOV if known (smartphone ~60-75)
ASSUMED_STEP_METERS = 0.6    # average human step length - adjust

def bbox_to_guidance(bbox, frame_size):
    """
    bbox: (x1,y1,x2,y2) in pixels from detector
    frame_size: (W,H)
    returns: dict with direction_text, angle_deg, distance_category, steps_instructions
    """
    W, H = frame_size
    x1,y1,x2,y2 = bbox
    cx = (x1 + x2) / 2.0
    cy = (y1 + y2) / 2.0
    bbox_w = x2 - x1
    bbox_h = y2 - y1

    # 1) Horizontal offset → percent from center (-0.5 .. +0.5)
    offset_percent = (cx - W/2) / (W/2)   # -1 left, +1 right
    # convert to angle
    angle_deg = offset_percent * (HORIZONTAL_FOV_DEG/2)

    # direction bucket
    if abs(offset_percent) < 0.12:
        direction_text = "ahead of you"
    elif offset_percent < 0:
        direction_text = "to your left"
    else:
        direction_text = "to your right"

    # 2) Distance estimate by bbox size (heuristic)
    # choose thresholds empirical — may need tuning per camera
    bbox_area_ratio = (bbox_w * bbox_h) / (W * H)
    # fallback: use bbox_h relative
    height_ratio = bbox_h / H

    if height_ratio > 0.35 or bbox_area_ratio > 0.12:
        distance_category = "very close"
        approx_meters = 0.5
    elif height_ratio > 0.18 or bbox_area_ratio > 0.03:
        distance_category = "near"
        approx_meters = 1.5
    else:
        distance_category = "far"
        approx_meters = 3.0

    # compute rough number of steps (conservative)
    steps = max(1, int(round(approx_meters / ASSUMED_STEP_METERS)))

    # turn instruction: if angle > ~15°, suggest turning left/right
    turn_angle = angle_deg
    if abs(turn_angle) < 10:
        turn_instruction = ""
    elif turn_angle < 0:
        turn_instruction = f"turn {int(abs(turn_angle))} degrees to your left"
    else:
        turn_instruction = f"turn {int(abs(turn_angle))} degrees to your right"

    # forward instruction
    forward_instruction = f"then walk {steps} step{'s' if steps>1 else ''} forward"

    # Build readable guidance
    guidance_lines = []
    guidance_lines.append(f"Object is {direction_text}.")
    guidance_lines.append(f"Distance: {distance_category} (about {approx_meters:.1f} meters).")
    if turn_instruction:
        guidance_lines.append(turn_instruction + ", " + forward_instruction)
    else:
        guidance_lines.append(forward_instruction)

    guidance_text = " ".join(guidance_lines)

    return {
        "angle_deg": angle_deg,
        "direction_text": direction_text,
        "distance_category": distance_category,
        "approx_meters": approx_meters,
        "steps": steps,
        "turn_instruction": turn_instruction,
        "guidance_text": guidance_text
    }
