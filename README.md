# ProcessDLS
We use a pair of www.correlator.com correlators to capture speckle data from samples.

This code uses JScatter and CONTIN to (batch) process the www.correlator.com .SIN files.

Some demo .SIN files are included.

I could not get Jscatter to work on Mac or Windows, but the code runs nicely on Ubuntu 20.

#Installing on ubuntu

```
mkdir Github
cd Github/

git clone https://github.com/Resonanz/Jscatter-ProcessDLS.git

cd Jscatter-ProcessDLS/

wget http://s-provencher.com/pub/contin/contin.for.gz

gunzip contin.for.gz

sudo apt install gfortran
gfortran contin.for -o contin

sudo mv contin /usr/local/bin/contin
chmod u+x /usr/local/bin/contin
```
