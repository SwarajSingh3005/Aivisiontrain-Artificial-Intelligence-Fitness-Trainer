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
    Class responsible for estimating the pose from an image, and providing details about arm angles
    and repetitions performed during a workout.
    """

    def __init__(self):
        """Initializes the pose detector and other necessary attributes."""
        self.pose_detector = pm.BodyPoseAnalyzer()
        self.previous_time = 0
        self.direction = 0
        self.repetitions = 0

    def get_right_arm_angle(self, image):
        """
        Computes the angle of the right arm based on the pose landmarks.

        Args:
        - image (np.ndarray): The image/frame to process.

        Returns:
        - float: The calculated angle.
        """
        landmarks = self.pose_detector.get_landmark_positions(image, False)
        return self.pose_detector.calculate_angle(image, 12, 14, 16, landmarks)

    def process_image(self, image):
        """
        Processes the image to detect pose and draw workout related information.

        Args:
        - image (np.ndarray): The image/frame to process.

        Returns:
        - np.ndarray: The processed image.
        """
        image = self.pose_detector.get_pose(image, False)
        landmarks = self.pose_detector.get_landmark_positions(image, False)

        if landmarks:
            angle = self.get_right_arm_angle(image)
            self.draw_workout_info(image, angle)

        return image

    def draw_workout_info(self, image, angle):
        """
        Draws the workout details (like repetitions and angle percentage) on the image.

        Args:
        - image (np.ndarray): The image on which to draw the details.
        - angle (float): The angle of the right arm.
        """
        percentage = np.interp(angle, (50, 160), (0, 100))
        bar_position = np.interp(angle, (50, 160), (650, 100))
        bar_color = self.get_bar_color(percentage)

        cv2.rectangle(image, (1100, 100), (1175, 650), bar_color, -1)
        cv2.rectangle(image, (1100, int(bar_position)), (1175, 650), (255, 255, 255), cv2.FILLED)
        cv2.putText(image, f'{int(percentage)} %', (1080, 75), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 4)
        cv2.putText(image, f'Reps: {int(self.repetitions)}', (50, 700), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5,
                    cv2.LINE_AA)

    def get_bar_color(self, percentage):
        """
        Determines the color of the progress bar based on the current angle percentage.

        Args:
        - percentage (float): The angle percentage.

        Returns:
        - tuple: The color (BGR) for the progress bar.
        """
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
        """
        Calculates the frames per second and draws it on the image.

        Args:
        - image (np.ndarray): The image on which to draw the FPS.
        """
        current_time = time.time()
        fps = 1 / (current_time - self.previous_time)
        self.previous_time = current_time
        cv2.putText(image, f'FPS: {int(fps)}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4, cv2.LINE_AA)


def main():
    """Main function to capture video feed, process it, and display the processed frames."""
    cap = cv2.VideoCapture(0)
    estimator = PoseEstimator()

    while True:
        success, frame = cap.read()
        if not success:
            break
        frame = cv2.resize(frame, (1280, 720))
        processed_image = estimator.process_image(frame)
        estimator.calculate_fps(processed_image)

        cv2.imshow("Workout Tracking", processed_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

