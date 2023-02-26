In this directory, we use Looking Glasses to ping some machines we controlled. 
By monitoring the traffic on the controlled machines, we can deduce the IP address of LGs.
Because the machine may be pinged by others during this experiment, we recommend **using at least two machines to ensure accuracy**.

1. Firstly, adjust the `MACHINE_IPS` in the settings.py file. This variable represents the machines you controlled.

2. Run the command `tcpdump icmp -w output.warts` in your controlled machines to monitor the traffic. After running that command, execute the file `ping_to_one_ip.py` to let LGs ping your controlled machines. When the execution of file `ping_to_one_ip.py` is finished, end that command in your controlled machines. 

3. You should move the `output.warts` of your controlled machines to the subdirectory `result` of this directory. **Note: The `output.warts` should be named as `{x}_receive.warts` where x represent the index of the corresponding machine in `MACHINE_IPS`!**

4. Finally, execute `get_ip_of_lg.py`, the result will be put in the directory `../pickle_bin`.
