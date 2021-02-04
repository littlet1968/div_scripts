#!/bin/bash

#===============================================================================
# Get CPU usage data
#===============================================================================

/bin/echo " "
/bin/echo "===== CPU DATA ===="
/bin/echo " "
/usr/bin/sar -o /home/oracle/c1_process_chk.out 10 6

#===============================================================================
# Get Memory usage data
# ---------------------
# Calculation based on OEM process (MOS Doc ID 1908853.1 )
#
# formula used by Enterprise Manager 12.1.0.3 for Linux Memory Utilization (%), for example:
# Memory Utilization (%) = (100.0 * (activeMem) / realMem)
#  = 100 * 25046000/99060536
#  = 25.28
# EM Shows : 25.5
# Here, activeMem is Active Memory (Active), and realMem is Total Memory (MemTotal).
#
#===============================================================================

/bin/rm /tmp/log.txt
/bin/cat /proc/meminfo | /bin/grep MemTotal >> "/tmp/log.txt"
/bin/cat /proc/meminfo | /bin/grep Active\: >> "/tmp/log.txt"

totalMem=`/bin/grep -i mem /tmp/log.txt | /bin/awk '{print $2}' `
usedMem=`/bin/grep -i act /tmp/log.txt | /bin/awk '{print $2}' `
pctUsedMem=`/bin/echo "scale=2;$usedMem/$totalMem*100" | /usr/bin/bc`
/bin/echo " " >> /tmp/c1_process_chk.out
/bin/echo " " >> /tmp/c1_process_chk.out
/bin/echo "===== PERCENTAGE OF MEMORY USED ===== " $pctUsedMem"% " >> /tmp/c1_process_chk.out

#===============================================================================
# Get Swap usage data
#===============================================================================

/bin/echo " " >> /tmp/c1_process_chk.out
/bin/echo " " >> /tmp/c1_process_chk.out
/bin/echo "===== SWAP USAGE ==== " >>  /tmp/c1_process_chk.out
/bin/echo " " >> /tmp/c1_process_chk.out
/usr/bin/free -g >> /tmp/c1_process_chk.out
