import sys
import matplotlib.pyplot as plt

metrics = {}


def plotter(df, title):
    """
    This is the plot function

    Args:
        df: a dataFrame has column names: time, volt
        title: plot title

    Returns:
        None
    """
    peaklist = metrics['peaks']
    ybeat = [df.volt[x] for x in peaklist]
    plt.title(title)
    plt.plot(df.volt, alpha=0.5, color='blue', label="raw signal")
    plt.plot(df.rolling_mean, color='green', label="moving average")
    plt.scatter(peaklist, ybeat, color='red', label="average: %.1f BPM" % metrics['bpm'])
    plt.legend(loc=4, framealpha=0.6)
    plt.show()


def main():
    """
    This is the main function

    Returns:
        None
    """
    import hbAnalysis as hb  # Assuming we named the file 'heartbeat.py'
    import filehander
    import json
    from jsonEncoder import NumpyAwareJSONEncoder

    # get data
    filename = filehander.open_file_dialog()
    df = hb.get_data(filename)

    # Todo: clean the data

    # signal processing
    # calc interested info using the chosen data, and store in metrics
    hb.process(df, metrics)

    # plot the interested value
    plotter(df, "test_data1")

    # store the interested value into file
    j = json.dumps(metrics, cls=NumpyAwareJSONEncoder)
    f = open("data.json", "w")
    f.write(j)
    f.close()


if __name__ == "__main__":
    sys.exit(main())