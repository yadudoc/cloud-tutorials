type file;
type imagefile;
type landuse;

app (landuse output) getLandUse (imagefile input)
{
  getlanduse @filename(input) stdout=@filename(output);
}

app (file output, file tilelist) analyzeLandUse (landuse input[], string usetype, int maxnum)
{
  analyzelanduse @output @tilelist usetype maxnum @input;
}

# Constants and command line arguments
int nFiles       = @toInt(@arg("nfiles", "1000"));
int nSelect      = @toInt(@arg("nselect", "10"));
string landType  = @arg("landtype", "urban");
string MODISdir  = @arg("modisdir", "data/europe");

# Input Dataset
imagefile geos[] <ext; exec="../bin/modis.mapper", location=MODISdir, suffix=".rgb", n=nFiles>;

# Compute the land use summary of each MODIS tile
landuse land[] <structured_regexp_mapper; source=geos, match="(h..v..)", transform=@strcat("landuse/\\1.landuse.byfreq")>;

foreach g,i in geos {
    land[i] = getLandUse(g);
}

# Find the top N tiles (by total area of selected landuse types)
file topSelected <"topselected.txt">;
file selectedTiles <"selectedtiles.txt">;
(topSelected, selectedTiles) = analyzeLandUse(land, landType, nSelect);
