//Macro to select a circle based on cluster size at channel 3
//input: image with 4 channels, 4th channel nucleus
//outuput: cropped images around cluster
//Method: inspect how many slices will be used, mark first and how many.
//Made by Andre Thomaz (athomaz@ifi.unicamp.br) @ 2021-10-11

//clear 
run("Clear Results");
roiManager("reset");

//get image parameters
getPixelSize(unit, pixelWidth, pixelHeight);

//folder to save the images
dir = getDirectory( "Choose the Directory" );

title = getTitle();

//slices to Z Project SUM
first_slice = getNumber("First Slice?", 7);
slices = getNumber("How many slices?", 20);
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

//duplicate stacks and Analyze Particles min area = 0.1 um at line 49
roiManager("Select", 0);
run("Duplicate...", "duplicate");
setBackgroundColor(0, 0, 0);
run("Clear Outside", "stack");
rename("SUM");
Stack.setChannel(3);
run("Duplicate...", "duplicate channels=3")
setAutoThreshold("Default dark");
run("Threshold...");
waitForUser('Adjust Threshold to select clusters');
run("Convert to Mask");
selectWindow("SUM-1");
run("Analyze Particles...", "size=0.20-Infinity add");
selectWindow("SUM");

//start
numROIS = roiManager("count");
for (i=1; i<numROIS;i++) //start at 1 to keep nucleus ROI
{	roiManager("Select", i);
	run("Set Measurements...", "area centroid redirect=None decimal=3"); 
	results = roiManager("Measure"); //measure the area
	area = getResult("Area");
	d = 4*sqrt(area/PI); //set the region to a circle with double the area
	d = d/pixelWidth;
	xValue = getResult("X");
	yValue = getResult("Y");
	// gotta discount the raidius to make it centered
	x = xValue/pixelWidth - d/2;
	y = yValue/pixelWidth - d/2;
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
	imgNumber = i+0;
	name = dir + imgNumber;
	//print(name);
	saveAs("TIff", name);
	close();
	
	}

