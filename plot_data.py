import matplotlib.pyplot as plt
import pickle

def plot(robot):
    fig, axs = plt.subplots(5, 1, constrained_layout=True)
    fig.suptitle('Resultados', fontsize=16)

    plot_vars = [robot.right_wheel_rps_hist, robot.left_wheel_rps_hist, \
        robot.speed_hist, robot.omega_hist, robot.dist_hist]
    plot_titles = ["Roda Direita", "Roda Esquerda", "Velocidade", "Omega", "Desvio"]
    plot_yaxis = ['rps', 'rps', 'm/s', 'rad/s', 'cm']

    for i in range(5):
        axs[i].plot(plot_vars[i])
        axs[i].set_title(plot_titles[i])
        axs[i].set_ylabel(plot_yaxis[i])
        axs[i].set_xlabel('frame')
        axs[i].grid(True, axis='both')

    plt.show()

if __name__ == '__main__':
    with open('data.pkl', 'rb') as input:
        robot = pickle.load(input)
        plot(robot)