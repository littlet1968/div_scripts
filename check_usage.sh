#!/bin/bash

/usr/bin/top -n1 | /bin/grep -i -C3 cpu\(s\) | /usr/bin/tee "log.txt"

string1=$(/bin/grep -i cpu\(s\) log.txt)
string3=$(/bin/grep -i swap: log.txt)

#===============================================================================
# Get CPU percent_used
#===============================================================================

totalCpu=$(/bin/echo $string1 | /bin/sed 's/\s\s*/ /g' | /bin/cut -d'%' -f1 | /bin/cut -d' ' -f2)
/bin/echo
/bin/echo "LOOK HERE ..."
/bin/echo
/bin/echo "Percentage of used CPU    = "$totalCpu"%   :: escalate to App owner (for SQL tuning) if       > 90%"

#===============================================================================
# Get Memory percent_used
# -----------------------
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

/bin/cat /proc/meminfo | /bin/grep MemTotal > "/tmp/log.txt"
/bin/cat /proc/meminfo | /bin/grep Active\: >> "/tmp/log.txt"

totalMem=`/bin/grep -i mem /tmp/log.txt | /bin/awk '{print $2}' `
usedMem=`/bin/grep -i act /tmp/log.txt | /bin/awk '{print $2}' `
pctUsedMem=`/bin/echo "scale=2;$usedMem/$totalMem*100" | /usr/bin/bc`
/bin/echo "Percentage of used memory =" $pctUsedMem"%  :: escalate to DBA (DB bounce needed) if          > 95%"

#===============================================================================
# Get Swap percent_used
#===============================================================================

totalSwap1=$(/bin/echo $string3 | /bin/sed 's/\s\s*/ /g' | /bin/cut -d' ' -f2)
totalSwap2="${totalSwap1%?}"
c=$totalSwap2
usedSwap1=$(/bin/echo $string3 | /bin/sed 's/\s\s*/ /g' | /bin/cut -d' ' -f4)
usedSwap2="${usedSwap1%?}"
d=$usedSwap2
percentageUsedSwap2=$(/bin/echo "scale=4;$d/$c*100" | /usr/bin/bc)
percentageUsedSwap="${percentageUsedSwap2%??}"
/bin/echo "Percentage of used swap   =" $percentageUsedSwap"%      :: escalate to SysAdmin (swap undersized) if      > 50%"
/bin/echo
/bin/echo

#===============================================================================
# List top-10 memory consuming PIDs
#===============================================================================

/bin/echo
/bin/echo "List ot top-10 memory consuming PIDs"
/bin/echo "------------------------------------"
/bin/echo
/bin/ps aux | /bin/sort +5 -6 -n -r | /usr/bin/head -10
