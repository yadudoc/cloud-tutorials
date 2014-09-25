type file;

app (file f) greeting() { 
    echo "Hello, world!" stdout=@filename(f);
}

file outfile <"hello.txt">;
outfile = greeting();
