//Macro to select a circle based on yh2ax foci size at channel 1
//input: image with 4 channels, 1st channel gamma
//outuput: cropped images around yh2ax foci
//Method: inspect how many slices will be used, mark first and how many, line 54 change the area of the roi in um2
//Made by Andre Thomaz (athomaz@ifi.unicamp.br) @ 2022-06-21

//get image parameters
getPixelSize(unit, pixelWidth, pixelHeight);

//folder to save the images
dir = getDirectory( "Choose the Directory" );

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

//duplicate stacks and Clear Outside Nucleus
roiManager("Select", 0);
run("Duplicate...", "duplicate");
rename("SUM");
run("Clear Outside", "slice");

//select yh2ax channel and find maxima
Stack.setChannel(1);
run("Enhance Contrast", "saturated=0.35");
//prominence = getNumber("Prominence?", 10000);
run("Find Maxima...")



//start
numResults = nResults;
print(numResults);
for (i=0; i<numResults; i++) {
	// 0.17 um2 area os yh2ax	
	d = 4*sqrt(0.017/PI); //set the region to a circle with double the area
	d = d/pixelWidth;
	xValue = getResult("X",i);
	yValue = getResult("Y",i);
	// gotta discount the raidius to make it centered
	x = xValue - d/2;
	y = yValue - d/2;
	//selectWindow("SUM_copy-stacks.czi");
	makeOval(x, y, d, d);
	roiManager("Add");
	run("Duplicate...", "duplicate");
	run("Make Inverse");
	setBackgroundColor(0, 0, 0);
	run("Clear", "slice");
	Stack.setChannel(2);
	run("Clear", "slice");
	Stack.setChannel(3);
	run("Clear", "slice");
	imgNumber = i+1;
	name = dir + imgNumber;
	print(i);
	saveAs("TIff", name);
	close();
	
	}
roiManager("Show All");
