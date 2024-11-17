#!/bin/bash

# Create files for each metric if none exist
date_ip_file="date_ip.csv"
cpu_load_file="cpu_load.csv"
memory_process_file="memory_process.csv"
cpu_process_file="cpu_process.csv"
memory_usage_file="memory_usage.csv"
disk_usage_file="disk_usage.csv"
recent_logins_file="recent_logins.csv"
auth_log_activity_file="auth_log_activity.csv"
network_traffic_file="network_traffic.csv"
sys_log_activity_file="sys_log_activity.csv"

# Recover date and user IP
date=$(date "+%Y-%m-%d %H:%M:%S")
user_ip=$(hostname -I | awk '{print $1}')

tot_cpu_usage=$(top -bn1 | awk '{sum+=$9} END {print sum}')
tot_memomry_usage=$(free | awk '/Mem:/ {printf "%.2f", $3/$2 * 100}')

# Save date and IP in a dedicated file
echo "$date,$user_ip" > "$date_ip_file"

# Recover the various metrics
cpu_load=$(uptime | awk -F'load average: ' '{print $2}')
top_memory_processes=$(ps aux --sort=-%mem | head -n 6 | awk '{print "PID "$2" "$4"% "$11}' )
top_cpu_processes=$(ps aux --sort=-%cpu | head -n 6 | awk '{print "PID "$2":"$3"%:"$11}' )
memory_usage=$(free -h | grep Mem | awk '{print $3 "/" $2}')
disk_usage=$(df -h | grep '^/dev' | awk '{print $3 "/" $2}' )
recent_logins=$(last -n 3 | awk '{print $1" "$4" "$5" "$6" "$7}' )
uptime=$(uptime -p | sed 's/,//g')
auth_log_activity=$(tail -n 10 /var/log/auth.log | awk '{print $0}')
network_traffic=$(netstat -i | grep -E 'docker0|eth0|lo' | awk '{print $1": Rx "$3" Tx "$7}' )
sys_log_activity=$(tail -n 10 /var/log/syslog | awk '{print $0}')

# Write each metric to its respective file
echo "CPU LOAD :" > "$cpu_load_file"
echo "Load average : $cpu_load" >> "$cpu_load_file"
echo "The total of CPU usage : $tot_cpu_usage %" >> "$cpu_load_file"
echo "UPTIME :" >> "$cpu_load_file"
echo "$uptime" >> "$cpu_load_file"
echo "$top_memory_processes" > "$memory_process_file"
echo "$top_cpu_processes" > "$cpu_process_file"
echo "$memory_usage" > "$memory_usage_file"
echo "The total of memory usage : $tot_memomry_usage %" >> "$memory_usage_file"
echo "$disk_usage" > "$disk_usage_file"
echo "$recent_logins" > "$recent_logins_file"
echo "$auth_log_activity" > "$auth_log_activity_file"
echo "$network_traffic" > "$network_traffic_file"
echo "$sys_log_activity" > "$sys_log_activity_file"

check_critical_state() {
    threshold_cpu=90
    threshold_memory=80

    if (( $(echo "$tot_cpu_usage > $threshold_cpu" | bc -l) )) || (( $(echo "$tot_memomry_usage > $threshold_memory" | bc -l) )); then
        echo "Critical system detected at $date !" | mail -s "Monitoring alert" useremailaddress@gmail.com
    fi
}

check_critical_state
