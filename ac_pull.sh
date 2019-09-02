#FlightGear aircraft updater script
#intended for FG aircrafts, but can be used to upgradde any git repo

#Author: Rudolf

#add the directories containing aircraft directories here
#add as many as you wish
#use absolute path

FGAIRCRAFT=(~/.fgfs/Aircraft)

for dir in $FGAIRCRAFT;
do
	cd $dir
	todo=$(find ./ -name ".git" -type d)
	#echo "todo: " $todo
	work=$(pwd)
	for ac in $todo;
	do
		cd $work
		cd $ac
		cd ..
		pwd
		git pull
		echo ---
	done
	cd
done
