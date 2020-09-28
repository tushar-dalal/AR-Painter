# OpenCV-Painter
This repository has code for Augmented 2D painting with webcam. Pull requests welcome.

To run this code, first run Colour picker.

1. Raise a pen of a distinguished colour in front of the webcam.
2. Adjust the vaues of h_min and oher such variables in the bars till only your pen is visible.
3. Note the values of all the trackerbars
4. Quit the program (press <k>)

5. Edit the Painter variabe "myColours" and add your recorded colour to the list as [[h_min, s_min, v_min], [h_max, s_max, v_max]]
6. Add a colour to the "mycolourvals" variable as [B, G, R]
7. Run the main code.
8. Raise a pen and watch it paint the screen.
9. Quit this section using <q>

In  case working with Colour picker doesnt suit you (recording and then pasting in the source code of Painter.py), youcan use the quoted peice of code in Painter.
To use it, simply un-quote the program part and after the second step, press <s>. This will save a new pen configuration to your program, but will not add a new colour, that part needs to be added to the program as of yet. (Let me know if anyone wants to contribute) 
