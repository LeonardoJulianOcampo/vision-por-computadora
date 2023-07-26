import cv2 as cv
import numpy as np
import json

with open("camera.json","r") as json_file:
    camera_data = json.load(json_file)


t_vect = np.array(camera_data["tvecs"])
r_vect = np.array(camera_data["rvecs"])
cam_mtx = np.array(camera_data["mtx"])
d_coef  = np.array(camera_data["dist"])


marker_size_in_cm = 3.8


dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_ARUCO_ORIGINAL)
param = cv.aruco.DetectorParameters()
detector = cv.aruco.ArucoDetector(dict,param)

capture = cv.VideoCapture(0)



while True:
    ret,frame = capture.read()
    if not ret:
        break

    g_frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    corners, ids, reject = detector.detectMarkers(frame)

    if corners:
        rVec,tVec,_ = cv.aruco.estimatePoseSingleMarkers(corners,marker_size_in_cm,cam_mtx,d_coef)
        marker_index = range(0,(ids.size))
        for m_ids,m_corners,i in zip(ids,corners,marker_index):
            cv.polylines(frame,[m_corners.astype(np.int32)],True,(0,255,255),4,cv.LINE_AA)
            m_corners = m_corners.reshape(4,2)
            m_corners = m_corners.astype(int)
            
            dist = np.sqrt(tVec[i][0][0]**2 + tVec[i][0][1]**2 + tVec[i][0][2]**2)
            r = np.sqrt(tVec[i][0][0]**2 + tVec[i][0][1]**2)
            z = np.sqrt(tVec[i][0][2]**2 - tVec[i][0][0]**2 - tVec[i][0][1]**2)
            origin = cv.drawFrameAxes(frame,cam_mtx,d_coef,rVec[i],tVec[i],4,4)
            
#            cv.putText(frame,f"id:{m_ids[0]} Distancia: {round(dist,2)}",(5,25 + marker_index[i] * 25),cv.FONT_HERSHEY_PLAIN,1.3,(0,0,255),2,cv.LINE_AA,)
            cv.putText(frame,f"id:{m_ids[0]} x:{round(tVec[i][0][0],2)} y: {round(tVec[i][0][1],2)} z: {round(z,2)} d: {round(tVec[i][0][2],2)}",(5,25+marker_index[i]*55),cv.FONT_HERSHEY_PLAIN,1.3,(0,0,255),2,cv.LINE_AA,)
        
    cv.imshow("frame",frame)

    key=cv.waitKey(1)
    if key == ord("q"):
        break

capture.release()
cv.destroyAllWindows()
