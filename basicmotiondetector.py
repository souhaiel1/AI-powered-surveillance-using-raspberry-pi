# importing the necessary packages
import cv2
import imutils


class BasicMotionDetector:
    def __init__(self, accumWeight=0.5, deltaThresh=5, minArea=5000):
        # determine the OpenCV version, followed by storing the
        # the frame accumulation weight, the fixed threshold for
        # the delta image, and finally the minimum area required
        # for "motion" to be reported
        self.isv2 = imutils.is_cv2()
        self.accumWeight = accumWeight
        self.deltaThresh = deltaThresh
        self.minArea = minArea

        # initialize the average image for motion detection
        self.avg = None
        self.scanned_frames_counter = 0

    def update(self, image):
        self.scanned_frames_counter += 1
        # initializing the list of locations containing motion
        locs = []

        # if the average image is None, initialize it
        if self.avg is None:
            self.avg = image.astype("float")
            return locs

        # accumulating the weighted average between
        # the current frame and the previous frames, then compute
        # the pixel-wise differences between the current frame
        # and running average
        cv2.accumulateWeighted(image, self.avg, self.accumWeight)
        frameDelta = cv2.absdiff(image, cv2.convertScaleAbs(self.avg))

        # threshold the delta image and apply a series of dilations
        # to help fill in holes
        thresh = cv2.threshold(frameDelta, self.deltaThresh, 255,
                               cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        # find contours in the thresholded image
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        for c in cnts:
            # the contour will be added to the locations list only if it
            # exceeds the predifined minimum area
            if cv2.contourArea(c) > self.minArea:
                locs.append(c)

        # return the set of locations
        return locs
