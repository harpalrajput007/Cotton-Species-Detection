# Cotton Species Detection App 🌿

This is a Streamlit-based web application designed for farmers to detect cotton species from images using a YOLOv8 model. The app identifies the species, displays detailed information about it, provides a crop calendar with monthly tasks, and shares a fun fact about cotton. The UI features a clean design with styled cards, a cotton field background, and a user-friendly interface.

## Features

- **Image-Based Species Detection**: Upload an image of a cotton plant to detect its species using a pre-trained YOLOv8 model.
- **Species Information**: Displays details about the detected species, including origin, traits, care tips, use cases, and a bonus fact.
- **Crop Calendar**: Provides a monthly task list for the detected species to guide farmers through the growing season.
- **Fun Fact**: Shares a random educational fact about cotton.
- **Responsive UI**: Styled with a green theme, featuring cards with light green backgrounds, green borders, rounded corners, and shadows.

## Screenshots

![Screenshot 2025-04-23 192712](https://github.com/user-attachments/assets/f8351407-84a8-4318-94fe-25e0d90e2f1b)
![Screenshot 2025-04-23 192613](https://github.com/user-attachments/assets/c1162d83-ae50-438b-9a85-65f2b5af3971)
![Screenshot 2025-04-23 192809](https://github.com/user-attachments/assets/31f427d0-ef71-44e2-8a50-e23cfc05cc83)
![Screenshot 2025-04-23 192804](https://github.com/user-attachments/assets/d2c5c27b-5a89-43f8-af06-fb01eda5191e)
![Screenshot 2025-04-23 192753](https://github.com/user-attachments/assets/02ff6e81-cde2-4621-a6fa-6a58f5c121b3)
![Screenshot 2025-04-23 192744](https://github.com/user-attachments/assets/b4cd5b3e-3e88-45de-9e48-a01530c1cef6)
![Screenshot 2025-04-23 192734](https://github.com/user-attachments/assets/ceab128f-1e27-41d6-a45f-93284b3bded4)


## Prerequisites

Before running the app, ensure you have the following:

- **Python 3.8+**: The app is built using Python.
- **Required Files**:
  - `last.pt`: Pre-trained YOLOv8 model file for cotton species detection.
  - `cotton_bg.jpg`: Background image for the app (a cotton field image).
- **Hardware**: A computer with internet access to run the Streamlit server and view the app in a browser.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/cotton-species-detection.git
   cd cotton-species-detection

2. **Install Dependencies**: Install the required Python libraries using pip:

   ```bash
   pip install streamlit pillow opencv-python numpy ultralytics
