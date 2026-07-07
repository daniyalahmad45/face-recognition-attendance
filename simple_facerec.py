import face_recognition
import cv2
import os
import glob
import numpy as np
import config


class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

        # Resize frame for faster speed (higher than before to preserve detail for far faces)
        self.frame_resizing = 0.35

    def load_encoding_images(self, images_path):
        """
        Load encoding images from path
        :param images_path:
        :return:
        """
        images_path = glob.glob(os.path.join(images_path, "*.*"))

        print("{} encoding images found.".format(len(images_path)))

        # Store image encoding and names
        for img_path in images_path:
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            basename = os.path.basename(img_path)
            filename = os.path.splitext(basename)[0]

            # Strip numbered suffix so "Daniyal_1", "Daniyal_2" all map to "Daniyal"
            name = filename.split("_")[0]

            encodings = face_recognition.face_encodings(rgb_img)
            if not encodings:
                print(f"Warning: no face found in {basename}, skipping.")
                continue

            img_encoding = encodings[0]

            # Store name and encoding
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(name)

        print("Encoding images loaded")

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(
            frame,
            (0, 0),
            fx=self.frame_resizing,
            fy=self.frame_resizing
        )

        rgb_small_frame = cv2.cvtColor(
            small_frame,
            cv2.COLOR_BGR2RGB
        )

        face_locations = face_recognition.face_locations(
            rgb_small_frame,
            number_of_times_to_upsample=2,
            model="hog"
        )
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame,
            face_locations
        )

        face_names = []

        for face_encoding in face_encodings:
            name = "Unknown"

            if self.known_face_encodings:
                matches = face_recognition.compare_faces(
                    self.known_face_encodings,
                    face_encoding,
                    tolerance=config.FACE_RECOGNITION_TOLERANCE
                )

                face_distances = face_recognition.face_distance(
                    self.known_face_encodings,
                    face_encoding
                )

                best_match_index = np.argmin(face_distances)

                if matches[best_match_index] and face_distances[best_match_index] < config.FACE_RECOGNITION_TOLERANCE:
                    name = self.known_face_names[best_match_index]

            face_names.append(name)

        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing

        return face_locations.astype(int), face_names