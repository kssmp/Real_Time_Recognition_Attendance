# Real-Time Attendance Recognition System using Firebase & Face-recognition Library

The Real-Time Attendance Recognition System utilizes Firebase's real-time storage and database capabilities to facilitate efficient and accurate attendance recording. It uses thte face-recognition library for correctly recognizing and manipulatingfaces using the dlib's deep learning algorithm. This system allows you to track attendance in real-time, record the last attendance time, and maintain a count of the number of attendances for each individual.

![Screenshot 2023-08-08 at 9 35 08 PM](https://github.com/kssmp/Real_Time_Recognition_Attendance/assets/115448106/4a8f54ec-e175-436e-a709-27854983f36e)

![Screenshot 2023-08-09 at 1 20 35 PM](https://github.com/kssmp/Real_Time_Recognition_Attendance/assets/115448106/194f865c-be0b-4c5e-b9b1-c0c2fe504a80)



## Features

- Real-time Database and Storage using Firebase for attendance updation
- Last attendance time tracking.
- Number of attendance counts per individual.
- Change in interface when a new user enters

## Face-recognition Library
- Uses HOG representation for extracting the information of the edges magnitude as well as the orientation of the edges for successful identification of the face
- Alter the face into 68 specific landmarks and encode it for the deep neural network with 128 input measurements or embeddings
- The input is then compared using the SVM classifier to know whether we have a matching person in put database

## Usage

1. Attendance Recording:
   - Use the application to capture attendance data (e.g., user ID, timestamp).
   - The application will automatically update the real-time database with attendance records.

2. Last Attendance Time:
   - Each time attendance is recorded, the system will update the last attendance time for the corresponding user.

3. Attendance Count:
   - The system will maintain a count of the number of attendances for each individual based on the recorded data.

