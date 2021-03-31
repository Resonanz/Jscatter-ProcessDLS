import jscatter as js
import numpy as np
import math
import matplotlib.pyplot as plt

LASER_WAVELENGTH = 632 #530

FILENAMES_TO_OPEN = [
    'Liposomes (30mW 1.5mL undiluted)'#,
   # 'Liposomes (40mW 1.5mL 1-1 diluted)',
   # 'Liposomes (60mW 2.25mL 1-2 diluted)',
   # 'Liposomes (60mW 3mL 1-3 diluted)',
   # 'Liposomes (60mW 3.75mL 1-4 diluted)',
   # 'Liposomes (100mW 1.65mL 1-9 diluted)',
   # 'Liposomes (200mW 3.3mL 1-19 diluted)',
   # 'Liposomes (200mW 4.1mL 1-24 diluted)' 
]

FILENAME_PATH = 'data/'
FILENAME_SIN_EXTENSION = '.SIN'
FILENAME_CSV_EXTENSION = '.csv'
CLEANED = ' (cleaned)'
G1_VS_GAMMA = ' (g1 vs gamma)'
G1_VS_TAU = ' (g1 vs tau)'
PRH_RH = ' (Prob Rh vs Rh)'

# If NAN appears in the Rh .csv, enlarge the value of NOISEY_LINES.
# A value of 100 has been observed to produce NAN values.
NOISEY_LINES = 150  # Noisey lines of data at start of text file

search_text_start = '[CorrelationFunction]\n'
search_text_end = '\n[RawCorrelationFunction]'


def read_correlator_text_file(filename):
    with open(filename, 'r') as file:
        return file.read()


def trim_correlator_text_file(text):
    idx_start = (text.find(search_text_start)) + len(search_text_start)
    idx_end = (text.find(search_text_end))
    return text[idx_start:idx_end]


def average_two_data_columns(text):
    averaged_data = ''
    noisey_data_delete_line_counter = 0

    line = text.split('\n')  # Split into lines using \n
    for l in line:

        if (noisey_data_delete_line_counter < NOISEY_LINES):
            noisey_data_delete_line_counter += 1
            continue

        try:
            values = l.split('\t')  # Split each line into 3 using \t
            abscissa_value = (float(values[0]))
            ordinate_value = ( float(values[1]) + float(values[2]) ) / 2

            # Correlator s/w seems to produce a lot of zero ordinate values at the end of the file, so ignore
            if (ordinate_value == 0.0):
                continue

            # Subtract 1 to go from G2 to G2-1
            if (ordinate_value != 0):
                ordinate_value = ordinate_value - 1

            averaged_data += str(abscissa_value)
            averaged_data += '\t'
            averaged_data += str(ordinate_value)
            averaged_data += '\n'
        except:
            print("Failed to split line -- probably a blank line")

    return averaged_data


def write_cleaned_correlator_text_file(filename, text):
    with open(filename, 'w') as file:
        file.write(text)

'''
This next block of code is mostly lifted from the Jscatter demo code DLS example.
'''
def do_contin_fitting(text):
    t = js.loglist(1, 10000, 1000)  # times in microseconds
    q = 4 * np.pi / 1.333 / LASER_WAVELENGTH * np.sin(np.pi / 2)  # 90 degrees for 632 nm , unit is 1/nm**2
    D = 0.05 * 1000  # nm**2/ns * 1000 = units nm**2/microseconds
    gamma = q*q*D
    #print(np.sin(np.pi/2))
    noise = 0.0001  # typical < 1e-3
    data = js.dA(np.c_[t, 0.95 * np.exp(-q ** 2 * D * t) + noise * np.random.randn(len(t))].T)
    #data = js.dA(FILENAME_PATH + filename_to_open + CLEANED + FILENAME_SIN_EXTENSION)
    # add attributes to overwrite defaults
    data.Angle = 90  # scattering angle in degrees
    data.Temperature = 293  # Temperature of measurement  in K
    data.Viscosity = 1  # viscosity cPoise
    data.Refractive = 1.333  # refractive index
    data.Wavelength = LASER_WAVELENGTH
    # do CONTIN
    dr = js.dls.contin(data, distribution='x')  # also use r

    return dr


def write_g1_vs_gamma_plot_data(filename, x_data, y_data):
    csv_to_write = 'gamma, g1\n'

    for r in range(len(x_data)):
        csv_to_write += str(x_data[r])
        csv_to_write += ','
        csv_to_write += str(y_data[r])
        csv_to_write += '\n'

    with open(filename, 'w') as file:
        file.write(csv_to_write)


def write_g1_vs_tau_plot_data(filename, dr0):
    csv_to_write = 'tau, g1\n'

    x_data = dr0[0]
    y_data = dr0[1]

    for r in range(len(x_data)):
        csv_to_write += str(x_data[r])
        csv_to_write += ','
        csv_to_write += str(y_data[r])
        csv_to_write += '\n'

    with open(filename, 'w') as file:
        file.write(csv_to_write)


""" 
Rh = hydrodynamic radius
PRh = probability of hydrodynamic radius

"""
def write_intensity_weight_plot_data(filename, Rh_data, prob_intensity_weight_data, prob_mass_weight_data, prob_number_weight_data):
    csv_to_write = 'Rh, P(Rh) Intensity Weight, P(Rh) Mass Weight, P(Rh) Number Weight, \n'

    for r in range(len(Rh_data)):
        csv_to_write += str(math.log10(Rh_data[r]))
        csv_to_write += ','
        csv_to_write += str(prob_intensity_weight_data[r])
        csv_to_write += ','
        csv_to_write += str(prob_mass_weight_data[r])
        csv_to_write += ','
        csv_to_write += str(prob_number_weight_data[r])
        csv_to_write += '\n'

    with open(filename, 'w') as file:
        file.write(csv_to_write)


