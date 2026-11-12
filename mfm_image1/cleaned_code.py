import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import math

# Paths to the images
mfm_image_path_1 = "{}/AB2.png".format(os.getcwd())
mfm_image_path_2 = "{}/AB3.png".format(os.getcwd())
mask_image_path = "{}/AB1.png".format(os.getcwd())

# Paths to the images (update these paths)
mask_image_path = "AB1.png"

# Step 1: Load the mask image
mask_image = cv2.imread(mask_image_path, cv2.IMREAD_COLOR)  # Read in color for overlay

# Step 2: Convert the mask image to grayscale and threshold to create a binary mask
mask_image_gray = cv2.cvtColor(mask_image, cv2.COLOR_BGR2GRAY)
_, bit_mask = cv2.threshold(mask_image_gray, 128, 255, cv2.THRESH_BINARY)

# Step 3: Use distance transform to separate close regions
distance_transform = cv2.distanceTransform(bit_mask, cv2.DIST_L2, 5)
_, sure_fg = cv2.threshold(distance_transform, 0.249 * distance_transform.max(), 255, 0)

# Step 4: Find unknown regions (sure background)
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(bit_mask, sure_fg)

# Step 5: Marker labelling
_, markers = cv2.connectedComponents(sure_fg)

# Add one to all markers to distinguish from the background
markers = markers + 1

# Mark the unknown regions with zero
markers[unknown == 255] = 0

# Apply the watershed algorithm
mask_image_watershed = cv2.cvtColor(bit_mask, cv2.COLOR_GRAY2BGR)
cv2.watershed(mask_image_watershed, markers)

# Step 6: Create a blank image to visualize all bits with different colors
bits_visualization = np.zeros_like(mask_image)

# Generate a colormap using 'hsv' and map it to RGB values for each segment
num_labels = markers.max() - 1  # Subtracting one to exclude background

colormap = plt.colormaps.get_cmap("hsv")
colors = (colormap(np.linspace(0, 1, num_labels))[:, :3] * 255).astype(int)

# Assign a unique color to each bit and draw on the visualization image
for i in range(2, markers.max() + 1):  # Start from 2 to skip the background
    color = tuple(colors[i - 2].tolist())
    bits_visualization[markers == i] = color

# Step 7: Count the number of unique colors in the visualization (excluding black)
unique_colors = np.unique(bits_visualization.reshape(-1, bits_visualization.shape[2]), axis=0)
num_unique_colors = len([color for color in unique_colors if not np.all(color == [0, 0, 0])])
print(f"Number of unique colors in the segmented visualization: {num_unique_colors}")

# Step 8: Verify if the numbers match the expected count of 93
if num_unique_colors == 93:
    print("Successfully detected 93 unique segments.")
else:
    print(f"Mismatch detected! Expected 93 segments, but found {num_unique_colors} segments.")

# Step 9: Display the results
plt.figure(figsize=(15, 10))

# Original Bit-by-bit image
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(mask_image, cv2.COLOR_BGR2RGB))
plt.title("Original Bit-by-bit Image")
plt.axis('off')

# Bits Visualization with Different Colors
plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(bits_visualization, cv2.COLOR_BGR2RGB))
plt.title("Bits Segmentation Visualization")
plt.axis('off')

plt.tight_layout()
plt.show()

segmentation_output_path = "{}/bit_segmentation_visualization.png".format(os.getcwd())
cv2.imwrite(segmentation_output_path, bits_visualization)
print(f"Bit segmentation visualization saved at: {segmentation_output_path}")

# Directory to save the separated segments
output_dir = "{}/corrected_segments".format(os.getcwd())
os.makedirs(output_dir, exist_ok=True)

# Path to the "Bits Segmentation Visualization" image
segmentation_visualization_path = "bit_segmentation_visualization.png"  # Path to the segmentation visualization

# Step 1: Load the segmentation visualization
segmentation_visualization = cv2.imread(segmentation_visualization_path)
if segmentation_visualization is None:
    print("Segmentation visualization image could not be loaded.")
