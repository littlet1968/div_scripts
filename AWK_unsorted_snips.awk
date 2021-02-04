unsorted AWK stuff

# checks if IP grater than 124 (basic if)
nmap -n -sP 192.168.1.0/24 | awk 'BEGIN{ERR=""}/^Nmap scan/{IP=$5;split(IP,add,".");if (add[4]<124) ERR=""; else ERR="Too many IPs"; };/^MAC/{print IP,$3}END{print ERR}'
