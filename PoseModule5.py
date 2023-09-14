#/// Mediapipe
#/// Modified from :-
#/// Mediapipe, 2023. Pose landmark detection guide [online]. Google for Developers.
#/// [Accessed 14 Aug 2023]. Available from: https://developers.google.com/mediapipe/solutions/vision/pose_landmarker
import cv2
import mediapipe as mp
import time
import math


class BodyPoseAnalyzer:
    """
    This class uses the MediaPipe library to analyze and visualize body poses.
    """

    def __init__(self, mode=False, upper_body_only=False, smooth=True,
                 min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """
        Initializes the pose analyzer with the provided parameters.
        """
        self.mode = mode
        self.upper_body_only = upper_body_only
        self.smooth = smooth
        self.min_tracking_confidence = min_tracking_confidence
        self.min_detection_confidence = min_detection_confidence

        self.drawing_utils = mp.solutions.drawing_utils
        self.pose_utils = mp.solutions.pose
        self.pose_model = self.pose_utils.Pose(self.mode, self.upper_body_only, self.smooth,
                                               min_detection_confidence=self.min_detection_confidence,
                                               min_tracking_confidence=self.min_tracking_confidence)

    def get_pose(self, img, draw=True):
        """
        Processes the image to find pose landmarks.
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose_model.process(img_rgb)
        if self.results.pose_landmarks and draw:
            self.drawing_utils.draw_landmarks(img, self.results.pose_landmarks, self.pose_utils.POSE_CONNECTIONS)
            cv2.putText(img, f"Detection Confidence: {self.min_detection_confidence}", (10, img.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        return img

    def get_landmark_positions(self, img, draw=True):
        """
        Returns the landmarks found in the given image.
        """
        landmarks = []
        if self.results.pose_landmarks:
            for idx, landmark in enumerate(self.results.pose_landmarks.landmark):
                h, w, _ = img.shape
                x, y = int(landmark.x * w), int(landmark.y * h)
                landmarks.append([idx, x, y, landmark.visibility])
                if draw:
                    color = (0, int(255 * (1 - landmark.visibility)), int(255 * landmark.visibility))
                    size = int(5 * landmark.visibility)
                    cv2.circle(img, (x, y), size, color, cv2.FILLED)
        return landmarks

    def calculate_angle(self, img, point1, point2, point3, landmarks, draw=True):
        """
        Calculates the angle between three landmarks.
        """
        x1, y1 = landmarks[point1][1:3]
        x2, y2 = landmarks[point2][1:3]
        x3, y3 = landmarks[point3][1:3]

        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360

        if draw:
            lines = [(x1, y1, x2, y2), (x3, y3, x2, y2)]
            for line in lines:
                cv2.line(img, (line[0], line[1]), (line[2], line[3]), (255, 255, 255), 3)

            for point in [(x1, y1), (x2, y2), (x3, y3)]:
                cv2.circle(img, point, 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, point, 15, (0, 0, 255), 2)

            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        return angle


def main():
    """
    Main function to run the body pose analyzer.
    """
    cap = cv2.VideoCapture(0)
    prev_time = 0
    analyzer = BodyPoseAnalyzer()

    while True:
        success, frame = cap.read()
        frame = analyzer.get_pose(frame)
        landmarks = analyzer.get_landmark_positions(frame, draw=False)

        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        cv2.putText(frame, f"FPS: {int(fps)}", (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow("Body Pose Analysis", frame)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
