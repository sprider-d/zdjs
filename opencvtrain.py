
import cv2
import numpy as np


def region_of_interest(img,vertices):
    mask = np.zeros_like(img)

    if len(img.shape>2):
        channel_count = img.shape[2]
        img_mask_color = (255,) *channel_count
    else:
        img_mask_color = 255

    cv2.fillPoly(mask,[vertices],img_mask_color)
    masked_image = cv2.bitwise_and(img,mask)

    return masked_image


def draw_lines(img,lines,color=[255,0,0],thickness=2):
    left_lines_x = []
    left_lines_y = []
    right_lines_x = []
    right_lines_y = []
    line_y_max = 0
    line_y_min = 999
    for line in lines:
        for x1,y1,x2,y2,in line:
            if y1>line_y_max:
                line_y_max = y1
            if y2>line_y_max:
                line_y_max = y2

            if y1<line_y_min:
                line_y_min = y1

            if y2<line_y_min:
                line_y_min = y2

            k = (y2-y1)/(x2-x1)

            if k<-0.3:
                left_lines_x.append(x1)
                left_lines_y.append(y1)
                left_lines_x.append(x2)
                left_lines_y.append(y2)


            elif k >0.3:
                right_lines_x.append(x1)
                right_lines_y.append(y1)
                right_lines_x.append(x2)
                right_lines_y.append(y2)

    left_line_k,left_line_b = np.polyfit(left_lines_x,left_lines_y,1)
    right_line_k,right_line_b = np.polyfit(left_lines_x,left_lines_y,1)


    cv2.line(img,
             (int((line_y_max-left_line_b)/left_line_k),line_y_max),
             (int((line_y_min - left_line_b) / left_line_k), line_y_min),
                color,thickness
             )

    cv2.line(img,
             (int((line_y_max-right_line_b)/right_line_k),line_y_max),
             (int((line_y_min - right_line_b) / right_line_k), line_y_min),
                color,thickness
             )

def main():
    img = cv2.imread(img_path)
    cv2.imshow("img", img)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray",gray)

    canny = cv2.Canny(gray,40,150)
    cv2.imshow("bianyuan",canny)

    # img_thre = cv2.threshold(gray,100,200,0)
    # cv2.imshow("img_thre",img_thre)

    # contours = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(img,contours,-1,(0,0,255),2)
    # cv2.imshow("new_img",img)
    #

    left_bottom = [0, canny.shape[0]]
    right_bottom = [canny.shape[1], canny.shape[0]]
    apex = [canny.shape[1] / 2, 310]
    vertices = np.array([left_bottom, right_bottom, apex], np.int32)
    roi_image = region_of_interest(canny, vertices)

    cv2.imshow("roi_image",roi_image)




    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    img_path = "img/chedao.jpg"

    main()




