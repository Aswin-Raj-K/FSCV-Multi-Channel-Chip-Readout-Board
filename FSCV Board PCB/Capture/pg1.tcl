set csv_file "data.csv"
set fh [open $csv_file r]
set contents [read $fh ]
set col 1
#set x 54.42
set x 180
set y 40.64
set incrementValue 2.54

foreach z $contents {
	if {$col >= 121} {
        #break ;
    
#    puts $x
    Paste $x $y
    SetProperty "Name" $z
    set y [expr {$y + $incrementValue}]
    
    }
incr col 1
}
close $fh