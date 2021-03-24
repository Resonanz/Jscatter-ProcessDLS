import jscatter as js
import numpy as np

FILENAMES_TO_OPEN = [
    'Liposomes (30mW 1.5mL undiluted)',
    'Liposomes (40mW 1.5mL 1-1 diluted)',
    'Liposomes (60mW 2.25mL 1-2 diluted)',
    'Liposomes (60mW 3mL 1-3 diluted)',
    'Liposomes (60mW 3.75mL 1-4 diluted)',
    'Liposomes (100mW 1.65mL 1-9 diluted)',
    'Liposomes (200mW 3.3mL 1-19 diluted)',
    'Liposomes (200mW 4.1mL 1-24 diluted)'
]

FILENAME_PATH = 'data/'
FILENAME_SIN_EXTENSION = '.SIN'
FILENAME_CSV_EXTENSION = '.csv'
CLEANED = ' (cleaned)'
G1_VS_GAMMA = ' (g1 vs gamma)'
G1_VS_TAU = ' (g1 vs tau)'


NOISEY_LINES = 100  # Noisey lines of data at start of text file

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


def do_contin_fitting(text):
    t = js.loglist(1, 10000, 1000)  # times in microseconds
    q = 4 * np.pi / 1.333 / 632 * np.sin(np.pi / 2)  # 90 degrees for 632 nm , unit is 1/nm**2
    D = 0.05 * 1000  # nm**2/ns * 1000 = units nm**2/microseconds
    gamma = q*q*D
    print(np.sin(np.pi/2))
    noise = 0.0001  # typical < 1e-3
    #data = js.dA(np.c_[t, 0.95 * np.exp(-q ** 2 * D * t) + noise * np.random.randn(len(t))].T)
    data = js.dA(FILENAME_PATH + filename_to_open + CLEANED + FILENAME_SIN_EXTENSION)
    # add attributes to overwrite defaults
    data.Angle = 90  # scattering angle in degrees
    data.Temperature = 293  # Temperature of measurement  in K
    data.Viscosity = 1  # viscosity cPoise
    data.Refractive = 1.333  # refractive index
    data.Wavelength = 632  # wavelength
    # do CONTIN
    dr = js.dls.contin(data, distribution='x')  # also use r

    #print(dr.contin_bestFit[0].ipeaks)  # contains the 11 contin_bestFit.peaks results, but in three lists???

    #print(dr[0].contin_bestFit)
    #print(dr[0].contin_bestFit.ipeaks_name)

    js.dls.contin_display(dr)  # display overview
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


if __name__ == '__main__':

    for filename_to_open in FILENAMES_TO_OPEN:

        file_text = read_correlator_text_file(FILENAME_PATH + filename_to_open + FILENAME_SIN_EXTENSION)
        new_text = trim_correlator_text_file(file_text)
        new_text = average_two_data_columns(new_text)
        write_cleaned_correlator_text_file(FILENAME_PATH + filename_to_open + CLEANED + FILENAME_SIN_EXTENSION, new_text)

        dr = do_contin_fitting(new_text)
        write_g1_vs_gamma_plot_data(FILENAME_PATH + filename_to_open + G1_VS_GAMMA + FILENAME_CSV_EXTENSION, dr.contin_bestFit[0].X, dr.contin_bestFit[0].Y)
        write_g1_vs_tau_plot_data(FILENAME_PATH + filename_to_open + G1_VS_TAU + FILENAME_CSV_EXTENSION, dr[0])
