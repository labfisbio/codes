//Macro to measure nuclear intensity at channels 2 and 3
//input: image with 4 channels, being C2 and C3 to be measured and C4 nucleus channel
//outuput: csv file with intensities C2,C3 per nucleus
//Method: Inside nucleus ROI measure intensity
//Made by Andre Thomaz (athomaz@ifi.unicamp.br) @ 2022-02-14

run("Clear Results");
roiManager("reset");

//Project and select nucleus ROI
//title = getTitle();
file_path = "C:/Users/Andre/Desktop/Images/fak mio yh2ax/myo5b/doxo";
//print(file_path);
img_number = getNumber("Image Number?", 1);
first_slice = getNumber("First Slice?", 1);
slices = getNumber("How many slices?", 14);
last_slice = first_slice + slices;
run("Z Project...", "start=" + first_slice + " stop=" + last_slice + " projection=[Sum Slices]");
Stack.setDisplayMode("color");
Stack.setChannel(4);
setTool("wand");
setAutoThreshold("Default dark");
run("Threshold...");
n_nucleus = getNumber("How many nucleus?", 1);
for (n = 0; n < n_nucleus; n++) {
 waitForUser('Adjust Threshold to select the nucleus and select it with wand');
 roiManager("Add");
}

//
n_rois = roiManager("count");
run("Set Measurements...", "area integrated redirect=None decimal=3");
for (i=0; i<n_rois; i++) {
	roiManager("Select", i);
	Stack.setChannel(2);
	run("Measure");
	Stack.setChannel(3);
	run("Measure");
};
file_name = file_path + "/" + img_number + ".csv";
//print(file_name)
saveAs("Results", file_name);




