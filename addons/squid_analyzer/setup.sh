#!/bin/sh

# This is a simple FC*/redhat setup file for squid analyzer,
# Version .02
# www.parspooyesh.com

prog_name="squid_analyzer"
squid_analyzer_root="/usr/local/IBSng/addons/squid_analyzer"
init_d_root="/etc/init.d"
logrotate_d_root="/etc/logrotate.d"
analyze_log_root="/var/log/IBSng"
chk_config="/sbin/chkconfig"

# mkdir even log dir
    
if [ ! -d $analyze_log_root ]; then
    mkdir $analyze_log_root
fi

set_service(){
#copy the service startup file and set it to run on boot
    if [ -f $init_d_root/squid_analyzer ]; then
	echo "init file exists, Do you want to overwrite it? (y/n)"
	while :
	do
	    read i_owrite
	    case $i_owrite in
		y)
		    rm -f $init_root_d/squid_analyer >> $analyze_log_root/squid_analyzer.log 2>&1
	    	    cp $squid_analyzer_root/init.d/squid_analyzer $init_d_root >> $analyze_log_root/squid_analyzer.log 2>&1
	    	    break
	    	    ;;
		n)
		    break
		    ;;
		*)
		    echo "y or n"
		    ;;
	    esac
	done
    else
        cp $squid_analyzer_root/init.d/squid_analyzer $init_d_root >> $analyze_log_root/squid_analyzer.log 2>&1
    fi
    $chk_config --level 35 $prog_name on >> $analyze_log_root/squid_analyzer.log 2>&1
    echo "Startup script is copied and set to be run on boot."
}

set_logrotate(){
#copy logrotate files
    if [ -f $logrotate_d_root/squid ]; then
    	echo "logrotate conf are exists right now. do you want to overwrite them? (y/n)"
    	while :
    	do
    	    read l_owrite
    	    case $l_owrite in
    		y)
    		    rm -f $logrotate_d_root/squid* >> $analyze_log_root/squid_analyzer.log 2>&1
		    cp $squid_analyzer_root/logrotate.d/* $logrotate_d_root >> $analyze_log_root/squid_analyzer.log 2>&1
    		    break
    		    ;;
    		n)
    		    break
    		    ;;
    		*)
    		    echo "y or n"
    		    ;;
    	    esac
    	done
    else
	cp $squid_analyzer_root/logrotate.d/* $logrotate_d_root >> $analyze_log_root/squid_analyzer.log 2>&1
    fi
    echo "Logrotation is set."
}

set_conf(){
#cp conf file
    if [ -f $conf_dir/squid_analyzer.conf ]; then
	echo "Analyze config file exists, Do you want to overwrite it with default conf? (y/n)"
	while :
	do
	    read c_owrite
	    case $c_owrite in
		y)
		    rm -f $squid_analyzer_root/conf/squid_analyzer.conf
   		    cp $squid_analyzer_root/conf/squid_analyzer.conf.default $squid_analyzer_root/conf/squid_analyzer.conf >> $analyze_log_root/squid_analyzer.log 2>&1
   		    break
    		    ;;
    		n)
    		    break
    		    ;;
    		*)
    		    echo "y or n"
    		    ;;
    	    esac
    	done
    else
	cp $squid_analyzer_root/conf/squid_analyzer.conf.default $squid_analyzer_root/conf/squid_analyzer.conf >> $analyze_log_root/squid_analyzer.log 2>&1
    fi
    echo "Config file is copied and will be used in next service start."
}


description="Hi there, this is the setup script for Squid Analyzer.\n
Here is your options:\n
----------------------\n
Choose	  To\n
------    ------------\n
auto    : Do Installation completely.\n
aconf   : Copy the squid analyzer config to $conf_dir as squid_analyzer.conf .\n
lconf	: Copy the logrotation files for squid and squid_analyzer to $logrotate_d_root.\n
setinit : Copy the service startup script to $init_d_root and set to run on boot.\n
quit	: Exit the setup and back to shell.\n
help	: Print this menu.\n

All installation logs will be written in $analyze_log_root, check it.\n
"

echo -e $description
while :
do
    echo -e "Your Choice:"
    read input_str
    case $input_str in
	auto)
    		echo "Start Auto Installation ..."
    		set_service
    		set_logrotate
    		set_conf
    		echo "Analyzer is fully installed."
		;;
	lconf)
		set_logrotate
		;;
	aconf)
		set_conf
		;;
	setinit)
		set_service
		;;
	quit)
		echo "Exit Operation ..."
		break
		;;
	help)
		echo -e $description
		;;
	*)
		echo "Sorry, not a defined option"
		;;
    esac
done
echo "BaBye ;)"
