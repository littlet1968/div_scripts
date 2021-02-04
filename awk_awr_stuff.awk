# the following lines can be used to get information out of HTML AWR's
# to get number of users out of html AWR's
grep "Begin Snap:" * | awk '{ match($11,/[0-9]*[0-9]/,arr); print "Number of users: "arr[0] }' > num_users.txt
#
# to calculate CPU % usage busy_time/(busy_time+idle_time) !!!!!
# to get busy time out of AWR
grep "BUSY_TIME" * | awk '{ match($5,/[0-9]{1,3}?,*[0-9]{1,3}?,*[0-9]{1,3}/,arr); print "Busy_Time :"arr[0] }' > busy_time.txt
# to idle  busy time out of AWR
grep "IDLE_TIME" * | awk '{ match($5,/[0-9]{1,3}?,*[0-9]{1,3}?,*[0-9]{1,3}/,arr); print "Idle_Time :"arr[0] }' > idle_time.txt
#
# shared pool memory usage
grep "Memory Usage" * | awk '{ match($8,/[0-9]{1,3}?.*[0-9]/,arr); print $8 "shared pool Memory : " arr[0] }'  >shared_mem4.txt
# host memory usage
grep "Host Mem used for SGA+PGA:" * | awk '{ match($11,/[0-9]{1,3}?.*[0-9]/,arr); print $11 "Host Memory : " arr[0] }' >host_mem4.txt
# SGA Usage
grep "SGA use (MB)" * | awk '{ match($11,/[0-9]{1,3}?.*[0-9]/,arr); print $11 "SGA in use : " arr[0] }' >sga_mem4.txt
# PGA Usage
grep "PGA use (MB)" * | awk '{ match($11,/[0-9]{1,3}?.*[0-9]/,arr); print $11 "PGA in use : " arr[0] }' >pga_mem4.txt


# find gc lost blocks (return lost blocks)
grep "gc blocks lost" *.html|awk ' {(match($7,/[0-9]{1,}/, arr)); if (arr[0] > 0) print $1 "> "  arr[0]; }'


awk -F"PROGRAM=" '/10-NOV-2020 10:/ && !/oemagent/ && !/service_update/ && !/ping/ && !/SERVICE=LISTENER/ { print $2 }' listener.log-2020-11-11|awk -F")" '{ print $1 }'|sort |uniq -c

awk -F"HOST=" '/17-OCT-2020 13:/ && !/oemagent/ && !/service_update/ && !/ping/ && !/SERVICE=LISTENER/ { print $2 }' listener.log-2020-10-18|awk -F")" '{ print $1 }'|sort |uniq -c
