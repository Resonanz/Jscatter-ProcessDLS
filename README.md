# ProcessDLS
We use a pair of www.correlator.com correlators to capture speckle data from samples.

This code uses JScatter and CONTIN to (batch) process the www.correlator.com .SIN files.

Some demo .SIN files are included.

I could not get Jscatter to work on Mac or Windows, but the code runs nicely on Ubuntu 20.

# Installing Jscatter on Ubuntu
In home directory:
```
mkdir Github
cd Github/
git clone https://github.com/Resonanz/Jscatter-ProcessDLS.git
```
Get CONTIN:
```
wget http://s-provencher.com/pub/contin/contin.for.gz
gunzip contin.for.gz
```
Install Fortran compiler, compiler, move executable into path and change permissions:
```
sudo apt install gfortran
gfortran contin.for -o contin

sudo mv contin /usr/local/bin/contin
chmod u+x /usr/local/bin/contin
```
Run the Python code from here:
```
cd Jscatter-ProcessDLS/
```
