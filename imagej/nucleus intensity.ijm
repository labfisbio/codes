//Macro to measure nuclear intensity at 2 channels change each channel at lines 39 and 41
//input: image with 4 channel C4 nucleus channel
//outuput: csv file with intesities, image_number_number_cells.csv
//Method: Inside nucleus ROI measure intensity
//Made by Andre Thomaz (athomaz@ifi.unicamp.br) @ 2022-02-14

run("Clear Results");
roiManager("reset");

//Project and select nucleus ROI
title = getTitle();
//img_number_index = lastIndexOf(title, '647'); //Change this to the last wavelength channel
//img_number = substring(title, img_number_index+4, img_number_index+6);

file_path = getDirectory( "Choose the Directory" );
//print(file_path);
img_number = getNumber("Image Number?", 1);
first_slice = getNumber("First slice?", 1);
slices = getNumber("How many slices?", 4);
last_slice = first_slice + slices;
//run("Z Project...", "projection=[Sum Slices]");
run("Z Project...", "start=" + first_slice + " stop=" + last_slice + " projection=[Sum Slices]");
Stack.setDisplayMode("color");
Stack.setChannel(4);

img_numbersss = 1;
n_nucleus = getNumber("How many nucleus?", 1);
img_number = img_number+"_"+n_nucleus;
print(n_nucleus);
print(img_number);



setTool("wand");
setAutoThreshold("Default dark");
run("Threshold...");

for (n = 0; n < n_nucleus; n++) {
 waitForUser('Adjust Threshold to select the nucleus and select it with wand');
 roiManager("Add");
}

//
n_rois = roiManager("count");
run("Set Measurements...", "area integrated redirect=None decimal=3");
for (i=0; i<n_rois; i++) {
	roiManager("Select", i);
	Stack.setChannel(1); //first channel to measure
	run("Measure"); 
	Stack.setChannel(3); //second channel to measure
	run("Measure");
};
file_name = file_path + "/" + img_number + ".csv";
//print(file_name)
saveAs("Results", file_name);




