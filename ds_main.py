import cv2
import sys, os
import ds_imread

alpha_slider_max = 300
beta_slider_max = 100

alpha = 1.0 # simple contrast control, range [1.0,3.0] > display (%)
beta = 0.   # simple brightness control, range [0., 100]
invert = 0  # 0 : file, 1 : invert
marker_radius = 4

def on_invert_trackbar(val):
    global invert 
    invert = val
    print(f'invert={invert}')
    
def on_contrast_trackbar(val):
    global alpha
    # alpha = val / 100
    alpha = val
    # print(f'alpha={alpha}, beta={beta}')
def on_brightness_trackbar(val):
    global beta 
    beta = val 
    # print(f'alpha={alpha}, beta={beta}')
    
def on_marker_radius_trackbar(val):
    global marker_radius
    marker_radius = val 
    # print(f'alpha={alpha}, beta={beta}')
    
def apply_invert(input_img, invert):
    if invert == 1:
        ret = cv2.bitwise_not(input_img)
        return ret
    else:
        return input_img

def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)
    
def apply_brightness_contrast(input_img, brightness = 255, contrast = 127):
    brightness = map(brightness, 0, 510, -255, 255) # -255~255범위로 변환 ratio
    contrast   = map(contrast,   0, 254, -127, 127) # -127~127범위로 변환 ratio
    
    if brightness != 0:
        if brightness > 0:
            shadow = brightness # min_value
            highlight = 255     # max_value
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow
        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b) # gamma_b =bias.
    else:
        buf = input_img.copy()
        
    if contrast != 0:
        f = float(131 * (contrast + 127)) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)
    cv2.putText(buf,'B:{},C:{}'.format(brightness,contrast),(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    return buf    
    
def ds_paint(img_ori):
    fstr=''
    
    ceph_view = apply_invert(img_ori,invert)
    ceph_view = apply_brightness_contrast(ceph_view, 
                                          brightness = beta, 
                                          contrast = alpha)
    # ceph_view = apply_brightness_contrast(ceph_ori, brightness = beta, contrast = alpha)
    
    cv2.imshow("Landmark Points", ceph_view)
    cv2.displayOverlay('Landmark Points', fstr)

    
def ds_init(img_path):
    """_summary_ 초기화 루틴 :

    Args:
        img_path (str): 라벨링이 될 image파일들이 위치한 directory path

    Returns:
        img_path (str)
    """
    
    # global conf_PATH
        
    # cv2.namedWindow('Landmark Points',flags=(cv2.WINDOW_GUI_NORMAL | cv2.WINDOW_KEEPRATIO))
    cv2.namedWindow('Landmark Points',flags=(#cv2.WINDOW_KEEPRATIO|
                                          #   cv2.WINDOW_OPENGL|
                                            cv2.WINDOW_GUI_EXPANDED))
    
    trackbar_name = 'invert'
    cv2.createTrackbar(trackbar_name, "Landmark Points", invert, 1, on_invert_trackbar)
    
    trackbar_name = 'contrast'
    cv2.createTrackbar(trackbar_name, "Landmark Points", 127, 2*127, on_contrast_trackbar)
    
    trackbar_name = 'brightness'
    cv2.createTrackbar(trackbar_name, "Landmark Points", 255, 2*255, on_brightness_trackbar)
    
    trackbar_name = 'marker_radius'
    cv2.createTrackbar(trackbar_name, "Landmark Points", 4, 8, on_marker_radius_trackbar)
    cv2.setTrackbarMin(trackbar_name, 'Landmark Points', 1)
    
    pwd = os.getcwd()
    
    # -------------------------------------
    # sample_PATH 설정.
    # sample_PATH=pwd_PATH+'/sample'
    if img_path == None:
        print(f'Error : specify the path of image!')
        exit()
    
    return img_path

def ds_main(_img_path):
    
    whbreak = False
    img_path = ds_init(_img_path)
    
    img = ds_imread.ds_imread(img_path)
    
    while(True):
        ds_paint(img)
        ds_key = cv2.waitKeyEx(400) & 0xFF
        
        vis = cv2.getWindowProperty("Landmark Points", cv2.WND_PROP_VISIBLE)
        
        if ds_key == 27: # ESC.
            print('Terminated by ESC:',ds_key)
            whbreak = True
            break
        elif vis < 1:
            print('Terminated by WND_PROP_VISIBLE<1:',vis)
            whbreak = True
            break
        
    if whbreak == True:
        cv2.destroyAllWindows()
    
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Error: required the path of image to view.')
    else:
        ds_main(sys.argv[1])



    