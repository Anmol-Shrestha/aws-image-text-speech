# Style Guide: Pictorial Translate (3D Neumorphic / Glassmorphic Aesthetic)

This style guide outlines the visual language and UI components for the "Pictorial Translate" application. The goal is a high-end, portfolio-ready experience that feels tactile, creative, and futuristic.

## 1. Design Philosophy: "Physical Digital"
* **Tactility:** Use soft shadows, inner glows, and 3D depth to make elements feel like physical objects.
* **Clarity:** Despite the creative 3D vibe, the user flow must remain intuitive (Upload -> Process -> Display).
* **Vibrancy:** Use a "Dark Mode" base with glowing accent colors to simulate high-tech equipment.

## 2. Color Palette
* **Surface (Deep Space):** `#0F172A` (Rich Navy/Black)
* **Elevated Card (Frosted Glass):** `rgba(30, 41, 59, 0.7)`
* **Accent 1 (Electric Violet):** `#8B5CF6`
* **Accent 2 (Cyan Glow):** `#06B6D4`
* **Success/Text:** `#F8FAFC`

## 3. Typography
* **Primary Font:** Inter or Geist (Clean, modern sans-serif).
* **Header (H1):** `font-weight: 800; letter-spacing: -0.05em; background: linear-gradient(to right, #8B5CF6, #06B6D4); -webkit-background-clip: text;`
* **Mono (Code/Translation):** JetBrains Mono (For the translated output).

## 4. UI Components & 3D Effects

### A. The "Floating" Upload Zone
* **Style:** Large container with `backdrop-filter: blur(12px)`.
* **3D Effect:** Use `box-shadow: 20px 20px 60px #05070a, -20px -20px 60px #192746;` to create a soft 3D protrusion.
* **Interaction:** On drag-over, the border should "glow" using an animated CSS gradient.

### B. Action Buttons
* **Base:** Deep violet gradient.
* **3D Effect:** Use a slight `transform: translateY(-2px)` on hover and `translateY(1px)` on click to simulate a physical button press. Add a sharp bottom border (`border-bottom: 4px solid #6D28D9`) for depth.

### C. Glassmorphic Output Cards
* **Layout:** Two-column split (Left: Original Image, Right: Translated Text).
* **Glass Effect:** Thin white border (opacity 0.1) and a subtle mesh gradient background.

## 5. Animation Logic
* **Processing State:** When "Translate" is clicked, use a scanning light beam effect (a horizontal line moving up and down the uploaded image).
* **Transitions:** Use `cubic-bezier(0.4, 0, 0.2, 1)` for all transforms to ensure smooth, organic movement.

## 6. Layout Specs
* **Header:** Centered, oversized, "Pictorial Translate" with a subtle text-shadow.
* **Main Container:** Max-width 1000px, centered with significant vertical padding.
