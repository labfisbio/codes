//Macro to count yh2ax foci on nucleus
//input: image with 4 channels, being C1 yh2ax channel and C4 nucleus channel
//outuput: number of yh2ax foci on results windows
//Method: Inside nucleus ROI find maxima using Find Maxima tools with prominence=2000 (difference between maxima and minumum around)
//Made by Andre Thomaz (athomaz@ifi.unicamp.br) @ 2021-10-11


run("Clear Results");

//Project and select nucleus ROI
title = getTitle();
first_slice = getNumber("First Slice?", 1);
last_slice = getNumber("Last Slice?", 20);
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
run("Set Measurements...", "area integrated redirect=None decimal=3");
Stack.setChannel(2);
run("Measure");
Stack.setChannel(3);
run("Measure");