else:
    # Step 2: Convert to grayscale and create a binary mask for connected components
    segmentation_gray = cv2.cvtColor(segmentation_visualization, cv2.COLOR_BGR2GRAY)
    _, binary_mask = cv2.threshold(segmentation_gray, 1, 255, cv2.THRESH_BINARY)
    num_labels, labels_im = cv2.connectedComponents(binary_mask)
    print(f"Number of detected segments: {num_labels - 1}")

    # Step 3: Extract and save each segment individually
    for label in range(1, num_labels):  # Start from 1 to skip the background
        # Create a mask for the current segment
        segment_mask = np.zeros_like(binary_mask, dtype=np.uint8)
        segment_mask[labels_im == label] = 255

        # Find contours of the segment to get the bounding box
        contours, _ = cv2.findContours(segment_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            continue

        # Get the bounding box of the current segment
        x, y, w, h = cv2.boundingRect(contours[0])

        # Crop the segment using the bounding box
        cropped_segment = segmentation_visualization[y:y+h, x:x+w]

        # Save the cropped segment image
        segment_output_path = os.path.join(output_dir, f"segment_{label}.png")
        cv2.imwrite(segment_output_path, cropped_segment)
        print(f"Saved segment {label} to {segment_output_path}")

    # Step 4: Display one example segment to verify the output
    example_segment_path = os.path.join(output_dir, "segment_9.png")
    example_segment = cv2.imread(example_segment_path)

    if example_segment is not None:
        plt.figure(figsize=(6, 6))
        plt.imshow(cv2.cvtColor(example_segment, cv2.COLOR_BGR2RGB))
        plt.title("Example Segment (Segment 9)")
        plt.axis('off')
        plt.show()
    else:
        print("Example segment could not be loaded for verification.")

# Directory where the corrected segments are saved
corrected_segments_dir = "{}/corrected_segments".format(os.getcwd())

# Path to the original "Bits Segmentation Visualization" image
segmentation_visualization_path = "bit_segmentation_visualization.png"  # Path to the segmentation visualization

# Step 1: Load the original segmentation visualization to get the original dimensions
segmentation_visualization = cv2.imread(segmentation_visualization_path)
if segmentation_visualization is None:
    print("Segmentation visualization image could not be loaded.")
else:
    # Create a blank canvas for the reconstructed image
    reassembled_image = np.zeros_like(segmentation_visualization)

    # Step 2: Reassemble the image using the saved segments
    segment_files = sorted([f for f in os.listdir(corrected_segments_dir) if f.startswith("segment_") and f.endswith(".png")])

    # Loop over each saved segment file
    for segment_file in segment_files:
        # Extract the segment index from the file name
        segment_index = int(segment_file.split('_')[1].split('.')[0])
        segment_path = os.path.join(corrected_segments_dir, segment_file)

        # Load the saved segment
        segment = cv2.imread(segment_path, cv2.IMREAD_COLOR)

        if segment is None:
            print(f"Segment {segment_index} could not be loaded. Skipping...")
            continue

        # Step 3: Find the corresponding label positions in the original mask
        mask = (labels_im == segment_index).astype(np.uint8) * 255
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            print(f"No contours found for segment {segment_index}. Skipping...")
            continue

        # Get the bounding box of the current segment
        x, y, w, h = cv2.boundingRect(contours[0])

        # Resize the segment to fit within the original bounding box
        segment_resized = cv2.resize(segment, (w, h))

        # Place the resized segment back onto the reassembled image at the original position
        reassembled_image[y:y+h, x:x+w] = segment_resized

    # Step 4: Display the reassembled image
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(reassembled_image, cv2.COLOR_BGR2RGB))
    plt.title("Reconstructed Segmentation Image")
    plt.axis('off')
    plt.show()

    # Save the reassembled image
    reassembled_image_path = os.path.join(corrected_segments_dir, "reconstructed_segmentation_image.png")
    cv2.imwrite(reassembled_image_path, reassembled_image)
    print(f"Reconstructed segmentation image saved at: {reassembled_image_path}")

# Directory where the uniquely colored segments are saved
segmentation_dir = "{}/corrected_segments".format(os.getcwd())

# Path to the actual MFM image (AB3)
mfm_image_path_2 = "{}/AB2.png".format(os.getcwd())
mfm_image_2 = cv2.imread(mfm_image_path_2, cv2.IMREAD_GRAYSCALE)

# Path to the segmentation visualization used to identify regions
segmentation_visualization_path = "bit_segmentation_visualization.png"  # Assuming this is the correct path
segmentation_visualization = cv2.imread(segmentation_visualization_path)

# Directory to save the segmented bits from the MFM image
mfm_segment_output_dir = "{}/mfm_segments".format(os.getcwd())
os.makedirs(mfm_segment_output_dir, exist_ok=True)

