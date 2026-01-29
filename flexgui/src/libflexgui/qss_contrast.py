from PyQt6.QtGui import QColor

def get_luminance(color: QColor) -> float:
	"""
	Calculates the relative luminance of a QColor object according to WCAG 2.1.
	The color input should have RGB values in the range [0, 255].
	Returns a value between 0.0 (black) and 1.0 (white).
	"""
	# Normalize RGB values to the range [0, 1]
	r = color.redF()
	g = color.greenF()
	b = color.blueF()

	# Apply the gamma correction for sRGB color space
	if r <= 0.03928:
		r_linear = r / 12.92
	else:
		r_linear = ((r + 0.055) / 1.055) ** 2.4
	
	if g <= 0.03928:
		g_linear = g / 12.92
	else:
		g_linear = ((g + 0.055) / 1.055) ** 2.4

	if b <= 0.03928:
		b_linear = b / 12.92
	else:
		b_linear = ((b + 0.055) / 1.055) ** 2.4

	# Calculate relative luminance using the WCAG formula
	luminance = 0.2126 * r_linear + 0.7152 * g_linear + 0.0722 * b_linear
	return luminance

def calculate_contrast_ratio(color1: QColor, color2: QColor) -> float:
	"""
	Calculates the WCAG contrast ratio between two QColor objects.
	Returns a ratio between 1.0 and 21.0.
	"""
	l1 = get_luminance(color1)
	l2 = get_luminance(color2)

	# Ensure L1 is the lighter color and L2 is the darker color
	if l1 >= l2:
		lighter = l1
		darker = l2
	else:
		lighter = l2
		darker = l1

	# Apply the contrast ratio formula
	contrast = (lighter + 0.05) / (darker + 0.05)
	return round(contrast, 2)

