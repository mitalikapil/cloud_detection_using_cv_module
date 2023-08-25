import cv2
import numpy as np
import math

# Load the map image
map_image_path = "picture1.png"
map_image = cv2.imread(map_image_path)
image_height, image_width, _ = map_image.shape


# Cloud Detection
def detect_clouds(image_area):
    gray_image = cv2.cvtColor(image_area, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)
    cloud_pixels = np.sum(thresholded == 255)
    total_pixels = thresholded.size
    cloud_presence_percentage = (cloud_pixels / total_pixels) * 100
    return cloud_presence_percentage


# Center point for concentric zones
center_x = 600
center_y = 500

# Number of concentric zones
num_zones = 10

# Number of sectors per zone
num_sectors = 8

# Radius increment between zones
radius_increment = 30

# Angle increment for sectors
angle_step = 360 / num_sectors

# Create a copy of the map image for visualization
output_map = map_image.copy()

for zone_number in range(num_zones):
    radius = radius_increment * (zone_number + 1)

    # Draw concentric circles and mark the zone number
    cv2.circle(output_map, (center_x, center_y), radius, (0, 0, 255), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(output_map, str(zone_number + 1), (center_x - 5, center_y + 5), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

    for sector_number in range(num_sectors):
        angle = sector_number * angle_step
        angle_rad = math.radians(angle)

        x1 = int(center_x + radius * np.cos(angle_rad))
        y1 = int(center_y + radius * np.sin(angle_rad))
        x2 = int(center_x + radius * np.cos(angle_rad + math.radians(angle_step)))
        y2 = int(center_y + radius * np.sin(angle_rad + math.radians(angle_step)))

        # Calculate cloud presence in the current sector
        sector_image = map_image[min(y1, y2):max(y1, y2), min(x1, x2):max(x1, x2)]

        if sector_image.size == 0:
            print(f"Zone {zone_number + 1} - Sector {sector_number + 1}: Empty sector image!")
        else:
            cloud_coverage = detect_clouds(sector_image)
            print(f"Zone {zone_number + 1} - Sector {sector_number + 1}: Cloud coverage {cloud_coverage:.2f}%")

            # Draw lines from center to the edge of the sector
            cv2.line(output_map, (center_x, center_y), (x1, y1), (0, 0, 255), 2)

            # Draw sector number within the sector
            sector_label = f"{zone_number + 1}.{sector_number + 1:02}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            text_size = cv2.getTextSize(sector_label, font, 0.5, 1)[0]
            text_x = (x1 + x2 - text_size[0]) // 2
            text_y = (y1 + y2 + text_size[1]) // 2
            cv2.putText(output_map, sector_label, (text_x, text_y), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

# Save the final output image
output_image_path = "final_output_map_with_clouds.png"
cv2.imwrite(output_image_path, output_map)
