#!/usr/bin/zsh

start_date="2005-01-01"
end_date="2015-01-01"
start_cash="10000"


help_function () {
    echo "Usage: optimize.zsh [options] <project name> [opt 1 name] [opt 1 start] [opt 1 end] [opt 1 step] ..."
    echo
    echo "OPTIONS"
    echo
    echo "-h --help : print help function and exit"
    echo
    echo "-s --start_date <start date> : set start date, if not given, defaults to $start_date"
    echo
    echo "-e --end_date <end date> : set end date, if not given, defaults to $end_date"
    echo
    echo "-c --start_cash <starting cash> : set starting cash, if not given, defaults to $start_cash"
}

pos_args=()

while [[ $# > 0 ]]; do
  case $1 in
    -h|--help)
        help_function
        exit 0
        ;;
    -s|--start_date)
      start_date=$2
      shift # past argument
      shift # past value
      ;;
    -e|--end_date)
      end_date=$2
      shift # past argument
      shift # past value
      ;;
    -c|--start_cash)
      start_cash=$2
      shift # past argument
      shift # past value
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
      pos_args+=( $1 ) # save positional arg
      shift # past argument
      ;;
  esac
done

# check for valid project
if [[ ! -d "container/$pos_args[1]" ]]; then
    echo "bad project name $1, exiting."
    exit 1
elif [[ ! $pos_args[1] ]]; then
    echo "no project name given, exiting."
    exit 1
fi

# activate venv
# MUST run from QC_Projects directory
source venv/bin/activate
cd container

proj_name=$pos_args[1]
pos_args=("${pos_args[@]:1}")

case ${#pos_args[@]} in
    4)
        echo "BEGINNING OPTIMIZATION"
        name1=$pos_args[1]
        start1=$pos_args[2]
        end1=$pos_args[3]
        step1=$pos_args[4]
        for (( i=$start1; i<=$end1; i+=$step1 )); do
            # this is where i would actually do the backtest
            echo
            echo "$start_date to $end_date, starting with $start_cash, params $name1=$i"
            python3 ../param_updater.py $proj_name $start_date $end_date $start_cash $name1 $i
            lean cloud backtest $proj_name --push
            echo
        done
        deactivate
        echo "FINISHED OPTIMIZATION"
        exit 0
        ;;
    8)
        echo "BEGINNING OPTIMIZATION"
        name1=$pos_args[1]
        start1=$pos_args[2]
        end1=$pos_args[3]
        step1=$pos_args[4]
        name2=$pos_args[5]
        start2=$pos_args[6]
        end2=$pos_args[7]
        step2=$pos_args[8]
        for (( i=$start1; i<=$end1; i+=$step1 )); do
            for (( j=$start2; j<=$end2; j+=$step2 )); do
                # this is where i would actually do the backtest
                echo
                echo "$start_date to $end_date, starting with $start_cash, params $name1=$i, $name2=$j"
                echo python3 ../param_updater.py $proj_name $start_date $end_date $start_cash $name1 $i $name2 $j
                lean cloud backtest $proj_name --push
                echo
            done
        done
        deactivate
        echo "FINISHED OPTIMIZATION"
        exit 0
        ;;
    12)
        echo "BEGINNING OPTIMIZATION"
        name1=$pos_args[1]
        start1=$pos_args[2]
        end1=$pos_args[3]
        step1=$pos_args[4]
        name2=$pos_args[5]
        start2=$pos_args[6]
        end2=$pos_args[7]
        step2=$pos_args[8]
        name3=$pos_args[9]
        start3=$pos_args[10]
        end3=$pos_args[11]
        step3=$pos_args[12]
        for (( i=$start1; i<=$end1; i+=$step1 )); do
            for (( j=$start2; j<=$end2; j+=$step2 )); do
                for (( k=$start3; k<=$end3; k+=$step3 )); do
                    # this is where i would actually do the backtest
                    echo
                    echo "$start_date to $end_date, starting with $start_cash, params $name1=$i, $name2=$j, $name3=$k"
                    echo python3 ../param_updater.py $proj_name $start_date $end_date $start_cash $name1 $i $name2 $j $name3 $k
                    lean cloud backtest $proj_name --push
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
