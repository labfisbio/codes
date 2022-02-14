//Macro to count yh2ax foci on nucleus
//input: image with 4 channels, being C1 yh2ax channel and C4 nucleus channel
//outuput: number of yh2ax foci on results windows
//Method: Inside nucleus ROI find maxima using Find Maxima tools with prominence=2000 (difference between maxima and minumum around)
//Made by Andre Thomaz (athomaz@ifi.unicamp.br) @ 2021-10-11


run("Clear Results");

//Project, split and rename
title = getTitle();
run("Z Project...", "projection=[Max Intensity]");
run("Split Channels");
selectWindow("C4-MAX_" + title);
rename("Nucleus DAPI");
selectWindow("C1-MAX_" + title);
rename("GammaH2AX");

//go in a loop to get all Nucleus ROIs
selectWindow("Nucleus DAPI");
run("Enhance Contrast", "saturated=0.35");
setTool("wand");
setAutoThreshold("Default dark");
run("Threshold...");
n_nucleus = getNumber("How many nucleus?", 1);
for (n = 0; n < n_nucleus; n++) {
 waitForUser('Adjust Threshold to select the nucleus and select it with wand');
 roiManager("Add");
}


// change to y2hax window and count number of foci
selectWindow("GammaH2AX");
run("Enhance Contrast", "saturated=0.35");
nroi = roiManager("count");
for (i = 0; i < nroi; i++) {
	roiManager("Select", i);
	run("Find Maxima...", "prominence=2000 output=Count");
}