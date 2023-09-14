#/// Mediapipe
#/// Modified from :-
#/// Mediapipe, 2023. Pose landmark detection guide [online]. Google for Developers.
#/// [Accessed 14 Aug 2023]. Available from: https://developers.google.com/mediapipe/solutions/vision/pose_landmarker
import cv2
import numpy as np
import time
import PoseModule5 as pm


class PoseEstimator:
    """
    Class responsible for estimating the pose from an image and determining jump exercise repetitions.
    """

    def __init__(self):
        """Initializes the pose detector and other necessary attributes."""
        self.pose_detector = pm.BodyPoseAnalyzer()
        self.previous_time = 0
        self.direction = 0  # 0: starting position, 1: legs apart and arms raised
        self.repetitions = 0

    def get_hand_position(self, landmarks):
        """
        Returns the y-coordinates of the left and right wrists.

        Args:
        - landmarks (list): List of landmark positions.

        Returns:
        - tuple: y-coordinates of left and right wrists.
        """
        return landmarks[15][1], landmarks[16][1]

    def get_ankle_distance(self, landmarks):
        """
        Calculates the distance between left and right ankles.

        Args:
        - landmarks (list): List of landmark positions.

        Returns:
        - float: Distance between the ankles.
        """
        left_ankle, right_ankle = landmarks[27], landmarks[28]
        return ((right_ankle[0] - left_ankle[0]) ** 2 + (right_ankle[1] - left_ankle[1]) ** 2) ** 0.5

    def process_image(self, image):
        """
        Processes the image to detect pose and compute repetitions based on the estimated pose.

        Args:
        - image (np.ndarray): The image/frame to process.

        Returns:
        - np.ndarray: Processed image with overlaid details.
        """
        image = self.pose_detector.get_pose(image, False)
        landmarks = self.pose_detector.get_landmark_positions(image, False)

        if landmarks:
            left_wrist_y, right_wrist_y = self.get_hand_position(landmarks)
            ankle_distance = self.get_ankle_distance(landmarks)
            # Check conditions for detecting jump repetitions
            self.detect_jump_repetition(left_wrist_y, right_wrist_y, ankle_distance)

            self.draw_workout_info(image, ankle_distance)

        return image

    def detect_jump_repetition(self, left_wrist_y, right_wrist_y, ankle_distance):
        """Determines jump repetitions based on the wrist and ankle positions."""
        if ankle_distance > 150 and left_wrist_y < 300 and right_wrist_y < 300:
            if self.direction == 0:
                self.direction = 1
        elif ankle_distance < 100 and left_wrist_y > 400 and right_wrist_y > 400:
            if self.direction == 1:
                self.direction = 0
                self.repetitions += 1

    def draw_workout_info(self, image, ankle_distance):
        """
        Draws the workout details, such as repetitions and jump status, on the image.

        Args:
        - image (np.ndarray): Image to draw on.
        - ankle_distance (float): Distance between the ankles.
        """
        # Visualization based on ankle distance
        percentage = np.interp(ankle_distance, (50, 300), (0, 100))
        bar_position = np.interp(ankle_distance, (50, 300), (650, 100))
        bar_color = self.get_bar_color(percentage)

        cv2.rectangle(image, (1100, 100), (1175, 650), bar_color, -1)
        cv2.rectangle(image, (1100, int(bar_position)), (1175, 650), (255, 255, 255), cv2.FILLED)
        cv2.putText(image, f'{int(percentage)} %', (1080, 75), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 4)
        cv2.putText(image, f'Reps: {int(self.repetitions)}', (50, 700), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5,
                    cv2.LINE_AA)

        # Feedback on the current exercise status
        if self.direction == 1:
            cv2.putText(image, "Keep Going!", (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4, cv2.LINE_AA)
        else:
            cv2.putText(image, "Jump!", (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4, cv2.LINE_AA)

    def get_bar_color(self, percentage):
        """Determines the color of the progress bar based on the jump status."""
        if percentage == 100:
            if self.direction == 0:
                self.repetitions += 0.5
                self.direction = 1
            return (0, 255, 0)
        if percentage == 0:
            if self.direction == 1:
                self.repetitions += 0.5
                self.direction = 0
            return (0, 255, 0)
        return (80, 78, 255)

    def calculate_fps(self, image):
        """Calculates the frames per second and displays it on the image."""
        current_time = time.time()
        fps = 1 / (current_time - self.previous_time)
        self.previous_time = current_time
        cv2.putText(image, f'FPS: {int(fps)}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4, cv2.LINE_AA)


def main():
    """Main function to initialize the webcam stream and process each frame."""
    cap = cv2.VideoCapture(0)
    estimator = PoseEstimator()

    while True:
        success, frame = cap.read()
        frame = cv2.resize(frame, (1280, 720))
        processed_image = estimator.process_image(frame)
        estimator.calculate_fps(processed_image)

        cv2.imshow("Workout Tracking", processed_image)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()


