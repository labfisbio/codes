//Macro to select a circle based on BCLAF1 cluster size
//input: image with 4 channels
//outuput: cropped images around BCLFA1 cluster
//Method: First select BCLAF1 clusters by Analyze Particle and get each ROI then run macro. Before running the maacro 
// make sure centroid is selected in Set Measuremnt 
//Made by Andre Thomaz (athomaz@ifi.unicamp.br) @ 2021-10-11

//get image parameters
getPixelSize(unit, pixelWidth, pixelHeight);

//folder to save the images
dir = getDirectory( "Choose the Directory" );


//start
numROIS = roiManager("count");
for (i=0; i<numROIS;i++)
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
	imgNumber = i+1;
	name = dir + imgNumber;
	//print(name);
	saveAs("TIff", name);
	close();
	
	}
