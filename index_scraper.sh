find ./ -name *.png > namelist.txt; sed -i "s/.\{4\}$//" namelist.txt; sed -ri 's/^.{30}//' namelist.txt
