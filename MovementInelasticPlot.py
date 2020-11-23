"""This program enables one to visualise a system of falling blocks that inelastically collide. It
becomes clear upon reading the document 'exercise Falling Dominoes'."""
# ---------------------------------- ---------- -------------------------------- --------- --------- ---------
import numpy as np
import matplotlib.pyplot as plt

# define constants and initial conditions:
g = 9.81
x_spacing = 1
x = 0
x_initial = 0
v = 0
increasingMass = False  # if True: masses will increase as described in the solutions
tijdsduur = 100  # time to be plotted
tijdstap = 0.0001  # timestep for calculation
aantal_stappen = int(tijdsduur / tijdstap)  # amount of timesteps in total

tijd = np.linspace(0, tijdsduur, aantal_stappen)  # 1D array of timesteps
inform = np.zeros((2, aantal_stappen))  # array where information (position, velocity, ...) will be stored
t_prev, i = 0, 1

# actual calculation for the free fall + inelastic collision
for pos, t in enumerate(tijd):
    v += g * (t - t_prev)  # free fall velocity
    dx = v * (t - t_prev)
    x = x - dx  # free fall position
    if x < x_initial - i * x_spacing:  # if the block encounters the next mass to collide with
        v = i / (i + 1) * v if not increasingMass else 1 / 2 * v  # change in velocity upon collision
        i += 1  # parameter to look for next collision
    inform[0][pos] = x / x_spacing  # rescale x, store in first row of inform
    inform[1][pos] = v / np.sqrt(g * x_spacing)  # rescale v, store in second row of inform
    t_prev = t

tijd = tijd * np.sqrt(g / x_spacing)  # rescale time

# create figures
fig, axes = plt.subplots(2, sharex='col')
axes[0].plot(tijd, inform[0], linewidth=1)  # plot x
axes[1].plot(tijd, inform[1], linewidth=1)  # plot v
# set ax-labels and layout of plot
axes[0].set_ylabel(r'height $x/x_0$', ha='center', size='medium')
axes[1].set_xlabel(r'time $t.(g/x_0)^{1/2}$')
axes[1].set_ylabel(r'velocity $v . (gx_0)^{-1/2}$', ha='center', size='medium')
axes[0].set_ylim((inform[0, -1], 2))
axes[1].set_ylim((0, inform[1, -1] + 0.5))
axes[1].set_xlim((0, tijdsduur * np.sqrt(g * x_spacing)))
# add one mass in free fall to the figure
axes[0].plot(tijd, - tijd ** 2 / 2, linewidth=0.5, linestyle='--', c='grey', label="one mass in free fall")
axes[1].plot(tijd, tijd, linewidth=0.5, linestyle='--', c='grey')

# case-specific graphs
if increasingMass:
    axes[0].plot(tijd, [- (np.sqrt(2 / 3 + 2) + np.sqrt(2 / 3)) / 2 * t + 0.87 for t in tijd], c='grey', linewidth=1.5,
                 linestyle='--', label="linear motion with $v = (v_{high} + v_{low}) / 2$")
    axes[1].plot(tijd[1000:], [np.sqrt(2 / 3 + 2) for _ in tijd[1000:]], c='orange', linewidth=0.5, linestyle='--',
                 label=r'$v_{high} = \sqrt{8/3}$')
    axes[1].plot(tijd[1000:], [np.sqrt(2 / 3) for _ in tijd[1000:]], c='red', linewidth=0.5, linestyle='--',
                 label=r'$v_{low} = \sqrt{2/3}$')
    axes[1].plot(tijd[400:], [(np.sqrt(2 / 3 + 2) + np.sqrt(2 / 3)) / 2 for _ in tijd[400:]], c='grey', linewidth=1.5,
                 linestyle='--')
    axes[0].set_title("Increasing masses vertically lined up")
    axes[1].legend(loc='lower right')
    axes[0].legend()
else:
    axes[0].set_title(r"Equal masses vertically lined up")
    axes[1].plot(tijd, [1 / 3 * t for t in tijd], c='black', linewidth=1,
                 linestyle=(0, (3, 5, 1, 5)), label=r"$v=g' t$ with $g' = \frac{1}{3}g$")
    axes[0].plot(tijd, -(1 / 6) * tijd ** 2, c='black', linewidth=1,
                 linestyle=(0, (3, 5, 1, 5)), label=r"$x=-\frac{1}{2}g' t^2$ with $g' = \frac{1}{3}g$")
    axes[0].legend()
    axes[0].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    axes[1].legend()
plt.show()
