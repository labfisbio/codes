//Macro to calculate yh2ax mean area at channel 1
//input: image with 4 channels, 1st channel gamma
//outuput: mean yh2ax area at Log window
//Made by Andre Thomaz (athomaz@ifi.unicamp.br) @ 2022-06-22



//clear 
run("Clear Results");
roiManager("reset");

//slices to Z Project SUM
title = getTitle();
first_slice = getNumber("First Slice?", 1);
slices = getNumber("How many slices?", 14);
last_slice = first_slice + slices;
run("Z Project...", "start=" + first_slice + " stop=" + last_slice + " projection=[Sum Slices]");

//select nucleus ROI
z_title = 'SUM_'+title;
selectWindow(z_title);
Stack.setDisplayMode("color");
Stack.setChannel(4);
setTool("wand");
setAutoThreshold("Default dark");
run("Threshold...");
waitForUser('Adjust Threshold to select the nucleus and select it with wand');
roiManager("Add");

//duplicate stacks and Analyze Particles 
roiManager("Select", 0);
run("Duplicate...", "duplicate");
rename("SUM");
Stack.setChannel(1);
run("Clear Outside", "slice");
run("Duplicate...", "duplicate channels=1")
setAutoThreshold("Default dark");
run("Threshold...");
waitForUser('Adjust Threshold to select clusters');
run("Convert to Mask");
selectWindow("SUM-1");
run("Analyze Particles...", "add");
selectWindow("SUM");
run("Enhance Contrast", "saturated=0.35");
roiManager("Show All without labels");


// calculate mean area and plot
n_results = nResults;
area_array = newArray;

for (i = 1; i < nResults; i++) {
	f_area = getResult("Area", i);
	area_array = Array.concat(area_array, f_area);
}

Array.getStatistics(area_array, min, max, mean, stdDev);
print("yH2AX foci mean area = "+ mean + " um^2");


