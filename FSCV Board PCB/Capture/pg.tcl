set x 200
set y 132
set start 1
set end 8
set incrementValue 2.54

# Initialize the loop variable
set i $start

# Use a while loop to iterate through the range
while {$i <= $end} {
    Paste $x $y
    SetProperty "Name" "COND_EN_${i}_SEL"
    incr i 1
    set y [expr {$y + $incrementValue}]
}

#How to use in the command view
#source [file normalize {<file_path_to_capSyncPropPCBFootprint.tcl>}]