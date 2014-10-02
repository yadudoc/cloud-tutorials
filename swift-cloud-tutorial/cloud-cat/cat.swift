type file;

// The app "cat" takes an input file and cats the output to the specified output
// file
app (file out) cat (file input)
{
    cat @input stdout=@out;
}

// A filesystem mapper is used to map all files in a directory "inputs" with the
// suffix "txt" to an array of type files
file inputs[]    <filesys_mapper; location="inputs", suffix="txt">;


// Iterate over all files in parallel
foreach input,i in inputs
{
  file out <single_file_mapper; file=strcat("output/foo_",i,".out")>;
  out = cat (input);
}

