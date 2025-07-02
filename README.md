# Scraps
Scraps is a tool that enables you to reuse scraps of material in your laser cutter, plasma cutter or waterjet machine, by digitizing the shape and position of your bits of scrap.
The tool allows you to save a dxf file that you can import into the machines software and lay out your new parts to be cut onto the existing bits of scrap already in your machine.

## Usage
Browse to load an image taken of the machine bed with the scrap inside.
You need to mark a set of four rectangular points that establish a rectangle of known dimensions.
These dimensions need to be filled into the Measurements fields.

![Screenshot 2025-07-02 094611](https://github.com/user-attachments/assets/27f69b04-3fee-4404-93df-52be3d282fb1)

Once the image is loaded, you need to choose the calibration points top-left in a clockwise direction, then click on top down.
This will apply a transformation matrix that removes the perspective of the image, showing a normal view to the plane of the machine.
Note the zoom window to the bottom left that helps you pick the points accurately.

![2](https://github.com/user-attachments/assets/58726215-5d87-49d9-a0a0-d6173227c15c)

Once the points are chosen, after clicking on Top Down, you get a normal view.
If the camera you use to take the pictures is fixed, you can save the calibration to a file, and next time you can just load the calibration instead of picking the points for each image.

![3](https://github.com/user-attachments/assets/114ff965-3938-4611-97ec-c1981927e2d8)

A feature I really wanted to have was a measuring tool, which you can use with the appropriately named Measure button.

![4](https://github.com/user-attachments/assets/2e91a912-1b54-4a33-81b2-52e212aa5675)

Next, you can use the contour button to try and edge detect the image. Note that the supplied test image doesn't have the proper contrast that you would have in a real situation:

![5](https://github.com/user-attachments/assets/ae8f5be4-ff5c-4c5f-a16e-9fbd02fb166a)

You can use the Blur Kernel, Max and Min threshold settings to adjust the detection performance.
Then, clicking on Show Contour will show only the detected edges:

![6](https://github.com/user-attachments/assets/ebf8d755-eeb8-4db7-bd91-d46a6bddd5de)

Finally, you can save the dxf file to your drive and load it into the software that your machine uses.
Hope this helps!

