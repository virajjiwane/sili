import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import UnivariateSpline
criticalproximity = 0.12 / 2
piperadius= (0.19/ 2)

def avgradius(radii):
    r = 0
    for i in range(0, 7):
        r += radii[i]

    return r / 8

# def circledistance():
#     dis=[]
#     time = df.iloc[:,10].values/1000
#
#     acc = df.iloc[:,11].values
#     acc = np.subtract(acc,acc[0])
#     cacc=acc[0]
#     cvel = 0
#     s = cvel*time[0] +0.5*cacc*time[0]*time[0]
#
#     dis.append(s)
#     print(acc)
#     for i in range(1,len(acc)):
#         if acc[i] == 0:
#             s = cvel * (time[i]-time[i-1])
#             dis.append(s)
#         elif acc[i]>0:
#             s = cvel*(time[i]-time[i-1]) + 0.5*acc[i]*(time[i]-time[i-1])*(time[i]-time[i-1])
#             cvel = cvel + acc[i]*(time[i]-time[i-1])
#             dis.append(s)
#
#         else :
#             s = cvel*(time[i]-time[i-1]) + 0.5*acc[i]*(time[i]-time[i-1])*(time[i]-time[i-1])
#             cvel = cvel + acc[i]*(time[i]-time[i-1])
#             dis.append(s)
#
#     return dis


def circledistance():
    for i in range(1,len(df.iloc[:,10])):
        time = df.iloc[:i,10]/1000
        acc = df.iloc[:i,11]
        accdf = pd.DataFrame(acc).diff().values.ravel()
        accdf[0]=0
        vel = []
        for t in range(len(time)):
            ttime = time[:t]
            tacc = accdf[:t]
            vel.append(np.trapz(tacc,ttime))

        distance.append(np.trapz(vel,time))




def plotcriticalproximity(i):
    if i%5 ==0:
        x = criticalproximity * np.sin(theta)
        y = criticalproximity * np.cos(theta)
        #z = df.iloc[i].values[10] / 1000
        z = distance[i]
        ax.plot(x, z * np.ones(np.size(x)), y, c='k')


def plotpipe(i):
    if i%5==0:
        x = piperadius * np.sin(theta)
        y = piperadius * np.cos(theta)
        #z = df.iloc[i].values[10] / 1000
        z = distance[i]
        ax.plot(x, z * np.ones(np.size(x)), y, c='b')


def plotwax(i):
    radius = avgradius(df.iloc[i] / 100 + 0.11 / 2)
    x = radius * np.sin(theta)
    y = radius * np.cos(theta)
    #z = df.iloc[i].values[10] / 1000
    z = distance[i]

    if radius < piperadius:
        if radius < criticalproximity:
            ax.plot(x, z * np.ones(np.size(x)), y, c='r')
            import os
            os.system("echo -n '\a'")
        else:
            ax.plot(x, z * np.ones(np.size(x)), y, c='y')


def plotallwax():
    for i in range(df.iloc[:,0].count()-1):
        plotpipe(i)
        plotwax(i)
        plotcriticalproximity(i)

radius = []

# def plotWax(i):
#     radius = splResult.item(i)
#     x = radius * np.sin(theta)
#     y = radius * np.cos(theta)
#     #z = df.iloc[i].values[10] / 1000
#     z = dis.item(i)
#
#     if radius < piperadius:
#         if radius < criticalproximity:
#             ax.plot(x, z * np.ones(np.size(x)), y, c='r')
#             import os
#             os.system("echo -n '\a'")
#         else:
#              ax.plot(x, z * np.ones(np.size(x)), y, c='y')



from easygui import fileopenbox

reading = fileopenbox(msg="Select a csv file.", title="Wax deposition visualization")

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')
theta = np.linspace(0, 2 * np.pi, 100)

#
# z = np.linspace(-2, 2, 100)
# r = z**2 + 1
# x = 4 * np.sin(theta)
# y = 4 * np.cos(theta)
# ax.plot(x, 3*np.ones(np.size(x)), y, label='parametric curve')
#
#
# z = np.linspace(-2, 2, 100)
# r = z**2 + 1
# x = 4 * np.sin(theta)
# y = 4 * np.cos(theta)
# ax.plot(x, 4*np.ones(np.size(x)), y, label='parametric curve')

df = pd.read_csv(reading)

time = df.iloc[:,10]/1000
distance = np.array(time)

for i in range(df.iloc[:,0].count()-1):
    radius.append(avgradius(df.iloc[i] / 100 + 0.11 / 2))

distance = []
circledistance()
plotallwax()

# spl = UnivariateSpline(distance, np.array(radius))
#
#
# dis = np.linspace(distance.min(),distance.max(),distance.size*2)
# splResult = spl(dis)
#
# for i in range(distance.size*2-1):
#     plotWax(i)


#
# def plotalltemp(reading):
#     df = pd.read_csv(reading)
#     temp = df['t1']
#     x = temp
#     y = 0.09 * np.ones(np.size(temp))
#     z = df['time'].values / 1000
#     ax.plot(x, z, y, c='g')


# plotalltemp(reading)




red_patch = mpatches.Patch(color='red', label='Critical section')
blue_patch = mpatches.Patch(color='blue', label='Pipe')
black_patch = mpatches.Patch(color='black', label='Critical proximity level')
yellow_patch = mpatches.Patch(color='yellow', label='Wax deposition proximity')

ax.set_xlabel('X View')
ax.set_ylabel('Length')
ax.set_zlabel('Z View')
# custom = [ax.plot(np.NaN, np.NaN, np.NaN, c='y', label="Wax deposited proximity"),ax.plot(np.NaN, np.NaN, np.NaN, c='k', label="Critical proximity"),ax.plot(np.NaN, np.NaN, np.NaN, c='b', label="Pipeline")]
ax.legend(handles=[blue_patch, yellow_patch, red_patch, black_patch])
for angle in range(0, 360):
    ax.view_init(0, angle)
    plt.draw()
    plt.pause(.0005)
