title = getTitle();
print("dir: "+File.directory);


Stack.setChannel(1);
run("Plot Profile");
Plot.getValues(x, y);
for (i=0; i<x.length; i++)
{  setResult("X", i, x[i]);
  setResult("Y", i, y[i]);}
updateResults();
saveAs("Results", File.directory+"yh2ax.csv");

selectWindow(title);
Stack.setChannel(2);
run("Plot Profile");
Plot.getValues(x, y);
for (i=0; i<x.length; i++)
{  setResult("X", i, x[i]);
  setResult("Y", i, y[i]);}
updateResults();
saveAs("Results", File.directory+"parp1.csv");

selectWindow(title);
Stack.setChannel(3);
run("Plot Profile");
Plot.getValues(x, y);
for (i=0; i<x.length; i++)
{  setResult("X", i, x[i]);
  setResult("Y", i, y[i]);}
updateResults();
saveAs("Results", File.directory+"ptk2.csv");