# Step 1: Convert the segmentation visualization to grayscale and find connected components
segmentation_gray = cv2.cvtColor(segmentation_visualization, cv2.COLOR_BGR2GRAY)
_, binary_mask = cv2.threshold(segmentation_gray, 1, 255, cv2.THRESH_BINARY)
num_labels, labels_im = cv2.connectedComponents(binary_mask)

print(f"Number of detected unique segments: {num_labels - 1}")

# Step 2: Segment out the corresponding regions from the MFM image based on the unique labels
for label in range(1, num_labels):  # Start from 1 to skip the background
    # Create a mask for the current label
    segment_mask = (labels_im == label).astype(np.uint8) * 255

    # Use the mask to extract the corresponding region from the MFM image
    mfm_segment = cv2.bitwise_and(mfm_image_2, mfm_image_2, mask=segment_mask)

    # Find the bounding box of the non-zero region in the segment
    contours, _ = cv2.findContours(segment_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        x, y, w, h = cv2.boundingRect(contours[0])
        # Crop the segment to the bounding box to remove the background
        mfm_segment_cropped = mfm_segment[y:y+h, x:x+w]

        # Save the cropped MFM segment with the same index as the unique label
        mfm_segment_output_path = os.path.join(mfm_segment_output_dir, f"mfm_segment_{label}.png")
        cv2.imwrite(mfm_segment_output_path, mfm_segment_cropped)
        print(f"Saved cropped MFM segment {label} to {mfm_segment_output_path}")
    else:
        print(f"No contours found for segment {label}. Skipping...")

# Step 3: Verify that the number of segmented bits matches the number of unique segments
print(f"Number of segmented MFM bits: {num_labels - 1}")


# Directory where the MFM segments are saved
mfm_segments_dir = "{}/mfm_segments".format(os.getcwd())
# Directory to save the segments with directional arrows
output_dir = "{}/mfm_segments_with_directional_arrows".format(os.getcwd())
os.makedirs(output_dir, exist_ok=True)

# Counters for arrows pointing left and right
left_arrow_count = 0
right_arrow_count = 0

# Get the list of all segment files
segment_files = sorted([f for f in os.listdir(mfm_segments_dir) if f.startswith("mfm_segment_") and f.endswith(".png")])

# Step 1: Loop over each segment file
for segment_file in segment_files:
    # Extract segment index from the file name
    segment_index = int(segment_file.split('_')[2].split('.')[0])
    segment_path = os.path.join(mfm_segments_dir, segment_file)

    # Load the segment
    segment = cv2.imread(segment_path, cv2.IMREAD_COLOR)

    if segment is None:
        print(f"Segment {segment_index} could not be loaded. Skipping...")
        continue

    # Step 2: Convert the segment to grayscale and create a binary mask
    segment_gray = cv2.cvtColor(segment, cv2.COLOR_BGR2GRAY)

    # Step 3: Threshold to separate the bit from the black background
    _, bit_mask = cv2.threshold(segment_gray, 10, 255, cv2.THRESH_BINARY)

    # Step 4: Find the contours to calculate the orientation of the bit
    contours, _ = cv2.findContours(bit_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print(f"No contours found for segment {segment_index}. Skipping...")
        continue

    # Get the bounding box of the bit
    x, y, w, h = cv2.boundingRect(contours[0])
    bit_diagonal_length = int(np.sqrt(w ** 2 + h ** 2))

    # Set the arrow length to be a fraction of the bit diagonal (e.g., 75%)
    arrow_length = int(0.75 * bit_diagonal_length)

    # Fit an ellipse to find the orientation of the bit
    if len(contours[0]) >= 5:  # FitEllipse requires at least 5 points
        ellipse = cv2.fitEllipse(contours[0])
        center = (int(ellipse[0][0]), int(ellipse[0][1]))

        # Step 5: Find the brightest point within the bit
        # Mask the grayscale image to only include the bit region
        masked_segment = cv2.bitwise_and(segment_gray, segment_gray, mask=bit_mask)
        _, max_val, _, max_loc = cv2.minMaxLoc(masked_segment)
        brightest_point = max_loc

        # Calculate the vector from the center to the brightest point
        dx_brightest = brightest_point[0] - center[0]
        dy_brightest = brightest_point[1] - center[1]
        norm = math.sqrt(dx_brightest**2 + dy_brightest**2)
        if norm == 0:  # Prevent division by zero
            norm = 1
        dx_brightest = int((arrow_length / 2) * (dx_brightest / norm))
        dy_brightest = int((arrow_length / 2) * (dy_brightest / norm))

        # Calculate the start and end points of the arrow based on the brightest point direction
        start_point = (center[0] - dx_brightest, center[1] - dy_brightest)
        end_point = (center[0] + dx_brightest, center[1] + dy_brightest)

        # Step 6: Determine if the arrow points left or right
        arrow_direction = "Left" if dx_brightest < 0 else "Right"

        # Update the counters
        if arrow_direction == "Left":
            left_arrow_count += 1
        else:
            right_arrow_count += 1

        # Step 7: Draw the arrow on the segment
        segment_with_arrow = segment.copy()
        cv2.arrowedLine(segment_with_arrow, start_point, end_point, (255, 255, 255), 2, tipLength=0.2)

        # Step 8: Save the segment with the arrow to the output directory
        output_path = os.path.join(output_dir, f"mfm_segment_{segment_index}_with_arrow.png")
        cv2.imwrite(output_path, segment_with_arrow)

        print(f"Segment {segment_index} with arrow saved at: {output_path}")
    else:
        print(f"Not enough points to fit an ellipse for segment {segment_index}. Skipping...")

# Step 9: Print the results
print(f"Total arrows pointing right: {right_arrow_count}")
print(f"Total arrows pointing left: {left_arrow_count}")

# Determine the overall magnetic moment direction
overall_magnetic_moment = "Right" if right_arrow_count > left_arrow_count else "Left"
print(f"The overall magnetic moment direction is: {overall_magnetic_moment}")

# Directory where the MFM segments with arrows are saved
mfm_segments_with_arrows_dir = "{}/mfm_segments_with_directional_arrows".format(os.getcwd())
output_dir = "{}/reconstructed_image".format(os.getcwd())
os.makedirs(output_dir, exist_ok=True)

# Path to the original "Bits Segmentation Visualization" image
segmentation_visualization_path = "bit_segmentation_visualization.png"

# Load the original segmentation visualization to get the original dimensions
segmentation_visualization = cv2.imread(segmentation_visualization_path)
if segmentation_visualization is None:
    print("Segmentation visualization image could not be loaded.")
else:
    # Create a blank canvas for the reconstructed image
    reassembled_image = np.zeros_like(segmentation_visualization)

    # Convert to grayscale and find connected components in the segmentation visualization
    segmentation_gray = cv2.cvtColor(segmentation_visualization, cv2.COLOR_BGR2GRAY)
    _, binary_mask = cv2.threshold(segmentation_gray, 1, 255, cv2.THRESH_BINARY)
    num_labels, labels_im = cv2.connectedComponents(binary_mask)

    # Step 1: Loop over each segment based on the corrected segments
    for label in range(1, num_labels):
        # Find the corresponding MFM segment
        mfm_segment_path = os.path.join(mfm_segments_with_arrows_dir, f"mfm_segment_{label}_with_arrow.png")
        mfm_segment = cv2.imread(mfm_segment_path, cv2.IMREAD_COLOR)

        if mfm_segment is None:
            print(f"MFM Segment {label} could not be loaded. Skipping...")
            continue

        # Find the bounding box of the segment in the original mask
        mask = (labels_im == label).astype(np.uint8) * 255
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            print(f"No contours found for segment {label}. Skipping...")
            continue

        # Get the bounding box of the current segment
        x, y, w, h = cv2.boundingRect(contours[0])

        # Resize the MFM segment to fit within the original bounding box
        mfm_segment_resized = cv2.resize(mfm_segment, (w, h))

        # Place the resized MFM segment back onto the reassembled image at the original position
        reassembled_image[y:y+h, x:x+w] = mfm_segment_resized

        # # Step 2: Write the segment number on top of the bit
        # label_position = (x + w // 2, y + h // 2)
        # cv2.putText(reassembled_image, str(label), label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Step 3: Display the reassembled image
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(reassembled_image, cv2.COLOR_BGR2RGB))
    plt.title("Reconstructed MFM Image from Segments with Labels")
    plt.axis('off')
    plt.show()

 # Save the reassembled image
reassembled_image_path = os.path.join(output_dir, "reconstructed_mfm_image_with_directional_arrows.png")
cv2.imwrite(reassembled_image_path, reassembled_image)
print(f"Reconstructed MFM image with labels saved at: {reassembled_image_path}")
