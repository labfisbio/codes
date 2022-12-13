title = getTitle();

Stack.setChannel(2);
run("Plot Profile");
Plot.getValues(x, y);
for (i=0; i<x.length; i++)
{  setResult("X", i, x[i]);
  setResult("Y", i, y[i]);}
updateResults();
//saveAs("Results", "teste.csv");
print("dir: "+File.directory);
//Plot.create("Profile", "X", "Value", profile);
//selectWindow(title);
//Stack.setChannel(3);
//run("Plot Profile");
//
//selectWindow(title);
//Stack.setChannel(4);
//run("Plot Profile");


