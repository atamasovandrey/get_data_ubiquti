import paramiko
from pythonping import ping
from io import StringIO
import sys

def ssh_command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)
    _, stdout, stderr = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()
    if output:
        print(f'----------------------------------')
        for line in output:
            print(line.strip())
        print(f'----------------------------------')

cmd_deviceip = "echo -n 'Ip-address: '; mca-status | grep 'deviceName' | awk '{split($0,a,\"=\"); print a[6]}' | awk '{split($0,a,\",\"); print a[1]}'; "
cmd_device = "echo -n 'Device: '; mca-status | grep 'deviceName' | awk '{split($0,a,\"=\"); print a[5]}' | awk '{split($0,a,\",\"); print a[1]}'; "
cmd_username = "echo -n 'Username: '; mca-status | grep 'deviceName' | awk '{split($0,a,\"=\"); print a[2]}' | awk '{split($0,a,\",\"); print a[1]}'; "
cmd_mac_user = "echo -n 'MAC-Address: '; mca-status | grep 'deviceName' | awk '{split($0,a,\"=\"); print a[3]}' | awk '{split($0,a,\",\"); print a[1]}'; "
cmd_freq = "echo -n 'Freq: '; mca-status | grep 'freq' | awk '{split($0,a,\"=\"); print a[2]}'; "
cmd_essid = "echo -n 'ESSID: '; mca-status | grep 'essid' | awk '{split($0,a,\"=\"); print a[2]}'; "
cmd_noise = "echo -n 'Noise: '; mca-status | grep 'noise' | awk '{split($0,a,\"=\"); print a[2]}'; "
cmd_signal = "echo -n 'Signal: '; mca-status | grep 'signal' | awk '{split($0,a,\"=\"); print a[2]}'; "
cmd_apmac = "echo -n 'MAC-Address base: '; mca-status | grep 'apMac' | awk '{split($0,a,\"=\"); print a[2]}'; "
cmd_ccq = "echo -n 'CCQ: '; mca-status | grep 'ccq' | awk '{split($0,a,\"=\"); print a[2]}'; "
cmd_wlanPollingQuality = "echo -n 'AirMax Quality: '; mca-status | grep 'wlanPollingQuality' | awk '{split($0,a,\"=\"); print a[2]}'; "
cmd_wlanPollingCapacity = "echo -n 'AirMax Capacity: '; mca-status | grep 'wlanPollingCapacity' | awk '{split($0,a,\"=\"); print a[2]}'; "
cmd_txpower = "echo -n 'TX Power: '; mca-status | grep 'txPower' | awk '{split($0,a,\"=\"); print a[2]}'; "
cmd_mcsrate = "echo -n 'MCS: '; cat /tmp/system.cfg | grep radio.1.rate.mcs | awk '{split($0,a,\"=\"); print a[2]}'; "
cmd_mcsstatus = "echo -n 'MCS auto: '; cat /tmp/system.cfg | grep radio.1.rate.auto | awk '{split($0,a,\"=\"); print a[2]}'; "


cmd = cmd_device + cmd_username + cmd_deviceip + cmd_mac_user + cmd_apmac + cmd_essid + cmd_freq + cmd_txpower + cmd_signal + cmd_noise + cmd_ccq + \
      cmd_wlanPollingQuality + cmd_wlanPollingCapacity + cmd_mcsstatus + cmd_mcsrate

#        "echo -n 'Username: mca-status | grep 'deviceName' | awk '{split($0,a,"="); print a[2]}'"

ipaddr_start = '10.3.21.'
ipaddr_end = '10.3.251.15'
#
# _ipaddr_start = ipaddr_start.split(sep='.', maxsplit=3)
# _ipaddr_end = ipaddr_end.split(sep='.')
#
#
# print(_ipaddr_start)
#
# _ipaddr_start_end = int(_ipaddr_start[-1])
# _ipaddr_end_end = int(_ipaddr_end[-1])
#
# while _ipaddr_start_end <= _ipaddr_end_end:
#     lol = str(_ipaddr_start_end)
#     lol2 = ipaddr_start.replace(_ipaddr_start[-1], lol)
#     print(lol2)
#     _ipaddr_start_end += 1

def pinging(kon):
    # сохраняем ссылку, чтобы потом
    # снова отобразить вывод в консоли.
    tmp_stdout = sys.stdout

    # В переменной `result` будет храниться все,
    # что отправляется на стандартный вывод
    result = StringIO()
    sys.stdout = result

    # Здесь все, что отправляется на стандартный вывод,
    # будет сохранено в переменную `result`.
    #print(f'\n###################### Ping: {kon} ######################')
    ping(kon, verbose=True, count=1, out=sys.stdout)

    # Снова перенаправляем вывод `sys.stdout` на консоль
    sys.stdout = tmp_stdout

    # Получаем стандартный вывод как строку!
    result_string = result.getvalue()
    return result_string

for a in range(46, 78):
    kon = ipaddr_start + str(a)
    a += 1
    res = pinging(kon)
    if 'Reply from' in pinging(kon):
        ssh_command(ip=kon, port=22, user='', passwd='', cmd=cmd)


