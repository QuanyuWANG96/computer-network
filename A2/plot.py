import pandas as pd
import matplotlib.pyplot as plt


res = []
with open('time.log', 'r', encoding='UTF-8') as f2:
    count = 0
    temp = 0
    l = 0
    for line in f2.readlines():
        line = line.strip('\n')
        num = float(line)
        temp += num
        count += 1
        l += 1
        if l == 49 :print(str(num) +"************" + str(count))
        if count == 3:
            count = 0
            res.append(temp/3)
            temp = 0
            count = 0

small = []
medium =[]
large =[]
count = 0
for i in range(len(res)):
    count += 1
    if count == 1 :
        small.append(res[i])
    if count == 2:
        medium.append(res[i])
    if count == 3:
        large.append(res[i])
        count = 0




index = ['baseline', 'discard0.1', 'discard0.2', 'discard=0.3', 'discard=0.4', 'discard=0.5','maxDelay=10', 'Delay=20', 'Delay=30', 'Delay=40', 'Delay=50','both1','both2','both3','both4','both5', 'both6']
df1 = pd.DataFrame({'small': small, 'medium': medium, 'large': large}, index=index)
ax1 = df1.plot.bar(rot=0)
plt.title('Average Transmission Time')
plt.xlabel('Packet Discard Probability')
plt.ylabel('Average Transmission Time(s)')
plt.xticks(rotation=-90)
plt.tick_params(axis='x', labelsize=8)
plt.show()


# plot NO DELAY
small1 = [small[0]]+small[1:6]
medium1 = [medium[0]]+medium[1:6]
large1 = [large[0]]+large[1:6]

index = ['baseline', 'discard0.1', 'discard0.2', 'discard0.3', 'discard0.4', 'discard0.5']
df1 = pd.DataFrame({'small': small1, 'medium': medium1, 'large': large1}, index=index)
ax1 = df1.plot.bar(rot=0)
plt.title('Maximum Delay = 0')
plt.xlabel('Packet Discard Probability')
plt.ylabel('Average Transmission Time(s)')
plt.show()

# plot NO DISCARD
small2 = [small[0]]+small[6:11]
medium2 = [medium[0]]+medium[6:11]
large2 = [large[0]]+large[6:11]
index = ['baseline','delay10', 'delay20', 'delay30', 'delay40', 'delay50']
df2 = pd.DataFrame({'small': small2, 'medium': medium2, 'large': large2}, index=index)
ax2 = df2.plot.bar(rot=0)
plt.title('Packet Discard Probability = 0')
plt.xlabel('Maximum Delay (ms)')
plt.ylabel('Average Transmission Time(s)')
plt.show()


#
# # plot DELAY=20 and DISCARD
# small3 = [small[7]]+small[11:14]
# medium3 = [medium[7]]+medium[11:14]
# large3 = [large[7]]+large[11:14]
# index = ['discard=0','discard=0.1', 'discard=0.2', 'discard=0.3']
# df3 = pd.DataFrame({'small': small3, 'medium': medium3, 'large': large3}, index=index)
# ax3 = df3.plot.bar(rot=0)
# plt.title('Delay and Discard, Maximum Delay = 20 ms')
# plt.xlabel('Packet Discard Probability')
# plt.ylabel('second')
# plt.show()
#
# # plot DELAY=40 and DISCARD
# small3 = [small[9]]+small[14:]
# medium3 = [medium[9]]+medium[14:]
# large3 = [large[9]]+large[14:]
# index = ['discard=0','discard=0.1', 'discard=0.2', 'discard=0.3']
# df4 = pd.DataFrame({'small': small3, 'medium': medium3, 'large': large3}, index=index)
# ax4 = df4.plot.bar(rot=0)
# plt.title('Delay and Discard, Maximum Delay = 40 ms')
# plt.xlabel('Packet Discard Probability')
# plt.ylabel('second')
# plt.show()

