import subprocess
import sys
from datetime import datetime

HELP = ''' Syntax: python twnpa.py {packets sending interval (sec)} {packets count} {IP address} {number of tests}

 Usage example:
        python twnpa.py 0.001 10000 10.0.0.1 3
        This commnand sends 10000 icmp packets with 1 ms interval to host with 10.0.0.1 IP address. Number of tests attempts is equal to 3.'''

if sys.argv[1] == '-h' or sys.argv[1] == '--help':
    print HELP
    sys.exit()
elif len(sys.argv) < 5:
    print 'Wrong arguments!!!'
    print HELP
    sys.exit()

print '''\n------ Checking network performance ------
IP-address: %s
Packets sending interval: %s ms
Packets count: %s''' % (sys.argv[3],  sys.argv[1], sys.argv[2])
print '------------------------------------------'

for i in range(1, int(sys.argv[4])+1):

    print '\n----------------- Test %s -----------------' %i
    print 'Start time: ', datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print 'In progress...'

    try:
        response = subprocess.check_output(
            ["ping", "-i",  sys.argv[1], "-c",  sys.argv[2],  sys.argv[3]],
            stderr=subprocess.STDOUT,  # get all output
            universal_newlines=True  # return string not bytes
        )
    except subprocess.CalledProcessError:
        response = None

    print 'End time: ', datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if response == None:
        print 'Ping result error! \nExit.'
    else:
        pings = []
        response = response.split('\n')
        for line in response:
            if 'bytes from' in line:
                pings.append(float(line.split()[-2][5:]))
            if 'packet loss' in line:
                temp = line.split(',')
                packets_transmitted = temp[0].split()[0]
                packets_received = temp[1].split()[0]
                packets_loss = (float(packets_transmitted)-float(packets_received))/float(packets_transmitted)*100

        pings.pop(0)

        print '--------------- RESULTS ------------------'
        print 'Packets transmitted:', packets_transmitted
        print 'Packets received:', packets_received
        print 'Packets loss: %s%%' %packets_loss
        print 'Min two way delay = %s ms' %min(pings)
        print 'Max two way delay = %s ms' %max(pings)
        jit = float(max(pings)) - float(min(pings))
        print 'Avarage TWO WAY jitter = %s ms' %jit
        print '------------------------------------------'

