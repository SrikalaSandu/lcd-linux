import syslog
import subprocess
import os

def configure_lcd4linux():
    
    conf_file = "/rfs/etc/lcd4linux/lcd4linux.conf.advantech"
    conf_link = "/etc/lcd4linux.conf"
    
    subprocess.run(["systemctl", "stop", "lcd4linux"])
    if os.path.exists(conf_link):
        syslog.syslog(syslog.LOG_LOCAL0 | syslog.LOG_ALERT, \
                  "remove lcd default")
        os.remove(conf_link)   
        if os.path.exists(conf_file):
            os.symlink(conf_file, conf_link)
            os.system("chmod 600 /etc/lcd4linux.conf")
            subprocess.run(["systemctl", "enable", "lcd4linux"])
            subprocess.run(["systemctl", "start", "lcd4linux"])
   
def get_manufacturer_info():
    dmidecode_cmd = "/usr/sbin/dmidecode"
    syslog.syslog(syslog.LOG_LOCAL0 | syslog.LOG_ALERT, \
                    "get_manufacturer")
    if os.path.exists(dmidecode_cmd):
        syslog.syslog(syslog.LOG_LOCAL0 | syslog.LOG_ALERT, \
                    "dmidecode success")
        chassis_info = subprocess.Popen(["dmidecode", "-t", "chassis"], stdout=subprocess.PIPE)
        manf_info = subprocess.Popen(["grep", "Manufacturer"], stdin=chassis_info.stdout, stdout=subprocess.PIPE)
        chassis_info.stdout.close()
        manufacturer = manf_info.communicate()[0].decode().split(":")[1].strip()
        if manufacturer=="Advantech":
            configure_lcd4linux()
            syslog.syslog(syslog.LOG_LOCAL0 | syslog.LOG_ALERT, \
                    "configured lcd4linux")
        else:
            subprocess.run(["systemctl", "disable", "lcd4linux"])        