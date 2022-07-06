//Macro to select a circle based on cluster size at channel 3 and the same number of random areas
//input: image with 4 channels, 4th channel nucleus
//outuput: cropped images around cluster
//Method: inspect how many slices will be used, mark first and how many.
//TODO: check if random areas are inside nucleus ROI and if they don't overlap with clusters
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
first_slice = getNumber("First Slice?", 14);
slices = getNumber("How many slices?", 9);
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


//duplicate stacks and Analyze Particles min area = 0.2 um at line 49
roiManager("Select", 0);
run("Duplicate...", "duplicate");
roiManager("add");
setBackgroundColor(0, 0, 0);
run("Clear Outside", "stack");
rename("SUM");
close(z_title);
selectWindow("SUM");
Stack.setChannel(2);
run("Duplicate...", "duplicate channels=2")
setAutoThreshold("Default dark");
run("Threshold...");
waitForUser('Adjust Threshold to select clusters');
run("Convert to Mask");
selectWindow("SUM-1");
run("Analyze Particles...", "size=0.15-Infinity add");
close();
selectWindow("SUM");

roiManager("Select", 0);
roiManager("Delete");
roiManager("Select", 0);
roiManager("rename", "Nucleus");


//start
num_Clusters = roiManager("count") - 1;
print('Number of detected clusters = ' + num_Clusters);
for (i=1; i <= num_Clusters;i++) //start at 1 to keep nucleus ROI
{	roiManager("Select", i);
	imgNumber = i+0;
	roiManager("rename", "cluster "+imgNumber);
	
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
	roiManager("Select", i + num_Clusters);
	roiManager("rename", "area "+imgNumber);
	run("Duplicate...", "duplicate");
	run("Clear Outside", "stack");
	
	name = dir + imgNumber;
	//print(name);
	saveAs("TIff", name);
	close();
	
	}

//save Results table with x,y and area 
area_array = newArray();

for (i=0; i < nResults(); i++) {
	area_i = getResult("Area", i);
	area_array = Array.concat(area_array,area_i);
}
Array.getStatistics(area_array, minimum, maximum, mean);
setResult("Mean", i, mean);
saveAs("Results", dir + "Results.csv");



//Random Areas
roiManager("select", 0);
Roi.getBounds(x_nucleus, y_nucleus, w_nucleus , h_nucleus); // heigth and width of nucleus ROI

random_folder = dir + File.separator + "random";

count = 0; //counter for number of randon areas
while (count < num_Clusters) {
	roiManager("select", 0);
	x1 = random()*(w_nucleus/pixelWidth) + x_nucleus/pixelWidth;
	y1 = random()*(h_nucleus/pixelWidth) + y_nucleus/pixelWidth;
if (Roi.contains(x1, y1) == true) {
	//n_circle_cluster = count + num_Clusters + 1; 
	n_cluster = count; 
	area = getResult("Area", n_cluster);
	d1 = 4*sqrt(area/PI); 
	d1 = d1/pixelWidth; //set the diameter from the cluster measured	
	makeOval(x1, y1, d1, d1);
	Roi.setStrokeColor("white");
	roiManager("Add");
	roiManager("select", count + 2*num_Clusters + 1);
	roiManager("rename", "random " + count+1);
	count++;
	print("Point add: " + count);
	run("Duplicate...", "duplicate");
	run("Clear Outside", "stack");
	imgNumber = count+0;
	name = random_folder + imgNumber;
	//print(name);
	saveAs("TIff", name);
	close();
			}
		
		}
print("Done");











