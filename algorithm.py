# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 14:46:44 2018

@author: venkatavaradhan lakshminarayanan

Description: This is an algorithm built to perform adaptive thresholding of an
image. This algorithm basically works as follows,

1. Take the input image and resize for faster outputs.

2. Integrate the image such that each pixel represents the sum computed both   
   above and behind the current pixel.
   
3. For the second iteration on the image, (Sample_window_1)x(Sample_window_2) 
   average is calculated for each pixel by utilizing the computed integral
   image.
   
4. Based on the threshold value if the intensity is lesser the pixel value is 
   set to 0 and 255 if higher.
   
"""

import numpy as np
import cv2

number = 1
class adaptive_threshold:
    def __init__(self,image):
        self.input_image = cv2.resize(image,(256,196))
        self.height,self.width,_ = self.input_image.shape    
        self.sample_window_1 = self.width/12
        self.sample_window_2 = self.sample_window_1/2
        self.threshold = 68
        self.integrated_image = np.zeros_like(self.input_image, dtype=np.uint32)
        self.output_image = np.zeros_like(self.input_image)
        self.main()
    
    def integrate_image(self):
        for column in range(self.width):
            for row in range(self.height):
                self.integrated_image[row,column] = self.input_image[0:row,0:column].sum()
    
    def the_algorithm(self):
        for column in range(self.width):
            for row in range(self.height):
                y1 = round(max(row-self.sample_window_2,0))
                y2 = round(min(row+self.sample_window_2, self.height-1))
                x1 = round(max(column-self.sample_window_2,0))
                x2 = round(min(column+self.sample_window_2,self.width-1))
                
                count = (y2-y1)*(x2-x1)
                
                total = self.integrated_image[y2,x2]-self.integrated_image[y1,x2]-self.integrated_image[y2,x1]+self.integrated_image[y1,x1]          
                
                if np.all(self.input_image[row,column]*count < total*(100-self.threshold)/100):
                    self.output_image[row,column] = 0
                else:
                    self.output_image[row,column] = 255
            
    def main(self):
        self.integrate_image()
        self.the_algorithm()
        self.display_save()        
        
    def display_save(self):
        global number
        cv2.imshow('Image',self.input_image)
        cv2.imshow('Output',self.output_image)
        filename = 'output-'+str(number)+'.jpg'
        cv2.imwrite(filename,self.output_image)
        number+=1
        key = cv2.waitKey(0)

image1 = cv2.imread('testImage0.pgm')
image2 = cv2.imread('testImage1.pgm')
filter_ = adaptive_threshold(image1)
filter_ = adaptive_threshold(image2)



    

