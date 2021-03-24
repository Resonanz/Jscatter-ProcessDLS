import jscatter as js
import numpy as np

FILENAME_PATH = 'data/'
FILENAME_TO_OPEN = 'Liposomes (200mW 4.1mL 1-24 diluted)'
FILENAME_EXTENSION = '.SIN'

NOISEY_LINES = 100  # Noisey lines of data at start of text file

search_text_start = '[CorrelationFunction]\n'
search_text_end = '\n[RawCorrelationFunction]'


def read_correlator_text_file():
    with open(FILENAME_PATH + FILENAME_TO_OPEN + FILENAME_EXTENSION, 'r') as file:
        return file.read()


def trim_correlator_text_file(text):
    idx_start = (text.find(search_text_start)) + len(search_text_start)
    idx_end = (text.find(search_text_end))
    return text[idx_start:idx_end]


def average_two_data_columns(text):
    averaged_data = ''
    noisey_data_delete_line_counter = 0

    line = text.split('\n')  # Split into lines using \n
    print(line)
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


def write_modified_correlator_text_file(text):
    with open(FILENAME_PATH + FILENAME_TO_OPEN + '(cleaned)' + FILENAME_EXTENSION, 'w') as file:
        file.write(text)


def do_contin_fitting(text):
    t = js.loglist(1, 10000, 1000)  # times in microseconds
    q = 4 * np.pi / 1.333 / 632 * np.sin(np.pi / 2)  # 90 degrees for 632 nm , unit is 1/nm**2
    D = 0.05 * 1000  # nm**2/ns * 1000 = units nm**2/microseconds
    gamma = q*q*D
    print(np.sin(np.pi/2))
    noise = 0.0001  # typical < 1e-3
    #data = js.dA(np.c_[t, 0.95 * np.exp(-q ** 2 * D * t) + noise * np.random.randn(len(t))].T)
    data = js.dA('data/output.txt')
    # add attributes to overwrite defaults
    data.Angle = 90  # scattering angle in degrees
    data.Temperature = 293  # Temperature of measurement  in K
    data.Viscosity = 1  # viscosity cPoise
    data.Refractive = 1.333  # refractive index
    data.Wavelength = 632  # wavelength
    # do CONTIN
    dr = js.dls.contin(data, distribution='x')  # also use r

    #print(dr.contin_bestFit[0].ipeaks)  # contains the 11 contin_bestFit.peaks results, but in three lists???

    print(dr.X)

    #print(dr[0].contin_bestFit)
    #print(dr[0].contin_bestFit.ipeaks_name)

    js.dls.contin_display(dr)  # display overview
    return dr


def write_g1_vs_gamma_plot_data(x_data, y_data):
    csv_to_write = 'gamma, g1\n'

    length = len(x_data)

    for l in range(0, length - 1):
        csv_to_write += str(x_data[l])
        csv_to_write += ','
        csv_to_write += str(y_data[l])
        csv_to_write += '\n'

    with open(FILENAME_PATH + FILENAME_TO_OPEN + '(g1 vs gamma).csv', 'w') as file:
        file.write(csv_to_write)


def write_g1_vs_tau_plot_data(x_data, y_data):
    csv_to_write = 'tau, g1\n'

    length = len(x_data)

    for l in range(0, length - 1):
        csv_to_write += str(x_data[l])
        csv_to_write += ','
        csv_to_write += str(y_data[l])
        csv_to_write += '\n'

    with open(FILENAME_PATH + FILENAME_TO_OPEN + '(g1 vs tau).csv', 'w') as file:
        file.write(csv_to_write)


if __name__ == '__main__':
    file_text = read_correlator_text_file()
    new_text = trim_correlator_text_file(file_text)
    new_text = average_two_data_columns(new_text)
    write_modified_correlator_text_file(new_text)

    dr = do_contin_fitting(new_text)
    write_g1_vs_gamma_plot_data(dr.contin_bestFit[0].X, dr.contin_bestFit[0].Y)
    write_g1_vs_tau_plot_data(dr.X, dr.Y)