class DLSExptsClass:

    expt_name = ''
    weight = 0.0
    mean = 0.0
    std = 0.0
    mean_err = 0.0
    imean = 0.0
    mean_Deff = 0.0
    Rh_cm = 0.0
    wavevector = 0.0
    mean_Deff_nmns = 0.0
    Rh_nm = 0.0
    wavevector_nm = 0.0
    bf1 = []
    bf3 = []
    bf4 = []
    bf5 = []
    bfX = []            # relaxation time distribution
    bfY = []            # relaxation time distribution


if __name__ == '__main__':

    for filename_to_open in FILENAMES_TO_OPEN:

        file_text = read_correlator_text_file(FILENAME_PATH + filename_to_open + FILENAME_SIN_EXTENSION)
        new_text = trim_correlator_text_file(file_text)
        new_text = average_two_data_columns(new_text)
        write_cleaned_correlator_text_file(FILENAME_PATH + filename_to_open + CLEANED + FILENAME_SIN_EXTENSION, new_text)

        dr = do_contin_fitting(new_text)
        write_g1_vs_gamma_plot_data(FILENAME_PATH + filename_to_open + G1_VS_GAMMA + FILENAME_CSV_EXTENSION, dr.contin_bestFit[0].X, dr.contin_bestFit[0].Y)
        write_g1_vs_tau_plot_data(FILENAME_PATH + filename_to_open + G1_VS_TAU + FILENAME_CSV_EXTENSION, dr[0])
        
        bf = dr[0].contin_bestFit
        
        write_intensity_weight_plot_data(FILENAME_PATH + filename_to_open + PRH_RH + FILENAME_CSV_EXTENSION, bf[3], bf[1], bf[4], bf[5])

        print("Rh from Contin: ")
        print(dr[0].contin_bestFit.ipeaks_name)
        print(dr[0].contin_bestFit.ipeaks)
        print(dr[0].contin_bestFit.ipeaks[0,2]/dr[0].contin_bestFit.ipeaks[0,1])


        # Create a dictionary of objects to store class instances
        # Key = experiment name
        # Value = class instance 
        dict_objects = {}

        # Add data from Jscatter output into the storage class instance 
        dict_objects[filename_to_open] = DLSExptsClass()  # Create class instance
        DLSExptsClass.weight = dr[0].contin_bestFit.ipeaks[0,0]            # weight peak weight
        DLSExptsClass.mean = dr[0].contin_bestFit.ipeaks[0,1]              # mean peak mean
        DLSExptsClass.std = dr[0].contin_bestFit.ipeaks[0,2]               # std peak standard deviation
        DLSExptsClass.mean_err = dr[0].contin_bestFit.ipeaks[0,3]          # mean_err error of mean
        DLSExptsClass.imean = dr[0].contin_bestFit.ipeaks[0,4]             # imean index of peak mean
        DLSExptsClass.mean_Deff = dr[0].contin_bestFit.ipeaks[0,5]         # 1/(q**2*mean) diffusion constant in cm**2/s
        DLSExptsClass.Rh_cm = dr[0].contin_bestFit.ipeaks[0,6]             # Rh hydrodynamic radius in cm
        DLSExptsClass.wavevector = dr[0].contin_bestFit.ipeaks[0,7]        # q wavevector in 1/cm
        DLSExptsClass.mean_Deff_nmns = dr[0].contin_bestFit.ipeaks[0,8]    # 1/(q**2*mean) diffusion constant in nm**2/ns
        DLSExptsClass.Rh_nm = dr[0].contin_bestFit.ipeaks[0,9]             # Rh hydrodynamic radius in nm
        DLSExptsClass.wavevector_nm = dr[0].contin_bestFit.ipeaks[0,10]    # q wavevector in 1/nm
        DLSExptsClass.expt_name = filename_to_open
        DLSExptsClass.bf1 = bf[1]
        DLSExptsClass.bf3 = bf[3]
        DLSExptsClass.bf4 = bf[4]
        DLSExptsClass.bf5 = bf[5]
        DLSExptsClass.bfX = bf.X
        DLSExptsClass.bfY = bf.Y


        # Get data from Jscatter
        x = dict_objects[filename_to_open].bf3  # 
        y1 = dict_objects[filename_to_open].bf1 # intensity weight
        y2 = dict_objects[filename_to_open].bf4 # mass weight
        y3 = dict_objects[filename_to_open].bf5 # number weight

        # Convert from lists to to numpy arrays for plotting 
        x = np.asarray(x, dtype=np.float64)
        y1 = np.asarray(y1, dtype=np.float64)
        y2 = np.asarray(y2, dtype=np.float64)
        y3 = np.asarray(y3, dtype=np.float64)
        
        plt.xscale('log', base=10)

        # plot the 3 sets
        plt.plot(x,y1, label='Intensity weight')
        plt.plot(x,y2, label='Mass weight')
        plt.plot(x,y3, label='Number weight')

        plt.title(filename_to_open)
        plt.xlabel("Rh")
        plt.ylabel("P(Rh)")

        # Create empty plot with blank marker containing the extra label
        plt.plot([], [], ' ', label="Rh = " + str(dict_objects[filename_to_open].Rh_nm) + " (nm)")
        plt.plot([], [], ' ', label="Rh = " + str(dict_objects[filename_to_open].Rh_cm))
        #plt.plot([], [], ' ', label="Rh = " + str(dict_objects[filename_to_open].Rh_nm) + " (nm)")

        # call with no parameters
        plt.legend()

        plt.savefig(FILENAME_PATH + filename_to_open + PRH_RH + ".pdf")
        plt.show()
