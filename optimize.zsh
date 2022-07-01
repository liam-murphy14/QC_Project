#!/usr/bin/zsh

start_date="2005-01-01"
end_date="2015-01-01"
start_cash="10000"
number_opts="2"
shifts=0


help_function () {
    echo "Usage: optimize.zsh [options] <project name>"
    echo
    echo "OPTIONS"
    echo
    echo "-h : print help function and exit"
    echo
    echo "-s <start date> : set start date, if not given, defaults to $start_date"
    echo
    echo "-e <end date> : set end date, if not given, defaults to $end_date"
    echo
    echo "-c <starting cash> : set starting cash, if not given, defaults to $start_cash"
    echo
    echo "-o <number of optimization params> : set number of optimization parameters, if not given, defaults to $number_opts"
}

while getopts "hs:e:c:o:" option; do
    case $option in
    h) # help
        help_function
        exit 0
        ;;
    s) # set start date
        start_date=$OPTARG
        shifts=$(($shifts + 2))
        ;;
    e) # set end date
        end_date=$OPTARG
        shifts=$(($shifts + 2))
        ;;
    c) # set start cash
        start_cash=$OPTARG
        shifts=$(($shifts + 2))
        ;;
    o) # number of optimizations 
        number_opts=$OPTARG
        shifts=$(($shifts + 2))
        ;;
    \?) # invalid option
        echo "Error: invalid option, exiting."
        exit
        ;;
    esac
done

# move args
while [[ $shifts > 0 ]]; do
    shift
    shifts=$(($shifts - 1))
done

# check for valid project
if [[ ! -d "container/$1" ]]; then
    echo "bad project name, exiting."
    exit 1
elif [[ ! $1 ]]; then
    echo "no project name given, exiting."
    exit 1
fi

if [[ $number_opts > 3 ]]; then
    echo "too many parameters: max 3, exiting."
    exit 1
elif [[ $number_opts < 1 ]]; then
    echo "must optimize something, exiting."
    exit 1
fi

param_array=$2

# activate venv
# MUST run from QC_Projects directory
source venv/bin/activate
cd container

case $number_opts in
    1)
        echo "BEGINNING OPTIMIZATION"
        name1=$param_array[1]
        start1=$param_array[2]
        end1=$param_array[3]
        step1=$param_array[4]
        for (( i=$start1; i<=$end1; i+=$step1 )); do
            # this is where i would actually do the backtest
            echo
            python3 ../param_updater.py $1 $start_date $end_date $start_cash $name1 $i
            lean cloud backtest $1 --push
            echo
        done
        deactivate
        echo "FINISHED OPTIMIZATION"
        exit 0
        ;;
    2)
        echo "BEGINNING OPTIMIZATION"
        name1=$param_array[1]
        start1=$param_array[2]
        end1=$param_array[3]
        step1=$param_array[4]
        name2=$param_array[5]
        start2=$param_array[6]
        end2=$param_array[7]
        step2=$param_array[8]
        for (( i=$start1; i<=$end1; i+=$step1 )); do
            for (( j=$start2; j<=$end2; j+=$step2 )); do
                # this is where i would actually do the backtest
                echo
                echo python3 ../param_updater.py $1 $start_date $end_date $start_cash $name1 $i $name2 $j
                lean cloud backtest $1 --push
                echo
            done
        done
        deactivate
        echo "FINISHED OPTIMIZATION"
        exit 0
        ;;
    3)
        echo "BEGINNING OPTIMIZATION"
        name1=$param_array[1]
        start1=$param_array[2]
        end1=$param_array[3]
        step1=$param_array[4]
        name2=$param_array[5]
        start2=$param_array[6]
        end2=$param_array[7]
        step2=$param_array[8]
        name3=$param_array[9]
        start3=$param_array[10]
        end3=$param_array[11]
        step3=$param_array[12]
        for (( i=$start1; i<=$end1; i+=$step1 )); do
            for (( j=$start2; j<=$end2; j+=$step2 )); do
                for (( k=$start3; k<=$end3; k+=$step3 )); do
                    # this is where i would actually do the backtest
                    echo
                    echo python3 ../param_updater.py $1 $start_date $end_date $start_cash $name1 $i $name2 $j $name3 $k
                    lean cloud backtest $1 --push
                    echo
                done
            done
        done
        deactivate
        echo "FINISHED OPTIMIZATION"
        exit 0
        ;;
    \?)
        echo "bad number of optimizations. exiting."
        deactivate
        exit 1
        ;;
esac
