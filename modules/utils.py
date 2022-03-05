import matplotlib.pyplot as plt


def show_graph(readings):
    temp = [r.get("temp") for r in readings]
    time = [r.get("time") for r in readings]

    plt.plot(time, temp)
    plt.title("Habitat Temperature Readings")
    plt.xlabel("Time (5 seconds)")
    plt.ylabel("Temperature (Deg C)")
    plt.show()
