type imagefile;
type landuse;

app (landuse output) getLandUse (imagefile input)
{
  getlanduse @filename(input) stdout=@filename(output);
}

imagefile modisImage <"data/europe/h18v05.rgb">;
landuse result <"landuse/h18v05.landuse.byfreq">;
result = getLandUse(modisImage);
