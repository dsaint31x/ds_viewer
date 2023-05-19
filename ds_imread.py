import cv2, numpy as np
import os
import sys
import pydicom 


def ds_imread_common(fstr):
   img_array = np.fromfile(fstr, np.uint8)
   img = cv2.imdecode(img_array, cv2.IMREAD_UNCHANGED)
   return img
 



def ds_imread(fstr):
   """_summary_ image파일을 로딩하는 구현부.

   Args:
       fstr (str): image파일의 경로 문자열.

   Returns:
       _type_: cv2에서 처리가능한 numpy ndarray. 
   """
   img = None
   _, fext = os.path.splitext(fstr)
   print(f'on "to_cv2" : fstr={fstr}, fext={fext}')
   
   if fext == None or fext.strip() == "":
      print(f'there is unavailiable file extension : {fstr}')
      sys.exit(0)
   elif fext.strip().lower() ==".dcm":
      d = pydicom.dcmread(fstr)
      tmp_array = d.pixel_array
      # ceph = cv2.normalize(tmp_array, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
      # src, dst, alpha, beta, flag. 
      img = cv2.normalize(tmp_array, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
      
      img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
   else:
      img= ds_imread_common(fstr)
   
   print("read shape:",img.shape, 
         "/ read dtype:", img.dtype, 
         "/max~min:",np.max(img),np.min(img))
      
   return img
   