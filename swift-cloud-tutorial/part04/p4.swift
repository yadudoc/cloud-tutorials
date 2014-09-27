type file;

app (file out) sortdata (file unsorted)
{
  sort "-n" "unsorted.txt" stdout=filename(out);
}

file unsorted <"unsorted.txt">;
file sorted <"sorted.txt">;

sorted = sortdata(unsorted);
